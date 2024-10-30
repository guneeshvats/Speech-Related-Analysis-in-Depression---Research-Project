import sounddevice as sd
import numpy as np
import wavio
from psychopy import prefs, sound
prefs.hardware['audioLib'] = ['sounddevice']
sound.init('sounddevice')  
from psychopy import visual, core, event, sound, data, gui, clock
import os
import csv
import uuid  
from datetime import datetime  


# Setup the Window
win = visual.Window(
    size=[1280, 720], fullscr=False, screen=0,
    # fullscr=True, screen=0,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[1, 1, 1], colorSpace='rgb',  
    blendMode='avg', useFBO=True, 
    units='height')

text_size = 0.04  # Consistent text size

# Define the demographic questions and options
demographic_questions = [
    {
        "question": "What is your age range?",
        "options": ["18-20", "21-23", "24-25", "Prefer not to say"]
    },
    {
        "question": "What is your gender?",
        "options": ["Male", "Female", "Other", "Prefer not to say"]
    },
    {
        "question": "What is your highest education level?",
        "options": ["High School", "Undergraduate", "Graduate", "Postgraduate"]
    },
    {
        "question": "What is your language proficiency in English?",
        "options": ["Native", "Fluent", "Intermediate", "Basic"]
    }
]

# Initialize components for Welcome Screen
welcomeText = visual.TextStim(win=win, name='welcomeText',
    text="""WELCOME!\n\n
    We appreciate your participation in our study. This study is conducted by the research team of Cognitive 
    Science Lab and Speech Processing Lab, International Institute of Information Technology, Hyderabad. It aims to
    understand Speech Emotion Perception and Production in young adults.
    
    There are going to be 5 different tasks & a demographic survey involved in the whole study. Each test is 
    different in nature and hence the duration. You will be informed about the details as you proceed. The total 
    time duration of the whole study will be 40-45 minutes.

    Your participation is entirely anonymous. No personal identifying information will be associated with the data we 
    collect from you. Anybody who is 18-25 years old and can understand and/or speak English is eligible to participate
    in this study.

    If you have any questions, you may ask us at any moment throughout the survey or thereafter. You can also email us 
    if you have any questions regarding this study:

    Research Student:
    guneesh.vats@research.iiit.ac.in

    Professors:
    priyanka.srivastava@iiit.ac.in and chiranjeevi.yarra@iiit.ac.in

    If you would like to know more, please proceed by clicking the 'Continue' button below.
    """,
    font='Arial', pos=(0, -1.4), height=text_size, wrapWidth=1.18, 
    color='black', colorSpace='rgb', opacity=1, languageStyle='LTR', alignText='left')

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
button_radius = 0.03  
button_spacing = 0.18  

# Set up valence and arousal buttons, and prepare images (SAM Scale Images)
valence_images = [f"sam_valence_{i}.jpg" for i in range(1, 6)]  
arousal_images = [f"sam_arousal_{i}.jpg" for i in range(1, 6)]

for i in range(1, 6):
    x_pos = -0.4 + (i - 1) * button_spacing
    samValenceButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='black', fillColor=None))
    samArousalButtons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.3), lineColor='black', fillColor=None))

# Debounce function to avoid multiple clicks being registered too fast
def debounce_click(mouse, wait_time=0.5):
    core.wait(wait_time)  # Wait for specified time in seconds
    while mouse.getPressed()[0]:  # Wait until the mouse button is released
        pass

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
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

# Function to display the consent form (positioned button on the right)
def display_consent_form():
    consentText = visual.TextStim(win=win, text= """
    Consent Form\n\n
    I hereby give my consent and permit members of the research team to access a de-identified version (with no mention of my name) of the data. The clinical information related to me will be used only for research purposes.\n\n
    I understand I will not be identified or identifiable in the report or reports that result from the research.\n\n
    I understand anonymized data can be shared in the public domain with other researchers worldwide.\n\n
    I have read the general information about the study and I have asked any questions regarding the procedure which have been satisfactorily answered. \n\n
    I am older than 18 years of age and no older than the age of 25.\n\n
    I understand the type of data being collected in this study and the reason for its collection. \n\n
    We hope you have read the general information. If you agree to all of the above, click on 'I Accept'  button to participate.
    """, font='Arial', pos=(0, 0.4), height=text_size, wrapWidth=1.18, color='black', colorSpace='rgb', 
    opacity=1, languageStyle='LTR', alignText='left')

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
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

