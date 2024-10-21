from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']  # Force pygame as the preferred audio library

from psychopy import visual, core, event, sound, gui, data, logging, clock
import random

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
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

# Instructions Screen
instructionText = visual.TextStim(win=win, name='instructionText',
    text='Please read the instructions carefully and press SPACE to proceed.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

# Consent Form
consentText = visual.TextStim(win=win, name='consentText',
    text='I consent to participate in this experiment.\n\nPress SPACE to continue.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

# Demographics Questions
demographicsText = visual.TextStim(win=win, name='demographicsText',
    text='Please answer the demographic questions.\n\nPress SPACE to proceed.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

# Stimuli loop setup
audioStimuli = ['audio1.wav', 'audio2.wav', ..., 'audio25.wav']  # Add your audio files here
valenceRatings = []
arousalRatings = []
reactionTimes = []
playCounts = []

# Rating scale text
valenceText = visual.TextStim(win=win, name='valenceText',
    text='Please rate your Valence on a scale from 1 to 5.\n\nPress the corresponding number key.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

arousalText = visual.TextStim(win=win, name='arousalText',
    text='Please rate your Arousal on a scale from 1 to 5.\n\nPress the corresponding number key.',
    font='Arial', pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR',
    depth=0.0)

# Function to display the welcome screen
def display_welcome():
    welcomeText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Function to display instructions
def display_instructions():
    instructionText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Function to display consent form
def display_consent():
    consentText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Function to display demographics
def display_demographics():
    demographicsText.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

# Function to play stimuli and track play count and reaction time
def present_stimulus(audio_file):
    playCount = 0
    # Initialize the sound component using pygame backend
    stim = sound.Sound(value=audio_file)  # pygame backend should handle this
    stim.play()
    playCount += 1
    clockRT = core.Clock()  # Reaction time clock
    while True:
        keys = event.getKeys(keyList=['space', 'r'])  # 'r' to replay audio, 'space' to continue
        if 'r' in keys:
            stim.play()
            playCount += 1
        elif 'space' in keys:
            rt = clockRT.getTime()
            break
    return playCount, rt

# Function to capture valence rating
def rate_valence():
    valenceText.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', '4', '5'])
    return int(keys[0])

# Function to capture arousal rating
def rate_arousal():
    arousalText.draw()
    win.flip()
    keys = event.waitKeys(keyList=['1', '2', '3', '4', '5'])
    return int(keys[0])

# The experiment begins here
display_welcome()
display_instructions()
display_consent()
display_demographics()

# Present each stimulus and gather ratings
for audio_file in audioStimuli:
    playCount, reactionTime = present_stimulus(audio_file)
    valenceRating = rate_valence()
    arousalRating = rate_arousal()
    
    # Store data for each stimulus
    valenceRatings.append(valenceRating)
    arousalRatings.append(arousalRating)
    reactionTimes.append(reactionTime)
    playCounts.append(playCount)

# Data output
thisExp = data.ExperimentHandler()
thisExp.addData('Valence Ratings', valenceRatings)
thisExp.addData('Arousal Ratings', arousalRatings)
thisExp.addData('Reaction Times', reactionTimes)
thisExp.addData('Play Counts', playCounts)
thisExp.saveAsWideText('experiment_data.csv')

# Close the window and cleanup
win.close()
core.quit()
