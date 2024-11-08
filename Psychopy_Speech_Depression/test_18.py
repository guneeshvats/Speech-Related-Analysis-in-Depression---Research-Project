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
from psychopy.visual import TextBox2
from psychopy.visual import TextBox


# Setup the Window
win = visual.Window(
    size=[1280, 720], fullscr=False, screen=0,
    # fullscr=True, screen=0,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[1, 1, 1], colorSpace='rgb',  
    blendMode='avg', useFBO=True, 
    units='height')

text_size = 0.040  # Consistent text size

############################################################################################################################################################
'''                                                                       WELCOME PAGE                                                                
'''
############################################################################################################################################################
welcomeHeading = visual.TextStim(
    win=win, name='welcomeHeading',
    text="WELCOME!",
    font='Arial',
    pos=(0, 0.4),  
    height=0.06,  
    color='black',
    colorSpace='rgb',
    opacity=1,
    alignText='center'  
)

welcomeText = visual.TextStim(win=win, name='welcomeText',
    text="""We appreciate your participation in our study. This study is conducted by the Cognitive Science Lab and Speech Processing Lab at the International Institute of Information Technology (IIIT), Hyderabad. Our goal is to understand Speech Emotion Perception and Production in young adults.

Your participation is anonymous; no personal information will be linked to your responses. If you are 18-25 years old and can understand or speak English, you are eligible to participate.
    
If you have any questions, you may ask us at any moment throughout the survey or email us:

        - Research Student: guneesh.vats@research.iiit.ac.in
        - Professors: priyanka.srivastava@iiit.ac.in,
                      chiranjeevi.yarra@iiit.ac.in

    To continue, please click the 'Continue' button below.
    """,
    font='Arial', 
    pos=(-0.4, -0.15), 
    height=text_size, 
    wrapWidth=1.15, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')

# 'Continue' button for welcome page (positioned on the right side)
continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.42))
continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.42), height=0.04, color='white')

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
    while any(mouse.getPressed()):  # Wait until all mouse buttons are released
        pass
    core.wait(wait_time)  # Add an additional wait after the release

# Function to display the scrollable welcome screen
def display_welcome():
    scroll_position = -0.34  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Set the position of both the heading and the main text based on scroll_position
        welcomeHeading.setPos((0, 0.77 + scroll_position))  # Adjust the y-position for the heading
        welcomeText.setPos((0, 0.27+scroll_position))  # Adjust the y-position for the main text

        # Draw both the heading and the main text
        welcomeHeading.draw()
        welcomeText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

############################################################################################################################################################
'''                                                                       GENERAL INSTRUCTIONS ABOUT STUDY                                                                 
'''
############################################################################################################################################################
instructionsHeading = visual.TextStim(
    win=win, name='instructionsHeading',
    text="GENERAL INSTRUCTIONS",
    font='Arial',
    pos=(0, 0.4),  
    height=0.06,  
    color='black',
    colorSpace='rgb',
    opacity=1,
    alignText='center'
)

