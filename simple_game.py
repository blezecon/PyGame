import pygame
import random
import os
import numpy as np
from pygame.locals import *
from sys import exit
from game_audio import (load_bgm, play_bgm, stop_bgm, set_volume,
                       generate_retro_jump_sound, generate_retro_coin_sound,
                       generate_retro_hit_sound, generate_retro_game_over_sound)  # Import audio functions

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for audio

# Set up the display
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Retro Blue Guy")

# Set game icon
icon = pygame.image.load("hero/Dude_Monster.png").convert_alpha()
pygame.display.set_icon(icon)
# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load background layers
sky_surface = pygame.image.load("images/sky.png")
sky_image = pygame.transform.scale(sky_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
ground_surface = pygame.image.load("images/ground.png")
ground_image = pygame.transform.scale(ground_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
cloud_surface = pygame.image.load("images/cloud.png")
cloud_image = pygame.transform.scale(cloud_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
support_surface = pygame.image.load("images/support.png")
support_image = pygame.transform.scale(support_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
hills_surface = pygame.image.load("images/hills.png")
hills_image = pygame.transform.scale(hills_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
bush_surface = pygame.image.load("images/bush.png")
bush_image = pygame.transform.scale(bush_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
tree_surface = pygame.image.load("images/tree1.png")
tree_image = pygame.transform.scale(tree_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
tree2_surface = pygame.image.load("images/tree2.png")
tree2_image = pygame.transform.scale(tree2_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Font for score
font = pygame.font.SysFont('Arial', 30)

# Heart image
heart_img = pygame.Surface((30, 30))
heart_img.fill(RED)

# Load hero animations directly
def load_hero_idle_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Idle_4.png").convert_alpha()
    frames = []
    for i in range(4):  # 4 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames

def load_hero_run_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Run_6.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames

def load_hero_jump_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Jump_8.png").convert_alpha()
    frames = []
    for i in range(8):  # 8 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames

def load_hero_attack_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Attack1_4.png").convert_alpha()
    frames = []
    for i in range(4):  # 4 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames
# made by BlezecoN
def load_hero_death_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Death_8.png").convert_alpha()
    frames = []
    for i in range(8):  # 8 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames

def load_hero_jump_animation():
    sprite_sheet = pygame.image.load("hero/Dude_Monster_Jump_8.png").convert_alpha()
    frames = []
    for i in range(8):  # 8 frames
        frame = sprite_sheet.subsurface((i * 32, 0, 32, 32))
        # Scale up the frame for better visibility
        frame = pygame.transform.scale(frame, (64, 64))
        frames.append(frame)
    return frames

# Load slime animations directly
def load_slime1_idle_animation():
    sprite_sheet = pygame.image.load("slime/Slime1_Idle_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime1_walk_left_animation():
    sprite_sheet = pygame.image.load("slime/Slime1_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime1_walk_right_animation():
    sprite_sheet = pygame.image.load("slime/Slime1_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Flip horizontally for right movement
        frame = pygame.transform.flip(frame, True, False)
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime1_death_animation():
    sprite_sheet = pygame.image.load("slime/Slime1_Death_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime1_attack_animation():
    sprite_sheet = pygame.image.load("slime/Slime1_Attack_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime2_idle_animation():
    sprite_sheet = pygame.image.load("slime/Slime2_Idle_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime2_walk_left_animation():
    sprite_sheet = pygame.image.load("slime/Slime2_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime2_walk_right_animation():
    sprite_sheet = pygame.image.load("slime/Slime2_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Flip horizontally for right movement
        frame = pygame.transform.flip(frame, True, False)
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames
# made by BlezecoN
def load_slime2_death_animation():
    sprite_sheet = pygame.image.load("slime/Slime2_Death_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime2_attack_animation():
    sprite_sheet = pygame.image.load("slime/Slime2_Attack_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime3_idle_animation():
    sprite_sheet = pygame.image.load("slime/Slime3_Idle_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime3_walk_left_animation():
    sprite_sheet = pygame.image.load("slime/Slime3_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime3_walk_right_animation():
    sprite_sheet = pygame.image.load("slime/Slime3_Walk_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Flip horizontally for right movement
        frame = pygame.transform.flip(frame, True, False)
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime3_death_animation():
    sprite_sheet = pygame.image.load("slime/Slime3_Death_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

def load_slime3_attack_animation():
    sprite_sheet = pygame.image.load("slime/Slime3_Attack_full.png").convert_alpha()
    frames = []
    for i in range(6):  # 6 frames
        frame = sprite_sheet.subsurface((i * 64, 0, 64, 64))
        # Scale to 2x the hero size
        frame = pygame.transform.scale(frame, (128, 128))
        frames.append(frame)
    return frames

# Hero class
class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load animations
        self.idle_frames = load_hero_idle_animation()
        self.run_frames = load_hero_run_animation()
        self.jump_frames = load_hero_jump_animation()
        self.attack_frames = load_hero_attack_animation()
        self.death_frames = load_hero_death_animation()  # Load death animation
        
        # Initial state
        self.current_frame = 0
        self.animation_cooldown = 80  # milliseconds (faster animation)
        self.last_update = pygame.time.get_ticks()
        self.state = "idle"  # idle, run, jump, attack, death
        self.frames = self.idle_frames
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        
        # Position and movement
        self.rect.x = 100  # Fixed position on screen
        self.rect.bottom = SCREEN_HEIGHT - 130  # Adjusted ground level - moved slightly down
        self.vel_y = 0
        self.jumping = False
        self.on_ground = True
        self.moving_right = False  # Track if hero is moving right
        self.speed = 3  # Movement speed
        
        # Game stats
        self.score = 0
        self.alive = True
        self.death_animation_complete = False
        self.death_frame = 0
    # made by BlezecoN
    def update(self):
        if not self.alive:
            # Play death animation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                if self.death_frame < len(self.death_frames) - 1:
                    self.death_frame += 1
                    self.image = self.death_frames[self.death_frame]
                    self.last_update = current_time
                else:
                    self.death_animation_complete = True
            return
            
        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = current_time
        
        # Apply gravity
        self.vel_y += 0.8
        if self.vel_y > 10:
            self.vel_y = 10
        
        # Update vertical position
        self.rect.y += self.vel_y
        
        # Check if on ground
        if self.rect.bottom >= SCREEN_HEIGHT - 130:  # Same adjusted ground level
            self.rect.bottom = SCREEN_HEIGHT - 130
            self.vel_y = 0
            self.on_ground = True
            self.jumping = False
            if self.state == "jump":
                if self.moving_right:
                    self.change_state("run")
                else:
                    self.change_state("idle")
    
    def jump(self):
        if self.on_ground and not self.jumping and self.alive:
            self.vel_y = -10  # Jump height
            self.jumping = True
            self.on_ground = False
            self.change_state("jump")
            # Play jump sound (will be passed from main)
    
    def run(self):
        if not self.jumping and self.state != "run" and self.alive:
            self.change_state("run")
        self.moving_right = True
    
    def idle(self):
        if not self.jumping and self.state != "idle" and self.alive:
            self.change_state("idle")
        self.moving_right = False
    
    def attack(self):
        if not self.jumping and self.state != "attack" and self.alive:
            self.change_state("attack")
    
    def die(self):
        if self.alive:
            self.alive = False
            self.death_frame = 0
            self.image = self.death_frames[self.death_frame]
            self.vel_y = 0  # Stop vertical movement during death animation
            # Play hit sound (will be passed from main)
    
    def change_state(self, new_state):
        self.state = new_state
        self.current_frame = 0
        
        if new_state == "idle":
            self.frames = self.idle_frames
        elif new_state == "run":
            self.frames = self.run_frames
        elif new_state == "jump":
            self.frames = self.jump_frames
        elif new_state == "attack":
            self.frames = self.attack_frames
        
        self.image = self.frames[self.current_frame]
# made by BlezecoN
# Slime class
class Slime(pygame.sprite.Sprite):
    def __init__(self, slime_type, x_pos):
        super().__init__()
        self.slime_type = slime_type
        
        # Load animations based on slime type
        if slime_type == 1:
            self.idle_frames = load_slime1_idle_animation()
            self.walk_left_frames = load_slime1_walk_left_animation()
            self.walk_right_frames = load_slime1_walk_right_animation()
            self.death_frames = load_slime1_death_animation()
            self.attack_frames = load_slime1_attack_animation()
        elif slime_type == 2:
            self.idle_frames = load_slime2_idle_animation()
            self.walk_left_frames = load_slime2_walk_left_animation()
            self.walk_right_frames = load_slime2_walk_right_animation()
            self.death_frames = load_slime2_death_animation()
            self.attack_frames = load_slime2_attack_animation()
        else:  # slime_type == 3
            self.idle_frames = load_slime3_idle_animation()
            self.walk_left_frames = load_slime3_walk_left_animation()
            self.walk_right_frames = load_slime3_walk_right_animation()
            self.death_frames = load_slime3_death_animation()
            self.attack_frames = load_slime3_attack_animation()
        
        # Initial state
        self.current_frame = 0
        self.animation_cooldown = 120  # milliseconds
        self.last_update = pygame.time.get_ticks()
        self.state = "idle"  # idle, walk_left, walk_right, death, attack
        self.frames = self.idle_frames
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        
        # Position - adjust y position to account for larger size
        self.rect.x = x_pos
        self.rect.bottom = SCREEN_HEIGHT - 85  # Match hero's ground level
        
        # Movement
        self.direction = random.choice(["left", "right", "idle"])
        self.move_timer = random.randint(30, 120)  # Frames before changing direction
        self.speed = random.randint(1, 3)
        
        # State
        self.dying = False
        self.dead = False
        self.death_frame = 0
        self.sound_played = False  # Track if death sound has been played
    
    def update(self):
        if self.dying:
            # Play death animation
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                self.death_frame += 1
                if self.death_frame >= len(self.death_frames):
                    self.dead = True
                    self.kill()
                else:
                    self.image = self.death_frames[self.death_frame]
                    self.last_update = current_time
            return
        
        # Update animation frame
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.last_update = current_time
        
        # Movement logic
        self.move_timer -= 1
        if self.move_timer <= 0:
            # Change direction
            self.direction = random.choice(["left", "right", "idle"])
            self.move_timer = random.randint(30, 120)
            self.change_state(self.direction)
        
        # Move based on direction
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
                self.direction = "right"
                self.change_state("right")
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
                self.direction = "left"
                self.change_state("left")
    # made by BlezecoN
    def change_state(self, new_direction):
        if new_direction == "left":
            self.frames = self.walk_left_frames
            self.state = "walk_left"
        elif new_direction == "right":
            self.frames = self.walk_right_frames
            self.state = "walk_right"
        else:  # idle
            self.frames = self.idle_frames
            self.state = "idle"
        
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
    
    def die(self):
        if not self.dying:
            self.dying = True
            self.death_frame = 0
            self.image = self.death_frames[self.death_frame]
            return self.slime_type * 10  # Score based on slime type
        return 0  # Return 0 if already dying
# made by BlezecoN
# Game class
class Game:
    def __init__(self):
        self.hero = Hero()
        self.all_sprites = pygame.sprite.Group()
        self.slimes = pygame.sprite.Group()
        self.all_sprites.add(self.hero)
        
        # Game state
        self.score = 0
        self.game_over = False
        self.game_over_sound_played = False
        
        # Background scrolling
        self.bg_scroll = 0
        self.cloud_scroll = 0
        self.hills_scroll = 0
        self.tree_scroll = 0
        self.tree2_scroll = 0
        self.bush_scroll = 0
        self.ground_scroll = 0
        self.support_scroll = 0
        
        # Pre-render background layers for better performance
        self.sky_layer = sky_image
        
        self.cloud_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.cloud_layer.blit(cloud_image, (0, 0))
        self.cloud_layer.blit(cloud_image, (SCREEN_WIDTH, 0))
        
        self.hills_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.hills_layer.blit(hills_image, (0, 0))
        self.hills_layer.blit(hills_image, (SCREEN_WIDTH, 0))
        
        self.support_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.support_layer.blit(support_image, (0, 0))
        self.support_layer.blit(support_image, (SCREEN_WIDTH, 0))
        
        self.tree_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.tree_layer.blit(tree_image, (0, 0))
        self.tree_layer.blit(tree_image, (SCREEN_WIDTH, 0))
        
        self.tree2_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.tree2_layer.blit(tree2_image, (0, 0))
        self.tree2_layer.blit(tree2_image, (SCREEN_WIDTH, 0))
        
        self.bush_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.bush_layer.blit(bush_image, (0, 0))
        self.bush_layer.blit(bush_image, (SCREEN_WIDTH, 0))
        
        self.ground_layer = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.ground_layer.blit(ground_image, (0, 0))
        self.ground_layer.blit(ground_image, (SCREEN_WIDTH, 0))
        
        # Spawn initial slimes
        self.spawn_slimes(5)
    
    def spawn_slimes(self, count):
        for _ in range(count):
            slime_type = random.randint(1, 3)
            x_pos = random.randint(300, SCREEN_WIDTH * 2)
            slime = Slime(slime_type, x_pos)
            self.slimes.add(slime)
            self.all_sprites.add(slime)
   # made by BlezecoN 
    def update(self):
        if self.game_over:
            # Play game over sound once
            if not self.game_over_sound_played:
                # Will be played from main
                self.game_over_sound_played = True
            return
        
        # Update all sprites
        self.all_sprites.update()
        
        # If hero death animation is complete, show game over
        if not self.hero.alive and self.hero.death_animation_complete:
            self.game_over = True
        
        # Track if hero successfully jumped on any slime this frame
        jumped_on_slime = False
      # made by BlezecoN  
        # Check for collisions between hero and slimes
        slime_hits = pygame.sprite.spritecollide(self.hero, self.slimes, False, pygame.sprite.collide_mask)
        for slime in slime_hits:
            # If hero is jumping and above the slime's center, kill the slime
            if self.hero.vel_y > 0 and self.hero.rect.bottom < slime.rect.top + 80:  # Adjusted collision point for higher hero
                score = slime.die()
                if score is not None:  # Check if score is not None
                    self.score += score
                    # Play coin sound when defeating a slime (will be called from main)
                # Mark that we successfully jumped on a slime
                jumped_on_slime = True
            # If hero collides with slime from the side or below and slime is not dying
            elif not slime.dying and self.hero.alive and not jumped_on_slime:
                # Hero dies
                self.hero.die()
                # Play hit sound (will be called from main)
        
        # Apply bounce only once if we jumped on any slime
        if jumped_on_slime:
            # Add a small bounce when defeating a slime
            self.hero.vel_y = -8  # Moderate bounce effect
        
        # Scroll the world when hero is running or moving right while jumping
        if (self.hero.state == "run" or self.hero.moving_right) and self.hero.alive:
            # Use hero's speed for consistent scrolling
            scroll_speed = self.hero.speed
            
            # Update background scroll positions at different speeds for parallax effect
            # All speeds are relative to scroll speed
            self.cloud_scroll = (self.cloud_scroll + scroll_speed * 0.2) % SCREEN_WIDTH
            self.hills_scroll = (self.hills_scroll + scroll_speed * 0.4) % SCREEN_WIDTH
            self.support_scroll = (self.support_scroll + scroll_speed * 0.5) % SCREEN_WIDTH
            self.tree_scroll = (self.tree_scroll + scroll_speed * 0.6) % SCREEN_WIDTH
            self.tree2_scroll = (self.tree2_scroll + scroll_speed * 0.6) % SCREEN_WIDTH
            self.bush_scroll = (self.bush_scroll + scroll_speed * 0.8) % SCREEN_WIDTH
            self.ground_scroll = (self.ground_scroll + scroll_speed) % SCREEN_WIDTH
            
            # Move slimes left at scroll speed
            for slime in self.slimes:
                slime.rect.x -= scroll_speed
        # made by BlezecoN
        # Spawn new slimes if needed
        if len(self.slimes) < 5:
            self.spawn_slimes(1)
    
    def draw(self, screen):
        # Draw background layers with parallax scrolling
        screen.blit(self.sky_layer, (0, 0))
        
        # Draw clouds with scrolling
        screen.blit(self.cloud_layer, (-self.cloud_scroll, 0))
        
        # Draw hills with scrolling
        screen.blit(self.hills_layer, (-self.hills_scroll, 0))
        
        # Draw support with scrolling
        screen.blit(self.support_layer, (-self.support_scroll, 0))
        
        # Draw trees with scrolling
        screen.blit(self.tree_layer, (-self.tree_scroll, 0))
        screen.blit(self.tree2_layer, (-self.tree2_scroll, 0))
        
        # Draw bushes with scrolling
        screen.blit(self.bush_layer, (-self.bush_scroll, 0))
        
        # Draw ground with scrolling
        screen.blit(self.ground_layer, (-self.ground_scroll, 0))
        
        # Draw all sprites
        self.all_sprites.draw(screen)
        # made by BlezecoN
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        
        # Draw music status
        if pygame.mixer.music.get_busy():
            music_text = font.render("Music: ON (Press M to toggle)", True, WHITE)
        else:
            music_text = font.render("Music: OFF (Press M to toggle)", True, WHITE)
        screen.blit(music_text, (10, 40))
        
        # Draw sound controls
        sound_text = font.render("Sound FX: ON", True, WHITE)
        screen.blit(sound_text, (10, 70))
        
        # Draw game over message if game is over
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 15))
            restart_text = font.render("Press R to restart", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30))
    
    def reset(self):
        self.__init__()
        # Reset game over sound played flag
        self.game_over_sound_played = False
# made by BlezecoN
# Main game loop
def main():
    game = Game()
    running = True
    
    # Load and play background music
    if load_bgm("retro.mp3"):  # Use the retro.mp3 file you added
        set_volume(0.15)  # Set volume to 15% (decreased from 30%)
        play_bgm()  # Start playing the music
    
    # Generate retro sound effects
    jump_sound = generate_retro_jump_sound()
    coin_sound = generate_retro_coin_sound()
    hit_sound = generate_retro_hit_sound()
    game_over_sound = generate_retro_game_over_sound()
    
    # Set sound volumes
    jump_sound.set_volume(0.3)
    coin_sound.set_volume(0.2)  # Reduced volume for coin sound
    hit_sound.set_volume(0.3)
    game_over_sound.set_volume(0.4)
 # made by BlezecoN   
    # For FPS calculation
    fps_font = pygame.font.SysFont('Arial', 20)
    fps_timer = 0
    fps_count = 0
    fps_display = 0
    
    while running:
        # Start frame timing
        frame_start = pygame.time.get_ticks()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    stop_bgm()  # Stop the music before exiting
                    exit()
                if event.key == K_r and game.game_over:
                    game.reset()
                if (event.key == K_SPACE or event.key == K_w) and not game.game_over and game.hero.alive:
                    game.hero.jump()
                    jump_sound.play()  # Play jump sound
                # Music controls
                if event.key == K_m:  # Toggle music on/off
                    if pygame.mixer.music.get_busy():
                        stop_bgm()
                    else:
                        play_bgm()
    # made by BlezecoN    
        # Get key states
        keys = pygame.key.get_pressed()
        
        if not game.game_over and game.hero.alive:
            if keys[K_d]:
                game.hero.run()
            else:
                game.hero.idle()
        
        # Update game state
        game.update()
        
        # Play sound effects based on game state
        if game.game_over and not game.game_over_sound_played:
            game_over_sound.play()
            game.game_over_sound_played = True
        
        # Check for slime hits to play sounds
        for slime in game.slimes:
            if slime.dying and slime.death_frame == 0:  # Just started dying
                coin_sound.play()
        
        # Check for hero death to play sound
        if not game.hero.alive and game.hero.death_frame == 0:  # Just died
            hit_sound.play()
        
        # Draw everything
        game.draw(screen)
        
        # Calculate and display FPS
        fps_count += 1
        fps_timer += pygame.time.get_ticks() - frame_start
        if fps_timer >= 1000:  # Update FPS display every second
            fps_display = fps_count
            fps_count = 0
            fps_timer = 0
        
        fps_text = fps_font.render(f"FPS: {fps_display}", True, WHITE)
        screen.blit(fps_text, (10, 10))
        
        # Update the display
        pygame.display.flip()
   # made by BlezecoN     
        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
# made by BlezecoN