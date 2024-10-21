from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']  # Use pygame for audio

from psychopy import visual, core, event, sound, data, gui, clock
import os
import csv
import uuid  # To generate unique participant ID

# Setup the Window
win = visual.Window(
    size=[1280, 720], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0.5, 0.5, 0.5], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')

# Initialize components for Welcome Screen
welcomeText = visual.TextStim(win=win, name='welcomeText',
    text='Welcome to the experiment.\n\nPress SPACE to continue.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR')

# Initialize progress bar
#progressText = visual.TextStim(win=win, text='', pos=(0.75, 0.4), height=0.05, color='white')
progressText = visual.TextStim(win=win, text='', pos=(0, 0.4), height=0.05, color='white')  # Adjusted to center

# Button for playing audio
playButton = visual.Rect(win, width=0.3, height=0.2, fillColor='grey', pos=(0, 0))
playButtonText = visual.TextStim(win=win, text='Play', pos=(0, 0), height=0.05)  # Adjust the height to reduce text size
#playButtonText = visual.TextStim(win=win, text='Play', pos=(0, 0))

# SAM scale setup
samValenceButtons = []
samArousalButtons = []
button_radius = 0.03  # Adjusted button size for better visibility
button_spacing = 0.18  # Increased spacing for better alignment

# Set up valence and arousal buttons, and prepare images (SAM Scale Images)
valence_images = [f"sam_valence_{i}.jpg" for i in range(1, 6)]  
arousal_images = [f"sam_arousal_{i}.jpg" for i in range(1, 6)]

for i in range(1, 6):
    x_pos = -0.4 + (i - 1) * button_spacing
    samValenceButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))  # Buttons further below SAM scale
    samArousalButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))  # Buttons further below SAM scale

def rate_sam(buttons, images, text):
    mouse = event.Mouse(visible=True, win=win)
    selected = None
    reaction_clock = core.Clock()  # Track reaction time
    sam_images = [visual.ImageStim(win, image=image, pos=(button.pos[0], -0.1), size=(0.18, 0.23)) for button, image in zip(buttons, images)]
  
    reaction_clock.reset()  # Start the reaction time clock
    
    while True:
        text.draw()
        for i, button in enumerate(buttons):
            sam_images[i].draw()  # Display SAM image for each button
            button.draw()
            if selected == i:
                visual.Circle(win, radius=button_radius * 0.8, pos=button.pos, fillColor='white').draw()  # Highlight selected option
        win.flip()
        
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for i, button in enumerate(buttons):
                if button.contains(pos):
                    selected = i
        
        keys = event.getKeys(['return', 'escape'])
        if 'return' in keys and selected is not None:
            rt = reaction_clock.getTime()  # Capture reaction time when 'return' is pressed
            return selected + 1, rt  # Return rating and reaction time
        elif 'escape' in keys:
            core.quit()

# Stimuli loop setup
audioStimuli = ['audio_1.wav', 'audio_2.wav']  # Add your audio files here

# CSV file setup
csv_file = 'experiment_data.csv'
file_exists = os.path.isfile(csv_file)

# Function to display the welcome screen
def display_welcome():
    welcomeText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])


def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)
    reaction_clock = core.Clock()
    
    # Display progress
    progress = f"{round((audio_index + 1) / len(audioStimuli) * 100, 1)}% done"
    progressText.setText(progress)
    
    while True:
        # Draw play button and progress text
        playButton.draw()
        playButtonText.draw()
        progressText.draw()
        win.flip()

        # Check for play button click
        mouse = event.Mouse()
        if mouse.isPressedIn(playButton):
            # Play the sound and reset the clock
            stim.stop()  # Stop any previous playback if still playing
            stim.play()
            playCount += 1
            playButtonText.setText("Playing...")
            playButton.draw()
            playButtonText.draw()
            progressText.draw()
            win.flip()
            
            # Wait for the duration of the audio to finish
            core.wait(stim.getDuration())
            
            # Update button text after playback finishes
            playButtonText.setText("Play")
            playButton.draw()
            playButtonText.draw()
            progressText.draw()
            win.flip()

        # Check if the participant wants to continue by pressing space
        keys = event.getKeys(keyList=['space'])
        if 'space' in keys:
            rt = reaction_clock.getTime()  # Get reaction time when space is pressed
            break
    
    return playCount, rt


# Unique ID for participant
participant_id = str(uuid.uuid4())

# The experiment begins here
display_welcome()

# Prepare a list to store participant data for appending into one row
participant_data = [participant_id]  # Include the participant ID as the first element

# Present each stimulus and gather ratings
for i, audio_file in enumerate(audioStimuli):
    playCount, _ = present_stimulus(audio_file, i)
    
    # Rating valence and arousal using the SAM scale
    valenceRating, valenceRT = rate_sam(samValenceButtons, valence_images, visual.TextStim(win=win, text="Rate your Valence (Press enter to next):", pos=(0, 0.4), height=0.05))  # Text moved higher
    arousalRating, arousalRT = rate_sam(samArousalButtons, arousal_images, visual.TextStim(win=win, text="Rate your Arousal (Press enter to next):", pos=(0, 0.4), height=0.05))  # Text moved higher
    
    # Store the data for the current stimulus
    participant_data.append([audio_file, valenceRating, valenceRT, arousalRating, arousalRT, playCount])

# After collecting data for all stimuli, append to CSV in one row per participant
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        # Define the header for each stimulus
        header = ['Participant ID']
        for _ in audioStimuli:
            header += ['Stimuli Name', 'Valence', 'Valence RT', 'Arousal', 'Arousal RT', 'Play Count']
        writer.writerow(header)  # Write the header

    # Flatten the list of data for CSV writing
    flattened_data = [item for sublist in participant_data[1:] for item in sublist]  # Flatten the list of lists
    writer.writerow([participant_id] + flattened_data)  # Write the data

# Close the window and cleanup
win.close()
core.quit()