def display_instructions():
    instructionsText = visual.TextStim(win=win, text= 
    """Let me walk you through the process. Also, please read the given FAQ carefully.\n
The study will last for around 40-45 minutes and consists of 5 tasks:\n
    - Emotion Perception Test
    - Language Fluency Test
    - Speech Production Test
    - Demographic Survey
    - Current Mood Assessment
    - General Health Questionnaire\n
The study will begin with a Language Fluency Test, followed by an assessment of your current mood. Next, you’ll listen to a series of audio clips and identify the speaker's emotions. Detailed instructions for this task will be provided beforehand.

Following that, you'll complete a Speech Production Task, where you'll record yourself reading a few paragraphs aloud. Finally, the study concludes with a Demographic Survey and a General Health Survey to gather general health information.

Each task is unique in nature and duration.\n\n
                        FREQUENTLY ASKED QUESTIONS (FAQ)\n
Q: What are the benefits of this research?\n
A: You may not be directly benefited by participating in our study. However, your participation will potentially advance our understanding of the impact of psychological health on emotion perception.\n\n
Q: What are the risks or inconveniences involved in this survey?\n
A: This study requires you to listen to audio clips and record yourself reading a paragraph. There are no known risks associated; however, you may feel some fatigue from prolonged listening. To ensure your comfort, we’ll maintain recommended volume levels. If you experience any discomfort, please let us know immediately.\n\n
Q: How will my personal information be protected?\n
A: Your privacy is our priority. All data collected in this study will remain anonymous, and no personal identifying information will be linked to your responses. Data will be stored securely and accessible only to authorized members of the research team. Results will be reported in aggregate form, ensuring individual identities remain confidential.\n\n
Q: What are my participation rights?\n
A: Your participation in this study is entirely voluntary. You can choose to withdraw from this study at any point in time. However, for the benefit of research, we request you complete the study.\n\n
Q: Whom do I contact if I have questions about the survey?\n
A: If you have any questions, you may ask us at any moment throughout the survey or thereafter. You can also email us if you have any questions regarding this study:\n
    
    - Research Student: guneesh.vats@research.iiit.ac.in
    - Professors: priyanka.srivastava@iiit.ac.in, 
                           chiranjeevi.yarra@iiit.ac.in

If you understand and wish to proceed, please click the "I Understand" button
    """,
    font='Arial', 
    pos=(-0.45, -0.55), 
    height=text_size, 
    wrapWidth=1.1, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')

    # Submit Button (or in this case - I Understand button)
    understandButton = visual.Rect(win, width=0.3, height=0.07, fillColor='darkgreen', pos=(0.70, -0.4))
    understandButtonText = visual.TextStim(win=win, text="I Understand", pos=(0.70, -0.4), height=0.04, color='white')

    scroll_position = -1.44
    mouse = event.Mouse()

    while True:
        # Defining heading and its position in the page
        instructionsHeading.setPos((0, 1.83 + scroll_position))

        instructionsText.setPos((0, 0.02+ scroll_position))
        instructionsHeading.draw()
        instructionsText.draw()
        understandButton.draw()
        understandButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        if mouse.isPressedIn(understandButton):
             # Debounce to prevent accidental multiple clicks
            debounce_click(mouse) 
            break

############################################################################################################################################################
'''                                                                  CONSENT FORM                                                                
'''
############################################################################################################################################################

consentHeading = visual.TextStim(
    win=win, name='consentHeading',
    text="CONSENT FORM",
    font='Arial',
    pos=(0, 0.4),
    height=0.06,  
    color='black',
    colorSpace='rgb',
    opacity=1,
    alignText='center'
)

# Function to display the consent form (positioned button on the right)
def display_consent_form():
    consentText = visual.TextStim(win=win, text= 
    """
1. I hereby give my consent and permit members of the research team to access a de-identified version (with no mention of my name) of the data. The clinical information related to me will be used only for research purposes.\n
2. I understand I will not be identified or identifiable in the report or reports that result from the research.\n
3. I understand that anonymized data can be shared in the public domain with other researchers worldwide.\n
4. I have read the general information about the study and I have asked any questions regarding the procedure which have been satisfactorily answered. \n
5. I am older than 18 years of age and no older than the age of 25.\n
6. I understand the type of data being collected in this study and the reason for its collection. \n\n
We hope you have read the general information. If you agree to all of the above, click on 'I Accept'  button to participate.
    """, font='Arial', 
    pos=(-0.40, -0.35), 
    height=text_size, 
    wrapWidth=1.15, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')

    acceptButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))  # Button moved to the right
    acceptButtonText = visual.TextStim(win=win, text="I Accept", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.33
    mouse = event.Mouse()

    while True:
        consentHeading.setPos((0, 0.71 + scroll_position))
        consentText.setPos((0, 0.098+scroll_position))

        consentHeading.draw()
        consentText.draw()
        acceptButton.draw()
        acceptButtonText.draw()
        win.flip()

        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        if mouse.isPressedIn(acceptButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break


############################################################################################################################################################
'''                                                               LANGUAGE FLUENCEY TEST                                                                
'''
############################################################################################################################################################


############################################################################################################################################################
'''                                                               PANAS - 10 (CURRENT MOOD)                                                                 
'''
############################################################################################################################################################

# PANAS Survey Questions and Options
panas_questions = [
    "Interested", "Distressed", "Excited", "Upset", "Strong", "Guilty", "Scared",
    "Hostile", "Enthusiastic", "Proud", "Irritable", "Alert", "Ashamed", "Inspired",
    "Nervous", "Determined", "Attentive", "Jittery", "Active", "Afraid"
]
panas_options = ["Very slightly or not at all", "A little", "Moderately", "Quite a bit", "Extremely"]

def display_panas_survey():
    mouse = event.Mouse(visible=True, win=win)
    selected_answers_panas = [-1] * len(panas_questions)  # Track selected answers

    # Instruction text for PANAS
    instruction_text = visual.TextStim(
        win=win, 
        text="This scale consists of a number of words that describe different feelings and emotions. Read each item and indicate to what extent you are feeling right now", 
        pos=(0, 0.9), 
        height=0.04, 
        color='black', 
        wrapWidth=1.5, 
        alignText='center'
    )

    # Option labels for PANAS (similar to PHQ-9 options display)
    option_label_texts = []
    option_horizontal_spacing = 0.25   #0.25
    text_size_small = 0.03

    for i, label in enumerate(panas_options):
        label_pos = (-0.3 + i * option_horizontal_spacing, 0.75)
        label_text = visual.TextStim(win=win, text=label, pos=label_pos, height=text_size_small, color='black', wrapWidth=0.2)
        option_label_texts.append(label_text)

    question_vertical_spacing = 0.14
    question_texts = []
    option_buttons = []

    for idx, question in enumerate(panas_questions):
        question_text = visual.TextStim(
            win=win, text=question, 
            pos=(-0.62, 0.6 - idx * question_vertical_spacing), 
            height=text_size_small, 
            wrapWidth=0.5, 
            color='black'
        )
        question_texts.append(question_text)

        buttons = []
        for opt_idx in range(len(panas_options)):
            button_pos = (-0.3 + opt_idx * option_horizontal_spacing, 0.6 - idx * question_vertical_spacing)
            option_button = visual.Circle(win, radius=0.02, pos=button_pos, lineColor='black')
            buttons.append(option_button)
        option_buttons.append(buttons)

    submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.45))
    submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.8), height=0.04, color='white')

    scroll_position = -0.5
    scroll_step = 0.05

    while True:
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * scroll_step

        instruction_text.setPos((0, 0.9 + scroll_position))
        instruction_text.draw()

        for label in option_label_texts:
            label.setPos((label.pos[0], 0.75 + scroll_position))
            label.draw()

        for q_idx, question_text in enumerate(question_texts):
            question_text.setPos((-0.62, 0.6 + scroll_position - q_idx * question_vertical_spacing))
            question_text.draw()
            for opt_idx, option_button in enumerate(option_buttons[q_idx]):
                option_button.setPos((-0.3 + opt_idx * option_horizontal_spacing, 0.6 + scroll_position - q_idx * question_vertical_spacing))
                option_button.draw()
                if selected_answers_panas[q_idx] == opt_idx:
                    visual.Circle(win, radius=0.02, pos=option_button.pos, fillColor='blue').draw()

        submit_button.setPos((0.7, -2.18 + scroll_position))
        submit_button_text.setPos((0.7, -2.18 + scroll_position))
        submit_button.draw()
        submit_button_text.draw()

        win.flip()

        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for q_idx, question_buttons in enumerate(option_buttons):
                for opt_idx, button in enumerate(question_buttons):
                    if button.contains(mouse):
                        selected_answers_panas[q_idx] = opt_idx

        if -1 not in selected_answers_panas and mouse.isPressedIn(submit_button):
            debounce_click(mouse)
            break

    # Adjust index to start from 1 instead of 0
    return [response + 1 for response in selected_answers_panas]




############################################################################################################################################################
'''                                                               SPEECH PERCEPTION TASK                                                                  
'''
############################################################################################################################################################

