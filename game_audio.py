import pygame
import os
import numpy as np

# Initialize pygame mixer
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

def load_bgm(filename):
    """
    Load a background music file
    """
    try:
        # Check if the audio folder exists, if not create it
        if not os.path.exists('audio'):
            os.makedirs('audio')
            print("Created audio directory. Please place your music files there.")
            return None
            
        # Full path to the audio file
        music_path = os.path.join('audio', filename)
        
        # Check if the file exists
        if not os.path.exists(music_path):
            print(f"Warning: {music_path} not found. Please add your music file.")
            return None
            
        # Load and return the music
        pygame.mixer.music.load(music_path)
        return True
    except Exception as e:
        print(f"Error loading music: {e}")
        return None

def play_bgm(loop=True):
    """
    Play the loaded background music
    """
    try:
        if loop:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        else:
            pygame.mixer.music.play()
    except Exception as e:
        print(f"Error playing music: {e}")

def stop_bgm():
    """
    Stop the background music
    """
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"Error stopping music: {e}")

def pause_bgm():
    """
    Pause the background music
    """
    try:
        pygame.mixer.music.pause()
    except Exception as e:
        print(f"Error pausing music: {e}")

def unpause_bgm():
    """
    Unpause the background music
    """
    try:
        pygame.mixer.music.unpause()
    except Exception as e:
        print(f"Error unpausing music: {e}")

def set_volume(volume):
    """
    Set the volume of the background music
    Volume should be between 0.0 and 1.0
    """
    try:
        pygame.mixer.music.set_volume(max(0.0, min(volume, 1.0)))
    except Exception as e:
        print(f"Error setting volume: {e}")

def load_sound_effect(filename):
    """
    Load a sound effect
    """
    try:
        # Check if the audio folder exists
        if not os.path.exists('audio'):
            os.makedirs('audio')
            print("Created audio directory. Please place your sound files there.")
            return None
            
        # Full path to the audio file
        sound_path = os.path.join('audio', filename)
        
        # Check if the file exists
        if not os.path.exists(sound_path):
            print(f"Warning: {sound_path} not found. Please add your sound file.")
            return None
            
        # Load and return the sound
        sound = pygame.mixer.Sound(sound_path)
        return sound
    except Exception as e:
        print(f"Error loading sound effect: {e}")
        return None

# Retro sound generation functions
def generate_retro_jump_sound():
    """Generate a classic 8-bit jump sound effect"""
    sample_rate = 44100
    duration = 0.3  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a frequency sweep from high to low
    freq_start = 800
    freq_end = 400
    freq = np.linspace(freq_start, freq_end, int(sample_rate * duration))
    
    # Generate the tone with decreasing amplitude
    tone = np.sin(2 * np.pi * freq * t) * np.exp(-5 * t)
    
    # Convert to 16-bit data
    audio = np.array(tone * 32767, dtype=np.int16)
    
    # Make it stereo
    audio = np.column_stack((audio, audio))
    
    # Convert to PyGame sound
    sound = pygame.sndarray.make_sound(audio)
    return sound

def generate_retro_coin_sound():
    """Generate a softer classic 8-bit coin collection sound"""
    sample_rate = 44100
    duration = 0.15  # slightly longer duration
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create two tones with gentler frequencies
    freq1 = 700  # Lower frequency (was 900)
    freq2 = 900  # Lower frequency (was 1200)
    
    # Generate the tones with smoother transition
    mid_point = len(t) // 2
    # Apply fade in/out envelope
    envelope1 = np.linspace(0, 1, mid_point) * np.exp(-3 * np.linspace(0, 1, mid_point))
    envelope2 = np.linspace(1, 0, len(t) - mid_point) * np.exp(-3 * np.linspace(0, 1, len(t) - mid_point))
    
    tone1 = np.sin(2 * np.pi * freq1 * t[:mid_point]) * envelope1
    tone2 = np.sin(2 * np.pi * freq2 * t[mid_point:]) * envelope2
    
    # Combine tones
    tone = np.concatenate([tone1, tone2])
    
    # Reduce volume significantly
    tone = tone * 0.3  # 30% of original volume
    
    # Convert to 16-bit data
    audio = np.array(tone * 32767, dtype=np.int16)
    
    # Make it stereo
    audio = np.column_stack((audio, audio))
    
    # Convert to PyGame sound
    sound = pygame.sndarray.make_sound(audio)
    return sound

def generate_retro_hit_sound():
    """Generate a classic 8-bit hit/damage sound"""
    sample_rate = 44100
    duration = 0.2  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a noise-based sound with decreasing frequency
    freq_start = 300
    freq_end = 50
    freq = np.linspace(freq_start, freq_end, int(sample_rate * duration))
    
    # Generate the tone with noise
    tone = np.sin(2 * np.pi * freq * t) * np.exp(-10 * t)
    noise = np.random.uniform(-0.5, 0.5, len(tone))
    combined = tone + noise * 0.3
    
    # Normalize and convert to 16-bit data
    combined = combined / np.max(np.abs(combined))
    audio = np.array(combined * 32767, dtype=np.int16)
    
    # Make it stereo
    audio = np.column_stack((audio, audio))
    
    # Convert to PyGame sound
    sound = pygame.sndarray.make_sound(audio)
    return sound

def generate_retro_game_over_sound():
    """Generate a classic 8-bit game over sound"""
    sample_rate = 44100
    duration = 1.0  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a descending series of tones
    freqs = [400, 300, 200, 100]
    tones = []
    
    segment_duration = duration / len(freqs)
    segment_samples = int(sample_rate * segment_duration)
    
    for i, freq in enumerate(freqs):
        segment_t = t[i*segment_samples:(i+1)*segment_samples]
        tone = np.sin(2 * np.pi * freq * segment_t) * 0.8
        tones.append(tone)
    
    # Combine all segments
    combined = np.concatenate(tones)
    
    # Apply a decay envelope
    envelope = np.exp(-2 * t)
    combined = combined * envelope
    
    # Convert to 16-bit data
    audio = np.array(combined * 32767, dtype=np.int16)
    
    # Make it stereo
    audio = np.column_stack((audio, audio))
    
    # Convert to PyGame sound
    sound = pygame.sndarray.make_sound(audio)
    return sound