# Function to display instructions (positioned button on the right)
def display_instructions():
    instructionsText = visual.TextStim(win=win, text= """
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
    
    Research Student: guneesh.vats@research.iiit.ac.in \n
    Professors: priyanka.srivastava@iiit.ac.in, chiranjeevi.yarra@iiit.ac.in.\n\n
    """,
    font='Arial', pos=(0, -1.5), height=text_size, wrapWidth=1.12, color='black', colorSpace='rgb', 
    opacity=1, languageStyle='LTR', alignText='left')

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

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.1

        if mouse.isPressedIn(understandButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

#############################################################################################
'''Demographic Instruction Page'''
#############################################################################################
def display_demographic_instructions():
    demographicText = visual.TextStim(win=win, text= """
    Demographic Survey Instructions\n\n
    Before proceeding with the tasks, we would like to collect some demographic information from you. This will include questions about your age, gender, language proficiency, and educational background.\n\n
    Please answer the following questions truthfully. The information will remain confidential and will only be used for research purposes.\n\n
    This survey will take around 5 minutes. After completing the survey, you will proceed to the main tasks of the study. If you are ready, click the 'Continue' button below to begin the demographic survey.\n\n
    """, font='Arial', pos=(0, 0.4), height=text_size, wrapWidth=1.18, color='black', colorSpace='rgb', 
    opacity=1, languageStyle='LTR', alignText='left')
    
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0, -0.7))  # Adjusted button position
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0, -0.7), height=0.04, color='white')
    # Adjust the position of the scroll to start at the top
    scroll_position = 0  # Ensures the page loads correctly at the top
    mouse = event.Mouse()

    

    while True:
        demographicText.setPos((0, scroll_position))  # Ensures text starts from the top
        demographicText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        if mouse.isPressedIn(continueButton):
            break

# Function to display demographic questions with fixed spacing and Submit button fully visible
def display_demographic_questions():
    scroll_position = 0  # Start the page from the top
    mouse = event.Mouse(visible=True, win=win)
    selected_answers = [-1] * len(demographic_questions)  # Track selected answer for each question

    question_texts = []
    option_buttons = []
    option_labels = []

    # Adjust vertical spacing between questions and options
    question_vertical_spacing = 0.4  # Reduced space between questions and options
    option_vertical_spacing = 0.08  # Slightly reduced space between options

    # Create visual elements for each question and options
    for idx, question_data in enumerate(demographic_questions):
        question_text = visual.TextStim(
            win=win, text=question_data["question"], pos=(0, 0.8 - idx * question_vertical_spacing), height=text_size, 
            wrapWidth=1.2, color='black', alignText='left'
        )
        question_texts.append(question_text)

        buttons = []
        labels = []
        for opt_idx, option in enumerate(question_data["options"]):
            button_pos = (-0.4, 0.65 - opt_idx * option_vertical_spacing - idx * question_vertical_spacing)  # Adjust position
            option_button = visual.Circle(win, radius=0.03, pos=button_pos, lineColor='black')
            option_label = visual.TextStim(win=win, text=option, pos=(button_pos[0] + 0.15, button_pos[1]), height=0.03, color='black')
            buttons.append(option_button)
            labels.append(option_label)
        option_buttons.append(buttons)
        option_labels.append(labels)

    # Add a Submit button that is fully visible
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='green', pos=(0, -0.7))  # Adjusted position to be fully visible
    continueButtonText = visual.TextStim(win=win, text="Submit", pos=(0, -0.7), height=0.04, color='white')

    while True:
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.1

        # Draw each question and its options
        for q_idx, question_text in enumerate(question_texts):
            question_text.setPos((0, 0.8 + scroll_position - q_idx * question_vertical_spacing))
            question_text.draw()

            for opt_idx, option_button in enumerate(option_buttons[q_idx]):
                option_button.setPos((-0.4, 0.65 + scroll_position - opt_idx * option_vertical_spacing - q_idx * question_vertical_spacing))
                option_button.draw()
                option_labels[q_idx][opt_idx].setPos((option_button.pos[0] + 0.15, option_button.pos[1]))
                option_labels[q_idx][opt_idx].draw()

                # Ensure only one option is selected per question
                if mouse.isPressedIn(option_button):
                    for ob in option_buttons[q_idx]:
                        ob.fillColor = None  # Clear previous selection
                    option_button.fillColor = 'blue'
                    selected_answers[q_idx] = opt_idx

        # Draw the Submit button fully visible
        continueButton.draw()
        continueButtonText.draw()

        win.flip()

        # Proceed if the submit button is pressed and all questions are answered
        if -1 not in selected_answers and mouse.isPressedIn(continueButton):
            break

    return selected_answers