perceptionInstructionText = visual.TextStim(win=win, text= 
    """
Instructions

In this session, you will listen to a series of audio files and rate the speaker's emotion.

For each audio clip:

You’ll see an audio file with a play button at the top of the page. Press ‘Play’ to listen, and you may replay it as needed.
Following the audio, you’ll rate the speaker's emotion across two dimensions on the next two pages: Valence and Arousal.
Rating Scales:

Valence (1 = extremely unpleasant, 9 = extremely pleasant)

Unpleasant feelings include unhappy, annoyed, or bored.
Pleasant feelings include happy, contented, or hopeful.
For neutral feelings, select the middle rating (5). Intermediate numbers can be used for in-between feelings.
Arousal (1 = low arousal, 9 = high arousal)

Low arousal feelings include relaxed, calm, or sleepy.
High arousal feelings include excited, jittery, or wide-awake.
For neutral arousal, select the middle rating (5). Use intermediate numbers if necessary.
Each page will display the question clearly along with a visual scale. Select the figure that best represents the speaker’s emotion according to your perception.

A progress bar at the top will indicate your completion percentage and the audio clip number.

If you’re ready to begin, click "Continue."
    """, font='Arial', 
    pos=(-0.40, -0.35), 
    height=text_size, 
    wrapWidth=1.15, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')


# Here will go the code for the instruction page







# SAM SCALE for rating of stimuli
def rate_sam(buttons, images, text, left_label_text, right_label_text):
    mouse = event.Mouse(visible=True, win=win)
    selected = None
    reaction_clock = core.Clock()

    # Define a consistent circle size and spacing for a 9-point scale
    button_radius = 0.03
    button_spacing = 0.1  # Reduced spacing to fit 9 buttons across the screen

    # Define the left and right labels with updated positions
    left_label = visual.TextStim(win, text=left_label_text, pos=(-0.55, -0.28), height=0.03, color='black', alignText='center')
    right_label = visual.TextStim(win, text=right_label_text, pos=(0.55, -0.28), height=0.03, color='black', alignText='center')

    # Calculate positions for the 9 buttons (centered horizontally)
    main_buttons = []
    for i in range(9):  # Updated to 9 buttons for a 9-point scale
        x_pos = -0.4 + i * button_spacing
        main_buttons.append(visual.Circle(win, radius=button_radius, pos=(x_pos, -0.2), lineColor='black'))

    # SAM images (still positioned above the buttons for the 5 images in the scale)
    image_spacing = 0.2
    sam_images = [visual.ImageStim(win, image=image, pos=(-0.4 + i * image_spacing, 0.0), size=(0.18, 0.23)) for i, image in enumerate(images)]

    reaction_clock.reset()

    while True:
        # Draw the question text
        text.draw()

        # Draw SAM images and 9-point scale buttons
        for i, button in enumerate(main_buttons):
            if i % 2 == 0 and i // 2 < len(sam_images):  # Draw images only at specific positions
                sam_images[i // 2].draw()
            button.draw()
            if selected == i:
                visual.Circle(win, radius=button_radius, pos=button.pos, fillColor='blue').draw()

        # Draw the left and right labels
        left_label.draw()
        right_label.draw()

        win.flip()

        # Mouse interaction for selecting buttons
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for i, button in enumerate(main_buttons):
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
def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)
    reaction_clock = core.Clock()

    # Prompt Text at the top of the screen
    promptText = visual.TextStim(
        win=win,
        text="Please click the 'Play' button to listen to the audio file.\nListen carefully to the following audio clip and pay attention to the speaker's tone and emotion",
        font='Arial',
        pos=(0, 0.2),  # Position it above the play button
        height=0.03,
        wrapWidth=1.2,
        color='black',
        colorSpace='rgb',
        opacity=1,
        languageStyle='LTR',
        alignText='center'
    )

    # Progress text at the very top
    progress = f"Audio: {audio_index + 1}/{len(audioStimuli)} - {round((audio_index + 1) / len(audioStimuli) * 100, 1)}% completed"
    progressText.setText(progress)
    progressText.setPos((0, 0.4))  # Position at the top of the window

    # Instruction text to display after the first play
    replayInstructionText = visual.TextStim(
        win=win,
        text="Click 'Play Again' to replay the audio.",
        font='Arial',
        pos=(0, -0.15),  # Position below the play button
        height=0.03,  # Smaller font size
        color='black',
        colorSpace='rgb',
        opacity=1,
        languageStyle='LTR',
        alignText='center'
    )

    playButtonText.setText("Play")  # Initially set button text to "Play"

    while True:
        # Draw all elements in every frame to ensure they stay visible
        promptText.draw()           # Draw question statement
        playButton.draw()            # Draw play button
        playButtonText.draw()        # Draw button text
        progressText.draw()          # Draw progress text
        
        # Draw replay instruction text after the first play
        if playCount > 0:
            replayInstructionText.draw()

        win.flip()

        mouse = event.Mouse()
        if mouse.isPressedIn(playButton):
            playButtonText.setText("Playing")  # Set button to "Playing" while audio is playing
            promptText.draw()  # Re-draw prompt text
            playButton.draw()  # Re-draw button
            playButtonText.draw()  # Re-draw button text
            progressText.draw()  # Re-draw progress text
            if playCount > 0:
                replayInstructionText.draw()  # Re-draw instruction text

            win.flip()
            
            stim.stop()  # Stop any previous sound if playing
            stim.play()  # Play the sound
            playCount += 1
            core.wait(stim.getDuration())  # Wait for the sound to finish

            playButtonText.setText("Play Again")  # Change button to "Play Again" after the audio finishes
            win.flip()

        # Continue to the next page if space is pressed
        keys = event.getKeys(['return'])
        if 'return' in keys:
            rt = reaction_clock.getTime()
            break
    
    return playCount, rt

# Stimuli loop setup
audioStimuli = ['audio_1.wav', 'audio_2.wav']

############################################################################################################################################################
'''                                                                       SPEECH PRODUCTION TASK                                                                  
'''
############################################################################################################################################################

def display_speech_production_instructions():
    # Heading for the instruction page, similar to the "WELCOME" heading
    speechHeading = visual.TextStim(
        win=win, name='speechHeading',
        text="SPEECH PRODUCTION TASK",
        font='Arial',
        pos=(0, 0.4),  # Position at the top
        height=0.06,  # Larger text size for the heading
        color='black',
        colorSpace='rgb',
        opacity=1,
        alignText='center'
    )

    # Instruction text for the speech production task, matching the style of the welcome page
    speechInstructionsText = visual.TextStim(
        win=win,
        text=
        """You are about to begin the Speech Production Task.\n
In this task, you will be presented with a series of three paragraphs. Your goal is to read each paragraph aloud while recording your voice.\n
- Each page will display one paragraph.
- Click the 'Record' button to start recording. Read the paragraph aloud at a clear and natural pace.
- The button will show "Recording (Click to stop)", indicating that the recording has started, and you should begin reading the paragraph.\n
- Once you’ve finished reading, click the "Recording (Click to Stop)" button to end the recording, as shown in the image below.\n
- After clicking Stop, the next page will automatically appear with another paragraph.\n\n\n\n\n\n\n\n\n
- Repeat this process for all three paragraphs across three pages.\n
Please ensure you complete reading the entire paragraph before stopping the recording.\n
    When you're ready to begin, click the 'Continue' button below.
        """,
        font='Arial',
        pos=(-0.45, -0.38), 
        height=text_size,  
        wrapWidth=1.13,
        color='black',       
        colorSpace='rgb',
        opacity=1,
        alignText='left'
    )

    # Add images side by side
    image1 = visual.ImageStim(
        win=win,
        image='record_1.png',  # Replace with your actual image file
        pos=(-0.2, -0.15),  # Position image1 on the left
        size=(0.56, 0.23)  # Adjust size as needed
    )
    image2 = visual.ImageStim(
        win=win,
        image='record_2.png',  # Replace with your actual image file
        pos=(0.2, -0.15),  # Position image2 on the right
        size=(0.56, 0.23)  # Adjust size as needed
    )

    # "Continue" button matching the style and position of the welcome page
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.13  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Update the position of the main text based on scroll_position
        speechHeading.setPos((0, 0.52 + scroll_position))
        speechInstructionsText.setPos((0, -0.34+scroll_position))
        image1.setPos((-0.3, -0.57 + scroll_position))  # Make image1 scroll
        image2.setPos((0.28, -0.57 + scroll_position))   # Make image2 scroll

        # Draw the heading, text, and button
        speechHeading.draw()
        speechInstructionsText.draw()
        
        image1.draw()
        image2.draw()

        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        # Check if the continue button is clicked
        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

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
    # Adjusted instruction text to be higher on the screen
    instructions_text = visual.TextStim(
        win=win,
        text="Please read the paragraph below aloud.\nPress the record button to start.",
        font='Arial',
        pos=(0, 0.45),  # Move the instructions higher up
        height=0.03,  # Smaller text size for instructions
        color='black',
        wrapWidth=0.8
    )

    # Paragraph text positioned below the record button
    paragraphText = visual.TextStim(
        win=win,
        text=paragraphs[paragraph_num - 1],
        font='Arial',
        pos=(0, -0.05),  # Move paragraph higher up to leave more space
        height=0.04,
        wrapWidth=0.8,
        color='black',
        colorSpace='rgb',
        opacity=1,
        languageStyle='LTR'
    )

    # Record button positioned slightly higher on the screen
    recordButton = visual.Rect(
        win, width=0.6, height=0.1, fillColor='red', pos=(0, 0.35)  # Move button higher up
    )
    recordButtonText = visual.TextStim(
        win=win,
        text="Record",
        pos=(0, 0.35),  # Match position of the button [VERY IMPORTANT]
        height=0.05,
        color='white'
    )

    mouse = event.Mouse(visible=True, win=win)
    recording = False
    stream = None
    audio_data = []
    start_time = None
    end_time = None
    audio_file = f"{participant_id}_paragraph_{paragraph_num}.wav"

    while True:
        # Draw all elements on the screen
        instructions_text.draw()  # Draw instructions at the top
        recordButton.draw()  # Draw record button
        recordButtonText.draw()  # Draw record button text
        paragraphText.draw()  # Draw paragraph text below the button
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

############################################################################################################################################################
'''                                                                       DEMOGRAPHICS                                                                 
'''
############################################################################################################################################################
# Function to display demographic instructions with a heading and scrollable text
def display_demographic_instructions():
    # Heading for the demographic instruction page
    demographicHeading = visual.TextStim(
        win=win, name='demographicHeading',
        text="DEMOGRAPHIC SURVEY",
        font='Arial',
        pos=(0, 0.4),  # Position at the top
        height=0.06,  # Larger text size for the heading
        color='black',
        alignText='center'
    )

    # Instruction text for the demographic survey
    demographicText = visual.TextStim(
        win=win,
        text="""Before we proceed, we kindly ask you to complete a brief demographic survey.\nThis short survey helps us gather essential background information to support our research. Your responses will remain entirely confidential and will be used exclusively for research purposes. The survey should take few minutes to complete. Once you’re finished, you’ll be guided to the final test of the study.\n\n

        Please click 'Continue' when you're ready to begin.
        """,
        font='Arial',
        pos=(-0.45, -0.15),  # Initial position
        height=text_size,  # Same text size as the welcome page
        wrapWidth=1.1,
        color='black',
        alignText='left'
    )

    # "Continue" button matching the style and position of the welcome page
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.10  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Update the position of the heading and main text based on scroll_position
        demographicHeading.setPos((0, 0.49 + scroll_position))
        demographicText.setPos((0, 0.140+scroll_position))

        # Draw the heading, text, and button
        demographicHeading.draw()
        demographicText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        # Check if the continue button is clicked
        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break

# Defining the demographic questions and options
demographic_questions = [
    {
        "question": "What gender do you most identify with?",
        "options": ["Male", "Female", "Transfemale", "Transmale", "Non-Binary", "Others", "Don't want to specify"]
    },
    {
        "question": "Select the option which best described your latest education status?",
        "options": ["Level XI - Level XII or Higher Seecondary", "Graduation", "Post Graduation", "Diploma", "PhD", "No Formal Education"]
    },
    {
        "question": "What is your language proficiency in English?",
        "options": ["Native", "Fluent", "Intermediate", "Basic"]
    }
    ,
    {
        "question": "Have you ever been diagnosed with a hearing condition (such as tinnitus, hearing loss, or other hearing-related disorder?",
        "options": ["Yes", "No"]
    }, 
    {
        "question": "Do you currently use any devices or tools to assist with your hearing, such as hearing aids or cochlear implants?",
        "options": ["Yes", "No"]
    }
]

# Text input for age (since we removed it from demographic_questions)
age_input_box = TextBox2(win, text='', 
                         pos=(0, 0.4), 
                         letterHeight=0.05, 
                         color='black', 
                         size=(0.2, 0.1))

age_question = visual.TextStim(win=win, 
                               text="What is your age?", 
                               pos=(-0.30, 0.92), 
                               height=text_size, 
                               color='black',
                               alignText = 'left')


# Function to display demographic questions with proper spacing and scrolling functionality
def display_demographic_questions():
    scroll_position = -0.34  # Start the page from the top
    mouse = event.Mouse(visible=True, win=win)
    selected_answers = [-1] * len(demographic_questions)  # Track selected answer for each question

    question_texts = []
    option_buttons = []
    option_labels = []

    # Define custom spacing for each question based on the number of options
    custom_spacing = [
        0.825,  
        0.74,  
        0.59,
        0.33, 
        0.33
    ]

    option_vertical_spacing = 0.1  # Space between options for each question

    # Create visual elements for each question and options
    for idx, question_data in enumerate(demographic_questions):
        question_text = visual.TextStim(
            win=win, text=question_data["question"],
            pos=(0, 0.8 - sum(custom_spacing[:idx])), height=text_size,
            wrapWidth=1.2, color='black', alignText='left'
        )
        question_texts.append(question_text)

        buttons = []
        labels = []
        for opt_idx, option in enumerate(question_data["options"]):
            button_pos = (-0.4, 0.7 - sum(custom_spacing[:idx]) - opt_idx * option_vertical_spacing)
            option_button = visual.Circle(win, 
                                          radius=0.03, 
                                          pos=button_pos, 
                                          lineColor='black', 
                                          fillColor=None)
            option_label = visual.TextStim(win=win, 
                                           text=option, 
                                           pos=(button_pos[0] + 0.45, button_pos[1]), 
                                           height=0.03, 
                                           color='black')
            buttons.append(option_button)
            labels.append(option_label)
        option_buttons.append(buttons)
        option_labels.append(labels)

    # Create a Submit button similar to the Continue button from the welcome page
    submitButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    submitButtonText = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.4), height=0.04, color='white')


    while True:
        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        # Draw age question and input box
        age_question.setPos((0, 0.85 + scroll_position))
        age_question.draw()
        age_input_box.setPos((0, 0.8 + scroll_position))
        age_input_box.draw()

            # Capture numeric input for age
        keys = event.getKeys()
        for key in keys:
            if key == 'backspace':
                age_input_box.text = age_input_box.text[:-1]  # Remove last character
            elif key in '0123456789':  # Allow only numbers
                age_input_box.text += key


        # Draw each question and its options with scroll position
        for q_idx, question_text in enumerate(question_texts):
            question_text.setPos((0, 0.8 + scroll_position - sum(custom_spacing[:q_idx])))
            question_text.draw()

            for opt_idx, option_button in enumerate(option_buttons[q_idx]):
                option_button.setPos((-0.4, 0.7 + scroll_position - sum(custom_spacing[:q_idx]) - opt_idx * option_vertical_spacing))
                option_button.draw()
                option_labels[q_idx][opt_idx].setPos((option_button.pos[0] + 0.15, option_button.pos[1]))
                option_labels[q_idx][opt_idx].draw()

                # Check for mouse click and ensure only one option is selected per question
                if mouse.isPressedIn(option_button):
                    # Deselect all options for the current question
                    for ob in option_buttons[q_idx]:
                        ob.fillColor = None
                    # Select the clicked option
                    option_button.fillColor = 'blue'
                    selected_answers[q_idx] = opt_idx

        # Draw the Submit button
        submitButton.draw()
        submitButtonText.draw()

        # Check if the Submit button is clicked and all questions are answered
        if mouse.isPressedIn(submitButton) and -1 not in selected_answers:
            debounce_click(mouse)  # Prevent accidental multiple clicks
            break  # Exit the loop when the Submit button is clicked

        win.flip()

    return selected_answers

