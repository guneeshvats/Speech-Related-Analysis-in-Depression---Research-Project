from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame']  # Use pygame for audio

from psychopy import visual, core, event, sound, data, gui, clock
import os
import csv
import uuid  # To generate unique participant ID
from datetime import datetime  # To add date and time

# Setup the Window
win = visual.Window(
    size=[1280, 720], fullscr=False, screen=0, 
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[0.5, 0.5, 0.5], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')

# Initialize components for Welcome Screen
welcomeText = visual.TextStim(win=win, name='welcomeText',
    text="""Welcome\n\nWe appreciate your participation in our study. This study is conducted by the research team of Cognitive Science Lab and Speech Processing Lab, International Institute of Information Technology, Hyderabad. It aims to understand Speech Emotion Perception in young adults.

There are going to be 4 different tasks & a demographic survey involved in the whole study. Each test is different in nature and hence the duration. You will be informed about the details as you proceed. The total time duration of the whole study will be 35-40 minutes.

Your participation is entirely anonymous. No personal identifying information will be associated with the data we collect from you. Anybody who is 18-25 years old and can understand and/or speak English is eligible to participate in this study.

If you have any questions, you may ask us at any moment throughout the survey or thereafter. You can also email us if you have any questions regarding this study:

Research Students:
guneesh.vats@research.iiit.ac.in, karthikeya.k@students.iiit.ac.in, and sriya.ravula@research.iiit.ac.in

Professors:
priyanka.srivastava@iiit.ac.in and chiranjeevi.yarra@iiit.ac.in

If you would like to know more, please proceed by clicking the 'Continue' button below.""",
    font='Arial', pos=(0, 0), height=0.04, wrapWidth=1.2, ori=0, 
    color='white', colorSpace='rgb', opacity=1, languageStyle='LTR')

# 'Continue' button
continueButton = visual.Rect(win, width=0.3, height=0.1, fillColor='green', pos=(0, -0.4))
continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0, -0.4), height=0.05)

# Initialize progress bar
progressText = visual.TextStim(win=win, text='', pos=(0, 0.4), height=0.05, color='white')

# Button for playing audio (global definition to avoid scope issues)
playButton = visual.Rect(win, width=0.3, height=0.2, fillColor='grey', pos=(0, 0))
playButtonText = visual.TextStim(win=win, text='Play', pos=(0, 0), height=0.05)

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
    samValenceButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))
    samArousalButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='white', fillColor=None))

# Function to display the scrollable welcome screen
def display_welcome():
    scroll_position = 0
    mouse = event.Mouse(visible=True, win=win)

    while True:
        welcomeText.setPos((0, scroll_position))
        welcomeText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.05

        if mouse.isPressedIn(continueButton):
            break

# Function to display the consent form
def display_consent_form():
    consentText = visual.TextStim(win=win, text="""Consent Form\n\nYou are invited to participate in a research study.\n\nPurpose: The purpose of this study is to understand human perception and behavior in response to various stimuli.\n\nVoluntary Participation: Your participation is completely voluntary, and you can withdraw at any time without any consequences.\n\nConfidentiality: Your responses will be kept confidential and will not be associated with your personal identity.\n\nBy clicking 'I Accept', you consent to participate in the study.""", pos=(0, 0.3), height=0.03, wrapWidth=1.5)

    acceptButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0, -0.4))
    acceptButtonText = visual.TextStim(win=win, text="I Accept", pos=(0, -0.4), height=0.04)

    scroll_position = 0
    mouse = event.Mouse()

    while True:
        consentText.setPos((0, scroll_position))
        consentText.draw()
        acceptButton.draw()
        acceptButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.1

        if mouse.isPressedIn(acceptButton):
            break