#############################################################################################
'''SAM SCALE DEFINITION'''
#############################################################################################
# Define rate_sam function for SAM scale rating with adjusted horizontal space between buttons and images
def rate_sam(buttons, images, text):
    mouse = event.Mouse(visible=True, win=win)
    selected = None
    reaction_clock = core.Clock()

    # Define a consistent circle size
    button_radius = 0.03  # Fixed size for all circles
    button_spacing = 0.2  # Increase spacing for circular buttons to spread them out horizontally

    # Calculate positions for the main buttons (keep y position the same)
    main_buttons = []
    for i in range(len(buttons)):
        x_pos = -0.4 + i * button_spacing  # Increase horizontal alignment for better spacing between circles
        main_buttons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.2), lineColor='black'))  # Keep y position the same

    # Create new buttons for the additional in-between buttons
    additional_buttons = []
    for i in range(1, len(main_buttons)):
        mid_x = (main_buttons[i - 1].pos[0] + main_buttons[i].pos[0]) / 2  # Position in between main buttons
        additional_buttons.append(visual.Circle(win, radius=button_radius, pos=(mid_x, -0.2), lineColor='black'))  # Keep y position the same

    # Combine main and additional buttons into one list
    all_buttons = []
    for i in range(len(main_buttons)):
        all_buttons.append(main_buttons[i])
        if i < len(additional_buttons):
            all_buttons.append(additional_buttons[i])

    # Adjust the horizontal spacing of SAM images (increase the gap between images)
    image_spacing = 0.2  # Increase spacing between SAM images
    sam_images = [visual.ImageStim(win, image=image, pos=(-0.4 + i * image_spacing, 0.0), size=(0.18, 0.23)) for i, image in enumerate(images)]

    reaction_clock.reset()

    while True:
        text.draw()

        # Draw SAM images and buttons
        for i, button in enumerate(all_buttons):
            if i % 2 == 0:  # Only main buttons have images
                sam_images[i // 2].draw()
            button.draw()
            if selected == i:
                visual.Circle(win, radius=button_radius, pos=button.pos, fillColor='blue').draw()

        win.flip()

        # Mouse interaction for selecting buttons
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for i, button in enumerate(all_buttons):
                if button.contains(pos):
                    selected = i

        # Continue if the return key is pressed and a button is selected
        keys = event.getKeys(['return', 'escape'])
        if 'return' in keys and selected is not None:
            rt = reaction_clock.getTime()
            return selected + 1, rt  # Return the selected button (1-based index) and reaction time
        elif 'escape' in keys:
            core.quit()



# Function to play stimuli and track play count and reaction time
# Function to play stimuli and track play count and reaction time
def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)  # Removed device argument
    reaction_clock = core.Clock()
    
    progress = f"Audio : {audio_index+1}/{len(audioStimuli)} : {round((audio_index + 1) / len(audioStimuli) * 100, 1)}% done\n (Press Space to continue)"
    progressText.setText(progress)

    while True:
        playButton.draw()
        playButtonText.draw()
        progressText.draw()
        win.flip()

        mouse = event.Mouse()
        if mouse.isPressedIn(playButton):
            stim.stop()  # Stop any previous sound if playing
            stim.play()  # Play the sound
            playCount += 1
            playButtonText.setText("Playing...")
            playButton.draw()
            playButtonText.draw()
            progressText.draw()
            win.flip()

            core.wait(stim.getDuration())  # Wait for the sound to finish

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
csv_file = 'experiment_data_temp.csv'
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

# Function to record audio using sounddevice and save as .wav with dynamic start/stop
def record_audio_dynamic(file_name, fs=16000):
    print("Recording started...")
    audio_data = []
    stream = sd.InputStream(samplerate=fs, channels=1, callback=lambda indata, frames, time, status: audio_data.append(indata.copy()))
    stream.start()
    return stream, audio_data