############################################################################################################################################################
'''                                                              PSYCHOLOGICAL DEMOGRAPHICS                                                                 
'''
############################################################################################################################################################

# Define the psychological demographics questions and options

psych_demographics = [
    {
        "question": "Have you ever sought psychological help from professionals like therapists or psychiatrists?",
        "options": ["Yes", "No"]
    },
    {
        "question": "Are you currently consulting any mental health professional (e.g., psychotherapist, psychiatrist, or counselor)?",
        "options": ["Yes", "No"]
    },
    {
        "question": "Do you have any family member or relative who has been diagnosed with a mental illness?",
        "options": ["Yes", "No"]
    }
]

# Additional options for detailed questions
mental_health_conditions = [
    "Depression", "Mania/Bipolar Disorder", "Psychotic Disorder (Including Schizophrenia)",
    "Anxiety Disorder", "Post Traumatic Stress Disorder", "Eating Disorder",
    "Compulsive Disorder (OCD)", "Substance Abuse or Addiction Disorder",
    "Attention Disorder (ADD or ADHD)", "Somatoform Disorder", "Personality Disorder",
    "Autism Spectrum Disorder (Including Asperger's Syndrome)", "Cognitive Disorder/Dementia"
]

treatment_types = [
    "Psychotherapy/Counseling", "Psychiatric Medication", "Hospitalization", "Prefer to Self Describe"
]