# Function to display instructions
def display_instructions():
    instructionsText = visual.TextStim(win=win, text="""Instructions\n\n1. During this experiment, you will be asked to listen to audio stimuli and provide your ratings based on your perception of the stimuli.\n\n2. Please ensure that you are in a quiet environment to avoid any distractions.\n\n3. If you have any questions or concerns, please contact the experimenter.""", pos=(0, 0.3), height=0.03, wrapWidth=1.5)
    
    understandButton = visual.Rect(win, width=0.3, height=0.07, fillColor='green', pos=(0, -0.4))
    understandButtonText = visual.TextStim(win=win, text="I Understand", pos=(0, -0.4), height=0.04)

    scroll_position = 0
    mouse = event.Mouse()

    while True:
        instructionsText.setPos((0, scroll_position))
        instructionsText.draw()
        understandButton.draw()
        understandButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.1

        if mouse.isPressedIn(understandButton):
            break

# Define rate_sam function for SAM scale rating
def rate_sam(buttons, images, text):
    mouse = event.Mouse(visible=True, win=win)
    selected = None
    reaction_clock = core.Clock()
    sam_images = [visual.ImageStim(win, image=image, pos=(button.pos[0], -0.1), size=(0.18, 0.23)) for button, image in zip(buttons, images)]

    reaction_clock.reset()

    while True:
        text.draw()
        for i, button in enumerate(buttons):
            sam_images[i].draw()
            button.draw()
            if selected == i:
                visual.Circle(win, radius=0.025, pos=button.pos, fillColor='white').draw()
        win.flip()

        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for i, button in enumerate(buttons):
                if button.contains(pos):
                    selected = i

        keys = event.getKeys(['return', 'escape'])
        if 'return' in keys and selected is not None:
            rt = reaction_clock.getTime()
            return selected + 1, rt
        elif 'escape' in keys:
            core.quit()

# Function to play stimuli and track play count and reaction time
def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)
    reaction_clock = core.Clock()
    
    progress = f"Audio : {audio_index+1}/{len(audioStimuli)} : {round((audio_index + 1) / len(audioStimuli) * 100, 1)}% done"
    progressText.setText(progress)

    while True:
        playButton.draw()
        playButtonText.draw()
        progressText.draw()
        win.flip()

        mouse = event.Mouse()
        if mouse.isPressedIn(playButton):
            stim.stop()
            stim.play()
            playCount += 1
            playButtonText.setText("Playing...")
            playButton.draw()
            playButtonText.draw()
            progressText.draw()
            win.flip()

            core.wait(stim.getDuration())

            playButtonText.setText("Play")
            playButton.draw()
            playButtonText.draw()
            progressText.draw()
            win.flip()

        keys = event.getKeys(['space'])
        if 'space' in keys:
            rt = reaction_clock.getTime()
            break
    
    return playCount, rt

# Stimuli loop setup
audioStimuli = ['audio_1.wav', 'audio_2.wav']

# CSV file setup
csv_file = 'experiment_data.csv'
file_exists = os.path.isfile(csv_file)

# Unique ID for participant
participant_id = str(uuid.uuid4())

# Add session start time
session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# The experiment begins here
display_welcome()
display_consent_form()
display_instructions()

# Prepare a list to store participant data for appending into one row
participant_data = [participant_id, session_start_time]

# Present each stimulus and gather ratings
for i, audio_file in enumerate(audioStimuli):
    playCount, _ = present_stimulus(audio_file, i)
    
    valenceRating, valenceRT = rate_sam(samValenceButtons, valence_images, visual.TextStim(win=win, text="Rate your Valence (Press enter to next):", pos=(0, 0.4), height=0.05))
    arousalRating, arousalRT = rate_sam(samArousalButtons, arousal_images, visual.TextStim(win=win, text="Rate your Arousal (Press enter to next):", pos=(0, 0.4), height=0.05))

    participant_data.append([audio_file, valenceRating, valenceRT, arousalRating, arousalRT, playCount])

# After collecting data for all stimuli, append to CSV in one row per participant
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    if not file_exists:
        header = ['Participant ID', 'Session Start Time']
        for i in range(len(audioStimuli)):
            header += [f'Stimuli Name {i+1}', f'Valence {i+1}', f'Valence RT {i+1}', 
                       f'Arousal {i+1}', f'Arousal RT {i+1}', f'Play Count {i+1}']
        writer.writerow(header)

    participant_data_row = [participant_id, session_start_time]
    for stimulus_data in participant_data[2:]:
        participant_data_row += stimulus_data
    writer.writerow(participant_data_row)

win.close()
core.quit()
