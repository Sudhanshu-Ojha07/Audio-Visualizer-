import pygame
import numpy as np
import pyaudio
import glob
import os

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1680, 1050
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("AI Animation")

# Colors
BLACK = (0, 0, 0)

# Audio setup
p = pyaudio.PyAudio()
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
rate = 44100  # Record at 44100 samples per second

# Start Recording
stream = p.open(format=sample_format,
                channels=channels,
                rate=rate,
                frames_per_buffer=chunk,
                input=True)


def get_sound_intensity():
    data = stream.read(chunk)
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean()


# Function to load GIF frames from a specified directory
def load_frames_from_directory(directory_path):
    width, height = 1600, 900
  
    frames = []
    frame_paths = sorted(glob.glob(os.path.join(directory_path, "*.jpg")))
    for frame_path in frame_paths:
        image = pygame.image.load(frame_path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))  # Resize frame to window size
        frames.append(image)
    return frames

# Specify the directory containing the GIF frames
frames_directory = "/home/sudhanshu/Downloads/J.A.R.V.I.S"  # Change this to your directory path

# Load GIF frames
frames = load_frames_from_directory(frames_directory)
frame_count = len(frames)
current_frame = 0

# Sound threshold to detect if there is sound
sound_threshold = 100  # Adjust this threshold based on your sound environment

frame_delay = 15
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get sound intensity
    intensity = get_sound_intensity()

    # Update current frame based on sound intensity only if intensity is above the threshold
    if intensity > sound_threshold:
        frame_increment = int(intensity / (100 * frame_delay))
        current_frame = (current_frame + frame_increment) % frame_count


        # Clear screen
        screen.fill(BLACK)

        # Draw current frame
        screen.blit(frames[current_frame], (0, 0))

    else:
        # Clear screen when no sound is detected
        screen.fill(BLACK)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