# Initialize list to store all responses
responses = []

def display_psych_demographics():
    mouse = event.Mouse(visible=True, win=win)
    scroll_position = 0  # Initial scroll position
    min_scroll_position = -1.5  # Minimum scroll position for downward scrolling
    max_scroll_position = 0.5  # Maximum scroll position to allow upward scrolling
    responses = []  # Collect all responses

    # Helper function to display yes/no questions with scrolling
    def display_yes_no_question(question_text):
        nonlocal scroll_position
        question = visual.TextStim(win=win, text=question_text, pos=(0, 0.4 + scroll_position), height=0.04, color='black')
        yes_button = visual.Circle(win, radius=0.03, pos=(-0.3, 0.2 + scroll_position), lineColor='black')
        no_button = visual.Circle(win, radius=0.03, pos=(0.3, 0.2 + scroll_position), lineColor='black')
        yes_text = visual.TextStim(win=win, text="Yes", pos=(-0.3, 0.2 + scroll_position), height=0.03, color='black')
        no_text = visual.TextStim(win=win, text="No", pos=(0.3, 0.2 + scroll_position), height=0.03, color='black')
        selected = None

        while selected is None:
            # Handle scrolling in both directions
            scroll_wheel = mouse.getWheelRel()[1]
            scroll_position += scroll_wheel * 0.05
            scroll_position = max(min(scroll_position, max_scroll_position), min_scroll_position)

            # Draw elements with updated scroll position
            question.setPos((0, 0.4 + scroll_position))
            question.draw()
            yes_button.setPos((-0.3, 0.2 + scroll_position))
            yes_button.draw()
            no_button.setPos((0.3, 0.2 + scroll_position))
            no_button.draw()
            yes_text.setPos((-0.3, 0.2 + scroll_position))
            yes_text.draw()
            no_text.setPos((0.3, 0.2 + scroll_position))
            no_text.draw()
            win.flip()

            if mouse.isPressedIn(yes_button):
                selected = "Yes"
            elif mouse.isPressedIn(no_button):
                selected = "No"

            core.wait(0.2)  # Debounce

        return selected
    
    # Helper function to display multiple-choice questions with scrolling
    def display_multiple_choice_question(question_text, options, allow_multiple=True, enable_text_input=False):
        nonlocal scroll_position
        question = visual.TextStim(win=win, text=question_text, pos=(0, 0.4 + scroll_position), height=0.04, color='black')
        option_buttons = []
        option_labels = []
        selected_options = set()

        # Create buttons and labels for each option
        for i, option in enumerate(options):
            button_pos_y = 0.2 - i * 0.1 + scroll_position
            button = visual.Circle(win, radius=0.03, pos=(-0.3, button_pos_y), lineColor='black')
            label = visual.TextStim(win=win, text=option, pos=(-0.1, button_pos_y), height=0.03, color='black')
            option_buttons.append(button)
            option_labels.append(label)

        # Optional text input field for "Prefer to Self Describe" - positioned statically
        if enable_text_input:
            text_input = TextBox(win, text='', font_size=32, font_color=[-1, -1, -1], size=(0.8, 0.2), pos=(0, -0.5))

        # Submit button
        submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
        submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.4), height=0.04, color='white')

        while True:
            # Handle scrolling in both directions
            scroll_wheel = mouse.getWheelRel()[1]
            scroll_position += scroll_wheel * 0.05
            scroll_position = max(min(scroll_position, max_scroll_position), min_scroll_position)

            # Draw question text
            question.setPos((0, 0.4 + scroll_position))
            question.draw()

            # Draw option buttons and labels
            for i, (button, label) in enumerate(zip(option_buttons, option_labels)):
                button.setPos((-0.3, 0.2 - i * 0.1 + scroll_position))
                label.setPos((-0.1, 0.2 - i * 0.1 + scroll_position))
                button.draw()
                label.draw()
                if i in selected_options:
                    button.fillColor = 'blue'
                else:
                    button.fillColor = None

            # Draw text input if enabled, with static position
            if enable_text_input:
                text_input.draw()

            # Draw the Submit button
            submit_button.setPos((0.7, -0.4 + scroll_position))
            submit_button_text.setPos((0.7, -0.4 + scroll_position))
            submit_button.draw()
            submit_button_text.draw()
            win.flip()

            # Handle option selection
            if mouse.getPressed()[0]:
                pos = mouse.getPos()
                for i, button in enumerate(option_buttons):
                    if button.contains(mouse):
                        if allow_multiple:
                            # Toggle selection
                            if i in selected_options:
                                selected_options.remove(i)
                            else:
                                selected_options.add(i)
                        else:
                            selected_options = {i}
                        core.wait(0.2)  # Debounce click

            # Check if the Submit button is clicked
            if mouse.isPressedIn(submit_button):
                core.wait(0.2)  # Debounce click
                break

        selected_text_options = [options[i] for i in selected_options]
        if enable_text_input:
            selected_text_options.append(text_input._text)  # Adjusted to use `_text`

        return ", ".join(selected_text_options)

    # Question 1: Have you ever sought psychological help?
    responses.append(display_yes_no_question("Have you ever sought psychological help from professionals like therapists or psychiatrists?"))

    if responses[-1] == "Yes":
        responses.append(display_multiple_choice_question(
            "Please choose the mental health diagnosis that best matches your condition(s). You can choose multiple options or self-describe.",
            mental_health_conditions, enable_text_input=True
        ))
        responses.append(display_multiple_choice_question(
            "Please describe the type of mental health treatment you required.",
            treatment_types, enable_text_input=True
        ))
    else:
        responses.extend(["", ""])

    # Question 2: Are you currently consulting a mental health professional?
    responses.append(display_yes_no_question("Are you currently consulting any mental health professional?"))

    if responses[-1] == "Yes":
        responses.append(display_multiple_choice_question(
            "Please choose the mental health diagnosis that best matches your current condition(s).",
            mental_health_conditions, enable_text_input=True
        ))
        responses.append(display_multiple_choice_question(
            "Select the frequency of your consultation.",
            ["SOS - Emergency need basis", "Once a month", "Twice a month", "Almost every week", "Once in 2 months", "Once in 3 months", "Once in 5 months", "Once in 6 months"]
        ))
    else:
        responses.extend(["", ""])

    # Question 3: Do you have a family member diagnosed with a mental illness?
    responses.append(display_yes_no_question("Do you have a family member or relative diagnosed with a mental illness?"))

    if responses[-1] == "Yes":
        responses.append(display_multiple_choice_question(
            "Please specify your relationship to the family member with a mental illness.",
            ["Sibling", "Cousin", "Parent", "Grandparent", "Uncle", "Aunt", "Partner", "Spouse", "Prefer to self-describe"],
            enable_text_input=True
        ))
    else:
        responses.append("")

    return responses


