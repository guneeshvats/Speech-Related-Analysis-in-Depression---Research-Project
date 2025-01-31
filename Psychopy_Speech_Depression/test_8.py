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

# Initialize components for Welcome Screen
welcomeText = visual.TextStim(win=win, name='welcomeText',
    text="""Welcome\n\nWe appreciate your participation in our study. This study is conducted by the research team of Cognitive Science Lab and Speech Processing Lab, International Institute of Information Technology, Hyderabad. It aims to understand Speech Emotion Perception and Production in young adults.

There are going to be 5 different tasks & a demographic survey involved in the whole study. Each test is different in nature and hence the duration. You will be informed about the details as you proceed. The total time duration of the whole study will be 40-45 minutes.

Your participation is entirely anonymous. No personal identifying information will be associated with the data we collect from you. Anybody who is 18-25 years old and can understand and/or speak English is eligible to participate in this study.

If you have any questions, you may ask us at any moment throughout the survey or thereafter. You can also email us if you have any questions regarding this study:

Research Student:
guneesh.vats@research.iiit.ac.in

Professors:
priyanka.srivastava@iiit.ac.in and chiranjeevi.yarra@iiit.ac.in

If you would like to know more, please proceed by clicking the 'Continue' button below.""",
    font='Arial', pos=(0, 0), height=0.04, wrapWidth=1.18, 
    color='black', colorSpace='rgb', opacity=1, languageStyle='LTR')

# 'Continue' button for welcome page (positioned on the right side)
continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0.7, -0.4))
continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

# Initialize progress bar
progressText = visual.TextStim(win=win, text='', pos=(0, 0.4), height=0.05, color='black')

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
    samValenceButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='black', fillColor=None))
    samArousalButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='black', fillColor=None))

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

# Function to display the consent form (positioned button on the right)
def display_consent_form():
    consentText = visual.TextStim(win=win, text=
    """
    Consent Form\n\n
    I hereby give my consent and permit members of the research team to access a de-identified version (with no mention of my name) of the data. The clinical information related to me will be used only for research purposes.\n\n
    I understand I will not be identified or identifiable in the report or reports that result from the research.\n\n
    I understand anonymized data can be shared in the public domain with other researchers worldwide.\n\n
    I have read the general information about the study and I have asked any questions regarding the procedure which have been satisfactorily answered. \n\n
    I am older than 18 years of age and no older than the age of 25.\n\n
    I understand the type of data being collected in this study and the reason for its collection. \n\n
    We hope you have read the general information. If you agree to all of the above,  click on 'I Accept'  button to participate.
    """, 
    font='Arial', pos=(0, 0), height=0.04, wrapWidth=1.18, 
    color='black', colorSpace='rgb', opacity=1, languageStyle='LTR')
    

    acceptButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0.7, -0.4))  # Button moved to the right
    acceptButtonText = visual.TextStim(win=win, text="I Accept", pos=(0.7, -0.4), height=0.04, color='white')

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

# Function to display instructions (positioned button on the right)
# Function to display instructions (positioned button on the right)
def display_instructions():
    instructionsText = visual.TextStim(win=win, text="""
    Details about the study\n\n
    Let me walk you through the process. Also, please read the given FAQ carefully.\n\n
    The study will last for around 40-45 minutes and consists of 5 tasks:\n\n
    - Survey about your demographic information\n
    - Language Fluency Test\n
    - Current Mood Assessment\n
    - Speech Emotion Perception Test\n
    - Speech Production Test \n
    - General Health Questionnaire\n\n
    We will start the study with the Demographic information survey, followed by a Language fluency test and current mood assessment. Later in the survey, you will be asked to perceive the speaker's emotions from a series of audio files presented to you. Instructions about this task will be provided later. Finally, the study ends with a health survey to obtain general health measures. Each test is different in nature and hence the duration.\n\n
                        Frequently Asked Questions (FAQ)\n
    Q: What are the benefits of this research?\n
    A: You may not be directly benefited by participating in our study. However, your participation will potentially advance our understanding of the impact of psychological health on emotion perception.\n\n
    Q: What are the risks or inconveniences involved in this survey?\n
    A: This study involves listening to audio. There are no potential risks associated. You may feel fatigued or tired from prolonged exposure to sounds. We will keep the volume levels in the recommended range for your comfort. If you feel any discomfort, please inform us immediately.\n\n
    Q: How will my personal information be protected?\n
    A: Your participation is entirely anonymous. No personal identifying information will be associated with the data we collect from you. Rest assured that all your responses will be treated with the utmost discretion.\n\n
    Q: What are my participation rights?\n
    A: Your participation in this study is entirely voluntary. You can choose to withdraw from this study at any point in time. However, for the benefit of research, we request you complete the study.\n\n
    Q: Whom do I contact if I have questions about the survey?\n
    A: If you have any questions, you may ask us at any moment throughout the survey or thereafter. You can also email us if you have any questions regarding this study:\n
    Research Students: guneesh.vats@research.iiit.ac.in, karthikeya.k@students.iiit.ac.in, sriya.ravula@research.iiit.ac.in\n
    Professors: priyanka.srivastava@iiit.ac.in, chiranjeevi.yarra@iiit.ac.in.\n\n
    """, font='Arial', pos=(0, 0), height=0.04, wrapWidth=1.18, 
    color='black', colorSpace='rgb', opacity=1, languageStyle='LTR')

    understandButton = visual.Rect(win, width=0.3, height=0.07, fillColor='green', pos=(0.7, -0.4))  # Button moved to the right
    understandButtonText = visual.TextStim(win=win, text="I Understand", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = 0
    mouse = event.Mouse()

    while True:
        instructionsText.setPos((0, scroll_position))
        instructionsText.draw()
        understandButton.draw()
        understandButtonText.draw()
        win.flip()

        # Scroll the instructions text
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.1

        # Check for "I Understand" click
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
                visual.Circle(win, radius=0.025, pos=button.pos, fillColor='blue').draw()
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
    
    valenceRating, valenceRT = rate_sam(samValenceButtons, valence_images, visual.TextStim(win=win, text="How pleasant was the speaker's voice in the provided audio file? (Press enter to next):", pos=(0, 0.4), height=0.05, color='black'))
    arousalRating, arousalRT = rate_sam(samArousalButtons, arousal_images, visual.TextStim(win=win, text="How excited was the speaker's voice in the provided audio file? (Press enter to next):", pos=(0, 0.4), height=0.05, color='black'))

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
