from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']  # Use pygame for audio

from psychopy import visual, core, event, sound, data, gui, clock
import os
import csv

# Setup the Window
win = visual.Window(
    size=[1280, 720], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0, 0, 0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')

# Initialize components for Welcome Screen
welcomeText = visual.TextStim(win=win, name='welcomeText',
    text='Welcome to the experiment.\n\nPress SPACE to continue.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR')

# Initialize progress bar
progressText = visual.TextStim(win=win, text='', pos=(0.75, 0.4), height=0.05, color='white')

# Button for playing audio
playButton = visual.Rect(win, width=0.2, height=0.1, fillColor='grey', pos=(0, 0))
playButtonText = visual.TextStim(win=win, text='Play', pos=(0, 0))

# SAM scale setup
samValenceButtons = []
samArousalButtons = []
button_radius = 0.03
button_spacing = 0.15

for i in range(1, 6):
    x_pos = -0.3 + (i - 1) * button_spacing
    samValenceButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))
    samArousalButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))

def rate_sam(buttons, text):
    mouse = event.Mouse(visible=True, win=win)
    selected = None
    while True:
        text.draw()
        for i, button in enumerate(buttons):
            button.draw()
            if selected == i:
                visual.Circle(win, radius=button_radius*0.8, pos=button.pos, fillColor='white').draw()
        win.flip()
        
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for i, button in enumerate(buttons):
                if button.contains(pos):
                    selected = i
        
        keys = event.getKeys(['return', 'escape'])
        if 'return' in keys and selected is not None:
            return selected + 1, 0  # Return rating from 1 to 9, ignore reaction time
        elif 'escape' in keys:
            core.quit()

# Stimuli loop setup
audioStimuli = ['audio_1.wav', 'audio_2.wav']  # Add your audio files here
valenceRatings = []
arousalRatings = []
reactionTimes = []
playCounts = []

# CSV file setup
csv_file = 'experiment_data.csv'
file_exists = os.path.isfile(csv_file)

# Function to display the welcome screen
def display_welcome():
    welcomeText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Function to play stimuli and track play count and reaction time
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
            stim.play()
            playCount += 1
            playButtonText.setText("Playing...")
            playButton.draw()
            win.flip()
            core.wait(stim.getDuration())
            playButtonText.setText("Play Again")
        # After playing, allow space to continue
        keys = event.getKeys(keyList=['space'])
        if 'space' in keys:
            rt = reaction_clock.getTime()
            break
    
    return playCount, rt

# The experiment begins here
display_welcome()

# Prepare a list to store participant data for appending into one row
participant_data = []

# Present each stimulus and gather ratings
for i, audio_file in enumerate(audioStimuli):
    playCount, reactionTime = present_stimulus(audio_file, i)
    
    # Rating valence and arousal using the SAM scale
    valenceRating, _ = rate_sam(samValenceButtons, visual.TextStim(win=win, text="Rate your Valence:", pos=(0, 0.4), height=0.05))
    arousalRating, _ = rate_sam(samArousalButtons, visual.TextStim(win=win, text="Rate your Arousal:", pos=(0, 0.4), height=0.05))
    
    # Store the data for the current stimulus
    participant_data.append([valenceRating, arousalRating, reactionTime, playCount])

# After collecting data for all stimuli, append to CSV in one row per participant
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(['Valence', 'Arousal', 'Reaction Time', 'Play Count'] * len(audioStimuli))  # Header
    flattened_data = [item for sublist in participant_data for item in sublist]  # Flatten the list of lists
    writer.writerow(flattened_data)

# Close the window and cleanup
win.close()
core.quit()