############################################################################################################################################################
'''                                                              PHQ - 9, GAD-7 SURVEY, SCORE PRESENTATION                                                                 
'''
############################################################################################################################################################

def display_health_survey_instructions():
    # Heading for the instruction page, similar to the "WELCOME" heading
    healthHeading = visual.TextStim(
        win=win, name='healthHeading',
        text="General Heath Survey",
        font='Arial',
        pos=(0, 0.4),  
        height=0.06, 
        color='black',
        colorSpace='rgb',
        opacity=1,
        alignText='center'
    )

    # Instruction text for the speech production task, matching the style of the welcome page
    healthInstructionsText = visual.TextStim(
        win=win,
        text=
        """
        In this final part of the study, we will ask you to complete a few brief surveys related to general health and well-being. \n

        Please take a moment to consider each question carefully and respond honestly based on your recent experiences. Your answers are invaluable to our research and will provide important insights into overall well-being.
        """,
        font='Arial',
        pos=(-0.45, -0.15), 
        height=text_size,  
        wrapWidth=1.1,
        color='black',       
        colorSpace='rgb',
        opacity=1,
        alignText='left'
    )

    # "Continue" button matching the style and position of the welcome page
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Start", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.10  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Update the position of the main text based on scroll_position
        healthHeading.setPos((0, 0.49 + scroll_position))
        healthInstructionsText.setPos((0, 0.18 + scroll_position))

        # Draw the heading, text, and button
        healthHeading.draw()
        healthInstructionsText.draw()
        continueButton.draw()
        continueButtonText.draw()
        win.flip()

        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        # Check if the continue button is clicked
        if mouse.isPressedIn(continueButton):
            debounce_click(mouse)  # Debounce to prevent accidental multiple clicks
            break


# PHQ-9 Survey Questions Setup
phq9_questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself or that you are a failure or have let yourself or your family down?",
    "Trouble concentrating on things, such as reading the newspaper or watching television?",
    "Moving or speaking so slowly that other people could have noticed. Or being so fidgety or restless that you've been moving around a lot more than usual?",
    "Thoughts that you would be better off dead, or of hurting yourself?"
]

phq9_options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

def display_phq9_survey():
    mouse = event.Mouse(visible=True, win=win)
    selected_answers_phq9 = [-1] * len(phq9_questions)  # Track selected answers

    # Instruction text at the top of the page
    instruction_text = visual.TextStim(
        win=win, 
        text="Over the last two weeks, how often have you been bothered by any of the of the follwoing problems?", 
        pos=(0, 0.9),  # Higher position to ensure visibility
        height=0.04, 
        color='black', 
        wrapWidth=1.5
    )

    # Define PHQ-9 option labels
    phq9_option_labels = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

    # Display PHQ-9 option labels at the top of the circular buttons
    option_label_texts = []
    option_horizontal_spacing = 0.25  # Adjusted spacing between labels
    text_size_small = 0.03  # Smaller text size for labels

    # Create labels for the options
    for i, label in enumerate(phq9_option_labels):
        label_pos = (-0.3 + i * option_horizontal_spacing, 0.75)  # Higher position above the buttons
        label_text = visual.TextStim(win=win, text=label, 
                                     pos=label_pos, 
                                     height=text_size_small, 
                                     color='black', 
                                     wrapWidth=0.2)
        option_label_texts.append(label_text)

    # Adjust vertical spacing for each question
    question_vertical_spacing = 0.19

    # Create visual elements for each question and its options
    question_texts = []
    option_buttons = []

    for idx, question in enumerate(phq9_questions):
        # Create question text on the left
        question_text = visual.TextStim(
            win=win, text=question, 
            pos=(-0.62, 0.6 - idx * question_vertical_spacing), 
            height=text_size_small, 
            wrapWidth=0.5, 
            color='black'
        )
        question_texts.append(question_text)

        # Create option buttons for each question on the right
        buttons = []
        for opt_idx in range(len(phq9_option_labels)):
            button_pos = (-0.3 + opt_idx * option_horizontal_spacing, 0.6 - idx * question_vertical_spacing)
            option_button = visual.Circle(win, radius=0.02, pos=button_pos, lineColor='black')
            buttons.append(option_button)
        option_buttons.append(buttons)

    # Add a Submit button at the bottom right
    submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.45))
    submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.8), height=0.04, color='white')

    # Scroll position variable
    scroll_position = -0.5
    scroll_step = 0.05  # Adjust to change the scroll speed

    while True:
        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * scroll_step

        # Draw instruction text (make sure it is drawn first)
        instruction_text.setPos((0, 0.9 + scroll_position))
        instruction_text.draw()

        # Draw option labels above the circular buttons
        for label in option_label_texts:
            label.setPos((label.pos[0], 0.75 + scroll_position))
            label.draw()

        # Draw questions and option buttons with scrolling
        for q_idx, question_text in enumerate(question_texts):
            question_text.setPos((-0.62, 0.6 + scroll_position - q_idx * question_vertical_spacing))
            question_text.draw()
            for opt_idx, option_button in enumerate(option_buttons[q_idx]):
                option_button.setPos((-0.3 + opt_idx * option_horizontal_spacing, 0.6 + scroll_position - q_idx * question_vertical_spacing))
                option_button.draw()
                if selected_answers_phq9[q_idx] == opt_idx:
                    visual.Circle(win, radius=0.02, pos=option_button.pos, fillColor='blue').draw()

        # Draw the Submit button
        submit_button.setPos((0.7, -0.935 + scroll_position))
        submit_button_text.setPos((0.7, -0.935 + scroll_position))
        submit_button.draw()
        submit_button_text.draw()

        win.flip()

        # Mouse interaction for selecting answers
        if mouse.getPressed()[0]:
            # debounce_click(mouse)
            pos = mouse.getPos()
            for q_idx, question_buttons in enumerate(option_buttons):
                for opt_idx, button in enumerate(question_buttons):
                    if button.contains(mouse):
                        selected_answers_phq9[q_idx] = opt_idx

        # Check if the Submit button is pressed and all questions are answered
        if -1 not in selected_answers_phq9 and mouse.isPressedIn(submit_button):
            debounce_click(mouse)
            break

    return selected_answers_phq9


