import sounddevice as sd
import numpy as np
import wavio
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
    monitor='testMonitor', color=[1, 1, 1], colorSpace='rgb',  # White background
    blendMode='avg', useFBO=True, 
    units='height')

# Debounce function to avoid multiple clicks being registered too fast
def debounce_click(mouse, wait_time=0.5):
    core.wait(wait_time)  # Wait for specified time in seconds
    while mouse.getPressed()[0]:  # Wait until the mouse button is released
        pass

# Function to show demographic survey
def show_demographic_survey():
    # Age input
    ageText = visual.TextStim(win=win, text="1. Enter your age:", font='Arial', pos=(-0.4, 0.3), height=0.03, color='black')
    ageInput = visual.TextStim(win=win, text="|", font='Arial', pos=(0.3, 0.3), height=0.03, color='black')

    # Gender identity MCQ
    genderText = visual.TextStim(win=win, text="2. Which gender identity do you most identify with?", font='Arial', pos=(-0.4, 0.1), height=0.03, color='black')
    genderOptions = ["Male", "Female", "Non-binary", "Prefer not to say"]
    genderButtons = []
    for i, option in enumerate(genderOptions):
        genderButtons.append({
            'button': visual.Circle(win, radius=0.03, pos=(-0.2 + i * 0.3, -0.1), lineColor='black'),
            'text': visual.TextStim(win=win, text=option, pos=(-0.2 + i * 0.3, -0.15), height=0.03, color='black'),
            'selected': False
        })

    # Other MCQs can follow similarly
    question3Text = visual.TextStim(win=win, text="3. How often do you experience emotional changes?", font='Arial', pos=(-0.4, -0.3), height=0.03, color='black')
    question3Options = ["Rarely", "Sometimes", "Often", "Always"]
    question3Buttons = []
    for i, option in enumerate(question3Options):
        question3Buttons.append({
            'button': visual.Circle(win, radius=0.03, pos=(-0.2 + i * 0.3, -0.4), lineColor='black'),
            'text': visual.TextStim(win=win, text=option, pos=(-0.2 + i * 0.3, -0.45), height=0.03, color='black'),
            'selected': False
        })

    # Continue button to submit demographic info
    submitButton = visual.Rect(win, width=0.3, height=0.1, fillColor='green', pos=(0, -0.6))
    submitButtonText = visual.TextStim(win=win, text="Submit", pos=(0, -0.6), height=0.05, color='white')

    age = ""
    gender = None
    question3 = None
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Draw the elements on the screen
        ageText.draw()
        ageInput.setText(f"{age}|")
        ageInput.draw()

        genderText.draw()
        for button in genderButtons:
            button['button'].draw()
            button['text'].draw()
            if button['selected']:
                visual.Circle(win, radius=0.025, pos=button['button'].pos, fillColor='blue').draw()

        question3Text.draw()
        for button in question3Buttons:
            button['button'].draw()
            button['text'].draw()
            if button['selected']:
                visual.Circle(win, radius=0.025, pos=button['button'].pos, fillColor='blue').draw()

        submitButton.draw()
        submitButtonText.draw()
        win.flip()

        # Handle typing for age input
        keys = event.getKeys()
        for key in keys:
            if key in '0123456789' and len(age) < 2:  # Max 2 digits for age
                age += key
            elif key == 'backspace' and len(age) > 0:
                age = age[:-1]

        # Handle mouse input for gender selection
        for button in genderButtons:
            if mouse.isPressedIn(button['button']):
                gender = button['text'].text
                for b in genderButtons:
                    b['selected'] = False
                button['selected'] = True

        # Handle mouse input for question 3 selection
        for button in question3Buttons:
            if mouse.isPressedIn(button['button']):
                question3 = button['text'].text
                for b in question3Buttons:
                    b['selected'] = False
                button['selected'] = True

        # Submit button
        if mouse.isPressedIn(submitButton) and len(age) > 0 and gender is not None and question3 is not None:
            debounce_click(mouse)  # Debounce to avoid multiple fast clicks
            break

    return age, gender, question3

# Function to show a page with text and a continue button
def show_intro_page(text):
    introText = visual.TextStim(win=win, text=text, font='Arial', pos=(0, 0), height=0.04, wrapWidth=1.18, color='black')
    continueButton = visual.Rect(win, width=0.3, height=0.1, fillColor='green', pos=(0, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0, -0.4), height=0.05, color='white')

    mouse = event.Mouse(visible=True, win=win)
    while True:
        introText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)  # Debounce to avoid multiple fast clicks
            break

# Function to play stimuli and track play count and reaction time
def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)
    reaction_clock = core.Clock()
    
    progress = f"Audio : {audio_index+1}/{len(audioStimuli)} : {round((audio_index + 1) / len(audioStimuli) * 100, 1)}% done"
    progressText = visual.TextStim(win=win, text=progress, pos=(0, 0.4), height=0.05, color='black')

    playButton = visual.Rect(win, width=0.3, height=0.2, fillColor='grey', pos=(0, 0))
    playButtonText = visual.TextStim(win=win, text='Play', pos=(0, 0), height=0.05)

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

# Function to display the scrollable welcome screen
def display_welcome():
    scroll_position = 0
    mouse = event.Mouse(visible=True, win=win)

    while True:
        welcomeText = visual.TextStim(win=win, text="""Welcome to the study...""", font='Arial', pos=(0, scroll_position), height=0.04, wrapWidth=1.18, color='black')
        continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0.7, -0.4))
        continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

        welcomeText.setPos((0, scroll_position))
        welcomeText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.05

        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)
            break

# CSV setup and demographic collection
participant_data = []
csv_file = 'experiment_data.csv'
file_exists = os.path.isfile(csv_file)
participant_id = str(uuid.uuid4())
session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

participant_data = [participant_id, session_start_time]

# Show introduction, consent, instructions
display_welcome()
show_intro_page("Now you will fill in a short demographic survey.")
age, gender, question3 = show_demographic_survey()
participant_data.extend([age, gender, question3])

# Continue to perception test intro
show_intro_page("Next, you will listen to audio files and rate them based on your perception of the speaker's emotion.")

# Audio stimuli loop
audioStimuli = ['audio_1.wav', 'audio_2.wav']
for i, audio_file in enumerate(audioStimuli):
    playCount, _ = present_stimulus(audio_file, i)
    valenceRating = 3  # Replace with actual valence rating code
    arousalRating = 3  # Replace with actual arousal rating code
    participant_data.extend([audio_file, valenceRating, arousalRating, playCount])

# Store all collected data in CSV
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    if not file_exists:
        header = ['Participant ID', 'Session Start Time', 'Age', 'Gender', 'Q3']
        for i in range(len(audioStimuli)):
            header += [f'Stimuli Name {i+1}', f'Valence {i+1}', f'Arousal {i+1}', f'Play Count {i+1}']
        writer.writerow(header)
    writer.writerow(participant_data)

win.close()
core.quit()