def stop_audio_dynamic(stream, audio_data, file_name, fs=16000):
    print("Recording stopped...")
    stream.stop()
    stream.close()

    if len(audio_data) > 0:  # Only concatenate if audio data exists
        audio_array = np.concatenate(audio_data, axis=0)  # Combine all recorded data
        wavio.write(file_name, audio_array, fs, sampwidth=2)  # Save as .wav
        print(f"Recording saved as {file_name}")
    else:
        print("No audio data recorded")

# Paragraphs for speech production task
paragraphs = [
    "This is the first paragraph for the speech production task. Please read it out loud when ready.",
    "This is the second paragraph. Try to read it naturally while recording.",
    "This is the third paragraph. Speak clearly and make sure you are recording."
]

# Function to display paragraphs and record speech with start/stop toggle
def speech_production_task(participant_id, paragraph_num):
    # Added smaller two-line instructions above the record button
    instructions_text = visual.TextStim(win=win, text="Please read the paragraph below aloud.\nPress the record button to start.", 
                                        font='Arial', pos=(0, 0.35), height=0.03, color='black', wrapWidth=0.8)
    
    paragraphText = visual.TextStim(win=win, text=paragraphs[paragraph_num-1], 
                                    font='Arial', pos=(0, 0.15), height=0.04, wrapWidth=0.8, 
                                    color='black', colorSpace='rgb', opacity=1, languageStyle='LTR')
    
    recordButton = visual.Rect(win, width=0.6, height=0.1, fillColor='red', pos=(0, -0.3))
    recordButtonText = visual.TextStim(win=win, text="Record", pos=(0, -0.3), height=0.05, color='white')

    mouse = event.Mouse(visible=True, win=win)
    recording = False
    stream = None
    audio_data = []
    start_time = None
    end_time = None
    audio_file = f"{participant_id}_paragraph_{paragraph_num}.wav"
    
    while True:
        instructions_text.draw()
        paragraphText.draw()
        recordButton.draw()
        recordButtonText.draw()
        win.flip()

        if mouse.isPressedIn(recordButton):
            debounce_click(mouse)
            if not recording:
                recording = True
                start_time = core.getTime()
                recordButtonText.setText("Recording (Click to stop)")
                win.flip()
                # Start recording
                stream, audio_data = record_audio_dynamic(audio_file)
            else:
                recording = False
                end_time = core.getTime()
                recordButtonText.setText("Recorded")
                win.flip()
                # Stop recording
                stop_audio_dynamic(stream, audio_data, audio_file)
                debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
                break  # Exit after recording

    duration = end_time - start_time if start_time and end_time else 0
    return audio_file, duration


# Function to display all three paragraphs and record the participant's response
def run_speech_production_task(participant_id):
    speech_data = []
    
    for i in range(1, 4):
        audio_file, audio_duration = speech_production_task(participant_id, i)
        speech_data.append([audio_file, audio_duration])
    
    return speech_data

# After audio stimuli, run the speech production task
speech_production_data = run_speech_production_task(participant_id)

# Add the speech production data to the participant data list
for i, speech_data in enumerate(speech_production_data):
    participant_data.append(speech_data)

# Display demographic instructions page before the demographic survey starts
display_demographic_instructions()

# Display the demographic questions and get the selected answers
selected_answers = display_demographic_questions()
# You can now process `selected_answers` to store them or use them for later steps
# For example, you can append them to participant data and store it in the CSV.
participant_data.append(selected_answers)

# Append participant data to the CSV (this part will remain as it is)
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)
    
    if not file_exists:
        header = ['Participant ID', 'Session Start Time']
        for i in range(len(audioStimuli)):
            header += [f'Stimuli Name {i+1}', f'Valence {i+1}', f'Valence RT {i+1}', 
                       f'Arousal {i+1}', f'Arousal RT {i+1}', f'Play Count {i+1}']
        for i in range(1, 4):
            header += [f'Paragraph {i} Audio File', f'Paragraph {i} Audio Duration']
        header += ["Age", "Gender", "Education", "Language Proficiency"]  # Add demographic columns
        writer.writerow(header)

    participant_data_row = [participant_id, session_start_time]
    for stimulus_data in participant_data[2:]:
        participant_data_row += stimulus_data
    writer.writerow(participant_data_row)

win.close()
core.quit()