# GAD-7 Survey Questions Setup
gad7_questions = [
    "Feeling nervous, anxious, or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it is hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?"
]

gad7_options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]


def display_gad7_survey():
    mouse = event.Mouse(visible=True, win=win)
    selected_answers_gad7 = [-1] * len(gad7_questions)  # Track selected answers

    # Instruction text at the top of the page
    instruction_text = visual.TextStim(
        win=win, 
        text="Over the last two weeks, how often have you been bothered by any of the following problems?", 
        pos=(0, 0.9),  # Higher position to ensure visibility
        height=0.04, 
        color='black', 
        wrapWidth=1.5
    )

    # Define GAD-7 option labels
    gad7_option_labels = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

    # Display GAD-7 option labels at the top of the circular buttons
    option_label_texts = []
    option_horizontal_spacing = 0.25  # Adjusted spacing between labels
    text_size_small = 0.03  # Smaller text size for labels

    # Create labels for the options
    for i, label in enumerate(gad7_option_labels):
        label_pos = (-0.3 + i * option_horizontal_spacing, 0.75)  # Higher position above the buttons
        label_text = visual.TextStim(win=win, text=label, 
                                     pos=label_pos, 
                                     height=text_size_small, 
                                     color='black', 
                                     wrapWidth=0.2)
        option_label_texts.append(label_text)

    # Adjust vertical spacing for each question
    question_vertical_spacing = 0.19

    # Create visual elements for each question and its options
    question_texts = []
    option_buttons = []

    for idx, question in enumerate(gad7_questions):
        # Create question text on the left
        question_text = visual.TextStim(
            win=win, text=question, 
            pos=(-0.62, 0.6 - idx * question_vertical_spacing), 
            height=text_size_small, 
            wrapWidth=0.5, 
            color='black'
        )
        question_texts.append(question_text)

        # Create option buttons for each question on the right
        buttons = []
        for opt_idx in range(len(gad7_option_labels)):
            button_pos = (-0.3 + opt_idx * option_horizontal_spacing, 0.6 - idx * question_vertical_spacing)
            option_button = visual.Circle(win, radius=0.02, pos=button_pos, lineColor='black')
            buttons.append(option_button)
        option_buttons.append(buttons)

    # Add a Submit button at the bottom right
    submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.62))
    submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.8), height=0.04, color='white')

    # Scroll position variable
    scroll_position = -0.55
    scroll_step = 0.05  # Adjust to change the scroll speed

    while True:
        # Handle scroll wheel input to update the scroll position
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * scroll_step

        # Draw instruction text (make sure it is drawn first)
        instruction_text.setPos((0, 0.9 + scroll_position))
        instruction_text.draw()

        # Draw option labels above the circular buttons
        for label in option_label_texts:
            label.setPos((label.pos[0], 0.75 + scroll_position))
            label.draw()

        # Draw questions and option buttons with scrolling
        for q_idx, question_text in enumerate(question_texts):
            question_text.setPos((-0.62, 0.6 + scroll_position - q_idx * question_vertical_spacing))
            question_text.draw()
            for opt_idx, option_button in enumerate(option_buttons[q_idx]):
                option_button.setPos((-0.3 + opt_idx * option_horizontal_spacing, 0.6 + scroll_position - q_idx * question_vertical_spacing))
                option_button.draw()
                if selected_answers_gad7[q_idx] == opt_idx:
                    visual.Circle(win, radius=0.02, pos=option_button.pos, fillColor='blue').draw()

        # Draw the Submit button
        submit_button.setPos((0.7, -0.55 + scroll_position))
        submit_button_text.setPos((0.7, -0.55 + scroll_position))
        submit_button.draw()
        submit_button_text.draw()

        win.flip()

        # Mouse interaction for selecting answers
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for q_idx, question_buttons in enumerate(option_buttons):
                for opt_idx, button in enumerate(question_buttons):
                    if button.contains(mouse):
                        selected_answers_gad7[q_idx] = opt_idx

        # Check if the Submit button is pressed and all questions are answered
        if -1 not in selected_answers_gad7 and mouse.isPressedIn(submit_button):
            debounce_click(mouse)
            break

    return selected_answers_gad7


# Define severity levels for PHQ-9 and GAD-7
def display_scores(phq9_score, gad7_score):
    # Determine PHQ-9 severity based on score
    if 1 <= phq9_score <= 4:
        phq9_severity = "Minimal depression"
    elif 5 <= phq9_score <= 9:
        phq9_severity = "Mild depression"
    elif 10 <= phq9_score <= 14:
        phq9_severity = "Moderate depression"
    elif 15 <= phq9_score <= 19:
        phq9_severity = "Moderately severe depression"
    elif 20 <= phq9_score <= 27:
        phq9_severity = "Severe depression"
    else:
        phq9_severity = "No significant depression"

    # Determine GAD-7 severity based on score
    if 0 <= gad7_score <= 4:
        gad7_severity = "Minimal anxiety"
    elif 5 <= gad7_score <= 9:
        gad7_severity = "Mild anxiety"
    elif 10 <= gad7_score <= 14:
        gad7_severity = "Moderate anxiety"
    elif 15 <= gad7_score <= 21:
        gad7_severity = "Severe anxiety"
    else:
        gad7_severity = "No significant anxiety"

    # Initialize TextStim for scores and recommendation text
    score_text = visual.TextStim(
        win=win,
        text=f"Your Score for PHQ-9 (Depression severity test) = {phq9_score}\n\n"
             f"Severity: {phq9_severity}\n\n\n"
             f"Your Score for GAD-7 (Anxiety Severity test) = {gad7_score}\n\n"
             f"Severity: {gad7_severity}\n\n",
        pos=(0, 0.4),  # Start position for scores
        height=0.04,
        color='black',
        wrapWidth=1.2,
        alignText='center'
    )

    recommendation_text = visual.TextStim(
        win=win,
        text="As per your score in our questionnaire, we could see some points for consideration "
             "regarding your mental health. However, our questionnaire is not designed to be used "
             "as a diagnostic tool. We recommend you to visit a qualified mental health professional "
             "for further exploration. You can share the brief of our research (as shared with you by "
             "our researcher) with the Mental Health Professional, and he/she/they can guide you further. "
             "You can proceed to the final test of the study by clicking \"Continue\".",
        pos=(0, -0.2),  # Position below the scores
        height=0.04,
        color='black',
        wrapWidth=1.2,
        alignText='left'
    )

    # "Continue" button
    continue_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continue_button_text = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

    # Make the screen scrollable
    scroll_position = -0.15
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Handle scrolling
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position += scroll_wheel * 0.03

        # Draw the score text and adjust position based on scroll
        score_text.setPos((0, 0.4 + scroll_position))
        recommendation_text.setPos((0, 0 + scroll_position))
        score_text.draw()
        recommendation_text.draw()

        # Draw "Continue" button at fixed position
        continue_button.draw()
        continue_button_text.draw()
        
        win.flip()

        # Check if "Continue" button is clicked
        if mouse.isPressedIn(continue_button):
            debounce_click(mouse)
            break



############################################################################################################################################################
'''                                                              THANK YOU NOTE [STUDY COMPLETION]                                                                 
'''
############################################################################################################################################################




############################################################################################################################################################
'''                                            ~ BEGINNING THE EXPERIMENT ~ (CALLING FUNCTIONS) & CSV MAKING                                                                 
'''
############################################################################################################################################################

# EXPERIMENT BEGINS [CALLING THE FIRST 3 PAGES]
display_welcome()
display_instructions()
display_consent_form()



# [CSV FILE SETUP]
csv_file = 'experiment_data_temp.csv'
file_exists = os.path.isfile(csv_file)

# Unique ID for participant
participant_id = str(uuid.uuid4())

# Add session start time
session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Prepare a list to store participant data for appending into one row
# Prepare a list to store participant data for appending into one row
participant_data = [participant_id, session_start_time]


selected_answers_panas = display_panas_survey()
participant_data.extend(selected_answers_panas)


# [CALLING SPEECH PERCEPTION TASK]
for i, audio_file in enumerate(audioStimuli):
    playCount, _ = present_stimulus(audio_file, i)
    valenceRating, valenceRT = rate_sam(
        samValenceButtons, valence_images, 
        visual.TextStim(win=win, text="How pleasant did the speaker’s voice sound in the audio clip? Please rate the emotion based on the scale below.\n (Press enter to next):", pos=(0, 0.4), height=0.05, color='black', wrapWidth = 1.4 ),
        "Extremely unpleasant", "Extremely pleasant"
    )
    arousalRating, arousalRT = rate_sam(
        samArousalButtons, arousal_images, 
        visual.TextStim(win=win, text="How energetic or excited did the speaker's voice sound in the audio clip?  Please rate the level of arousal on the scale below.\n (Press enter to next):", pos=(0, 0.4), height=0.05, color='black', wrapWidth = 1.4),
        "Low Arousal", "High Arousal"
    )
    
    participant_data.extend([audio_file, valenceRating, valenceRT, arousalRating, arousalRT, playCount])


# [CALLING THE SPEECH PRODUCITON TASK]
# First displaying instructions and then the speech recording task
# [CALLING THE SPEECH PRODUCTION TASK]
display_speech_production_instructions()
speech_production_data = run_speech_production_task(participant_id)
for audio_file, duration in speech_production_data:
    participant_data.extend([audio_file, duration])


# [CALLING DEMOGRAPHICS SURVEY - 1]
display_demographic_instructions()
selected_answers = display_demographic_questions()
age = age_input_box.text  # Get age input from the text box
participant_data.append(age)  # Append age to participant data
participant_data.extend(selected_answers)



# [CALLING DEMOGRAPHICS SURVEY - 2 - PSYCHOLOGICAL DEMOGRAPHICS]
responses = display_psych_demographics()

# Append responses to participant_data for CSV integration
participant_data.append(responses[0])  # Sought Psychological Help Yes/No
if responses[0] == "Yes":
    participant_data.append(responses[1])  # Mental Health Conditions
    participant_data.append(responses[2])  # Treatment Types
else:
    participant_data.extend(["", ""])  # Placeholders for No answer

participant_data.append(responses[3])  # Currently Consulting Yes/No
if responses[3] == "Yes":
    participant_data.append(responses[4])  # Current Mental Health Conditions
    participant_data.append(responses[5])  # Consultation Frequency
else:
    participant_data.extend(["", ""])  # Placeholders for No answer

participant_data.append(responses[6])  # Family Member Diagnosed Yes/No
if responses[6] == "Yes":
    participant_data.append(responses[7])  # Family Relationship
else:
    participant_data.append("")  # Placeholder for No answer


#[CALLING PHQ9, GAD7]
# [CALLING PHQ9, GAD7]
display_health_survey_instructions()
selected_answers_phq9 = display_phq9_survey()
participant_data.extend(selected_answers_phq9)
selected_answers_gad7 = display_gad7_survey()
participant_data.extend(selected_answers_gad7)

# Calculate total scores for PHQ-9 and GAD-7
phq9_score = sum(selected_answers_phq9)  # Assuming selected_answers_phq9 holds responses for PHQ-9
gad7_score = sum(selected_answers_gad7)  # Assuming selected_answers_gad7 holds responses for GAD-7

# Display the scores page
display_scores(phq9_score, gad7_score)



#[WRITING ALL THE DATA TO CSV]
# Write all data to CSV

# [WRITING ALL THE DATA TO CSV]
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)

    if not file_exists:
        header = ['Participant ID', 'Session Start Time']

        # PANAS Headers
        header.extend([f'PANAS_Q{i+1}' for i in range(20)])

        # Speech Perception Task Headers
        for i in range(len(audioStimuli)):
            header.extend([f'Stimuli Name {i+1}', f'Valence {i+1}', f'Valence RT {i+1}', 
                           f'Arousal {i+1}', f'Arousal RT {i+1}', f'Play Count {i+1}'])
        # Speech Production Task Headers
        for i in range(1, 4):
            header.extend([f'Paragraph {i} Audio File', f'Paragraph {i} Audio Duration'])
        # Demographic Survey - General
        header.extend(["Age", "Gender", "Education", "Language Proficiency", 
                       "Hearing Condition", "Hearing Assistance"])
        # Psychological Demographics
        header.extend([
            "Sought Psychological Help", 
            "Mental Health Conditions", 
            "Treatment Required",
            "Currently Consulting Professional", 
            "Current Mental Health Conditions", 
            "Consultation Frequency", 
            "Family Member Diagnosed", 
            "Family Relationship"
        ])
        

        # PHQ-9 and GAD-7 Headers
        header.extend([f'PHQ9_Q{i+1}' for i in range(9)])
        header.extend([f'GAD7_Q{i+1}' for i in range(7)])
        
        writer.writerow(header)

    writer.writerow(participant_data)
win.close()
core.quit()
