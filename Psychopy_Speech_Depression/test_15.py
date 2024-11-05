'''
Need to add and adjust alignment
1. Demographic Survey Complete with alternate directions
2. Complete PHQ-9, GAD-7
3. Thank You Note (in end)
4. Recording Pages completely set 
5. CSV File output correctly 
6. Instruction pages for each tasks
7. proper Alignment of heading and paragraph on each page
8. Enter keys all 
'''

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
    text="""
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
    priyanka.srivastava@iiit.ac.in
    chiranjeevi.yarra@iiit.ac.in

    If you would like to know more, please proceed by clicking the 'Continue' button below.
    """,
    font='Arial', 
    pos=(-0.4, -0.35), 
    height=text_size, 
    wrapWidth=1.1, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')

# 'Continue' button for welcome page (positioned on the right side)
continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
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
    scroll_position = -0.34  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Set the position of both the heading and the main text based on scroll_position
        welcomeHeading.setPos((0, 0.77 + scroll_position))  # Adjust the y-position for the heading
        welcomeText.setPos((0, scroll_position))  # Adjust the y-position for the main text

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
    """
    Let me walk you through the process. Also, please read the given FAQ carefully.\n
    The study will last for around 40-45 minutes and consists of 5 tasks:\n
    - Emotion Perception Test\n
    - Language Fluency Test\n
    - Speech Production Test \n
    - Demographic Survey\n
    - Current Mood Assessment\n
    - General Health Questionnaire\n\n
    We will start the study with the Demographic information survey, followed by a Language fluency test and current mood assessment. Later in the survey, you will be asked to perceive the speaker's emotions from a series of audio files presented to you. Instructions about this task will be provided later. Finally, the study ends with a health survey to obtain general health measures. Each test is different in nature and hence the duration.\n\n
                    FREQUENTLY ASKED QUESTIONS (FAQ)\n
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
    Professors: 
    priyanka.srivastava@iiit.ac.in 
    chiranjeevi.yarra@iiit.ac.in.\n
    """,
    font='Arial', 
    pos=(-0.45, -0.35), 
    height=text_size, 
    wrapWidth=1.1, 
    color='black', 
    colorSpace='rgb', 
    opacity=1, 
    languageStyle='LTR', 
    alignText='left')

    understandButton = visual.Rect(win, width=0.3, height=0.07, fillColor='darkgreen', pos=(0.70, -0.4))
    understandButtonText = visual.TextStim(win=win, text="I Understand", pos=(0.70, -0.4), height=0.04, color='white')

    scroll_position = -1.44
    mouse = event.Mouse()

    while True:
        # Defining heading and its position in the page
        instructionsHeading.setPos((0, 1.81 + scroll_position))

        instructionsText.setPos((0, scroll_position))
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
    I hereby give my consent and permit members of the research team to access a de-identified version (with no mention of my name) of the data. The clinical information related to me will be used only for research purposes.\n\n
    I understand I will not be identified or identifiable in the report or reports that result from the research.\n\n
    I understand anonymized data can be shared in the public domain with other researchers worldwide.\n\n
    I have read the general information about the study and I have asked any questions regarding the procedure which have been satisfactorily answered. \n\n
    I am older than 18 years of age and no older than the age of 25.\n\n
    I understand the type of data being collected in this study and the reason for its collection. \n\n
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
        consentText.setPos((0, scroll_position))

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
        text="""Before proceeding with the tasks, we would like to collect some demographic information from you.\n\n
        This will include questions about your age, gender, language proficiency, and educational background.\n\n
        Please answer the following questions truthfully. The information will remain confidential and will only be used for research purposes.\n\n
        This survey will take around 5 minutes. After completing the survey, you will proceed to the main tasks of the study.\n\n
        If you are ready, click the 'Continue' button below to begin the demographic survey.""",
        font='Arial',
        pos=(-0.45, -0.35),  # Initial position
        height=text_size,  # Same text size as the welcome page
        wrapWidth=1.1,
        color='black',
        alignText='center'
    )

    # "Continue" button matching the style and position of the welcome page
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.10  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Update the position of the heading and main text based on scroll_position
        demographicHeading.setPos((0, 0.49 + scroll_position))
        demographicText.setPos((0, scroll_position))

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

# Define the demographic questions and options
demographic_questions = [
    {
        "question": "What is your age range?",
        "options": ["18-20", "21-23", "24-25", "Prefer not to say"]
    },
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
        0.5,  
        0.81,  
        0.74,
        0.60, 
        0.328,
        0.328
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
                                           pos=(button_pos[0] + 0.25, button_pos[1]), 
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

# Function to display the main psychological demographics questions
# Function to display psychological demographics with all conditional logic
def display_psych_demographics():
    mouse = event.Mouse(visible=True, win=win)
    scroll_position = 0  # Initial scroll position
    max_scroll_position = 1.0  # Adjust based on content

    # Loop through each psychological question
    for idx, question_data in enumerate(psych_demographics):
        question_text = visual.TextStim(
            win=win, text=question_data["question"],
            pos=(0, 0.4), height=0.04, wrapWidth=1.2, color='black'
        )
        options = question_data["options"]
        option_buttons = []
        option_labels = []

        # Create buttons and labels for "Yes" and "No"
        for i, option in enumerate(options):
            button = visual.Circle(win, radius=0.03, pos=(-0.3 + i * 0.6, 0.2), lineColor='black')
            label = visual.TextStim(win=win, text=option, pos=(button.pos[0] + 0.1, button.pos[1]), height=0.03, color='black')
            option_buttons.append(button)
            option_labels.append(label)

        selected_option = None

        # Wait for participant's response with full-screen scrolling
        while selected_option is None:
            scroll_wheel = mouse.getWheelRel()[1]
            scroll_position = max(min(scroll_position + scroll_wheel * 0.05, 0), -max_scroll_position)

            # Draw question and options with scrolling
            question_text.setPos((0, 0.4 + scroll_position))
            question_text.draw()
            for button, label in zip(option_buttons, option_labels):
                button.setPos((button.pos[0], button.pos[1] + scroll_position))
                label.setPos((label.pos[0], label.pos[1] + scroll_position))
                button.draw()
                label.draw()
            win.flip()

            if mouse.getPressed()[0]:
                for i, button in enumerate(option_buttons):
                    if button.contains(mouse):
                        selected_option = options[i]
                        responses.append(selected_option)
                        core.wait(0.2)  # Debounce to prevent multiple clicks
                        break

        # Conditional logic for question flow
        if idx == 0 and selected_option == "No":
            continue  # Skip further questions if "No" for first question

        if idx == 0 and selected_option == "Yes":
            display_scrollable_options(
                "If known, please choose the mental health diagnosis that best matches your condition(s):",
                mental_health_conditions, allow_multiple=True
            )
            display_scrollable_options(
                "If you have consulted the professional/s, please describe the kind of mental health treatment you required:",
                treatment_types, allow_multiple=True
            )

        # Logic for second question (Currently consulting)
        if idx == 1 and selected_option == "Yes":
            display_scrollable_options(
                "If you are consulting any mental health professionals, please choose the options that best match your frequency of consultation:",
                [
                    "SOS - Emergency need basis", "Once a month", "Twice a month",
                    "Almost every week/quite frequently", "Once in 2 months",
                    "Once in 3 months", "Once in 5 months", "Once in 6 months"
                ],
                allow_multiple=False
            )

        # Logic for third question (Familial relationship)
        if idx == 2 and selected_option == "Yes":
            display_scrollable_options(
                "How are you related to the family member or relative who has been diagnosed with mental illness?",
                ["Sibling", "Cousin", "Parent", "Grandparent", "Uncle", "Aunt", "Partner", "Spouse", "Prefer to self-describe"],
                allow_multiple=False, vertical_layout=True
            )

# Function to display scrollable options with vertical layout and full-screen scrolling
def display_scrollable_options(question, options, allow_multiple=False, vertical_layout=False):
    question_text = visual.TextStim(
        win=win, text=question,
        pos=(0, 0.4), height=0.04, wrapWidth=1.2, color='black'
    )
    mouse = event.Mouse(visible=True, win=win)
    option_buttons = []
    option_labels = []
    selected_indices = set()
    
    # Initial scroll position and limit
    scroll_position = 0
    max_scroll_position = min(len(options) * 0.1 - 0.5, 0)  # Ensure max scroll position does not go beyond content

    # Create buttons and labels for options
    for i, option in enumerate(options):
        pos_y = 0.3 - 0.1 * i if vertical_layout else 0.3 - 0.1 * (i // 2)
        pos_x = 0 if vertical_layout else -0.3 + (i % 2) * 0.6

        button = visual.Rect(win, width=0.5, height=0.05, pos=(pos_x, pos_y), lineColor='black', fillColor='lightgrey')
        label = visual.TextStim(win=win, text=option, pos=(pos_x, pos_y), height=0.03, color='black')
        option_buttons.append(button)
        option_labels.append(label)

    # "Submit" button at the bottom right
    submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.4), height=0.04, color='white')

    while True:
        # Handle scrolling
        scroll_wheel = mouse.getWheelRel()[1]
        scroll_position = max(min(scroll_position + scroll_wheel * 0.05, 0), max_scroll_position)

        # Draw question text and adjust for scrolling
        question_text.setPos((0, 0.4 + scroll_position))
        question_text.draw()

        # Draw options with scrolling
        for idx, (button, label) in enumerate(zip(option_buttons, option_labels)):
            new_y_pos = button.pos[1] + scroll_position
            button.setPos((button.pos[0], new_y_pos))
            label.setPos((label.pos[0], new_y_pos))
            button.draw()
            label.draw()
            if idx in selected_indices:
                button.fillColor = 'blue'
            else:
                button.fillColor = 'lightgrey'

        # Draw the "Submit" button
        submit_button.draw()
        submit_button_text.draw()
        win.flip()

        if mouse.getPressed()[0]:
            for idx, button in enumerate(option_buttons):
                if button.contains(mouse):
                    if allow_multiple:
                        if idx in selected_indices:
                            selected_indices.remove(idx)
                        else:
                            selected_indices.add(idx)
                    else:
                        selected_indices = {idx}
                    core.wait(0.2)  # Debounce

            if submit_button.contains(mouse):
                responses.append(", ".join([options[idx] for idx in selected_indices]))
                break




############################################################################################################################################################
'''                                                                     PHQ - 9, GAD-7 SURVEY                                                                 
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
        .\n
        In this task, you will be presented with a General Health Survey Measures. 
        Click Start to begin the test...
        """,
        font='Arial',
        pos=(-0.45, -0.35), 
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
        healthInstructionsText.setPos((0, scroll_position))

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

def display_phq9_survey():
    mouse = event.Mouse(visible=True, win=win)
    selected_answers_phq9 = [-1] * len(phq9_questions)  # Track selected answers

    # Instruction text at the top of the page
    instruction_text = visual.TextStim(
        win=win, 
        text="Please select how often you have been bothered by the following problems over the last two weeks:", 
        pos=(0, 0.9),  # Higher position to ensure visibility
        height=0.04, 
        color='black', 
        wrapWidth=1.5
    )

    # Define PHQ-9 option labels
    phq9_option_labels = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

    # Display PHQ-9 option labels at the top of the circular buttons
    option_label_texts = []
    option_horizontal_spacing = 0.22  # Adjusted spacing between labels
    text_size_small = 0.03  # Smaller text size for labels

    # Create labels for the options
    for i, label in enumerate(phq9_option_labels):
        label_pos = (-0.3 + i * option_horizontal_spacing, 0.75)  # Higher position above the buttons
        label_text = visual.TextStim(win=win, text=label, pos=label_pos, height=text_size_small, color='black')
        option_label_texts.append(label_text)

    # Adjust vertical spacing for each question
    question_vertical_spacing = 0.3

    # Create visual elements for each question and its options
    question_texts = []
    option_buttons = []

    for idx, question in enumerate(phq9_questions):
        # Create question text on the left
        question_text = visual.TextStim(
            win=win, text=question, 
            pos=(-0.62, 0.6 - idx * question_vertical_spacing), 
            height=text_size_small, 
            wrapWidth=0.6, 
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
    submit_button = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.8))
    submit_button_text = visual.TextStim(win=win, text="Submit", pos=(0.7, -0.8), height=0.04, color='white')

    # Scroll position variable
    scroll_position = 0
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
        submit_button.setPos((0.7, -0.8 + scroll_position))
        submit_button_text.setPos((0.7, -0.8 + scroll_position))
        submit_button.draw()
        submit_button_text.draw()

        win.flip()

        # Mouse interaction for selecting answers
        if mouse.getPressed()[0]:
            pos = mouse.getPos()
            for q_idx, question_buttons in enumerate(option_buttons):
                for opt_idx, button in enumerate(question_buttons):
                    if button.contains(mouse):
                        selected_answers_phq9[q_idx] = opt_idx

        # Check if the Submit button is pressed and all questions are answered
        if -1 not in selected_answers_phq9 and mouse.isPressedIn(submit_button):
            break

    return selected_answers_phq9


############################################################################################################################################################
'''                                                                       SPEECH PERCEPTION TASK                                                                  
'''
############################################################################################################################################################

# SAM SCALE 
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
def present_stimulus(audio_file, audio_index):
    playCount = 0
    stim = sound.Sound(value=audio_file)
    reaction_clock = core.Clock()

    # Prompt Text at the top of the screen
    promptText = visual.TextStim(
        win=win,
        text="Please click the 'Play' button to listen to the audio file.",
        font='Arial',
        pos=(0, 0.2),  # Position it above the play button
        height=text_size,
        wrapWidth=1.5,
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
        keys = event.getKeys(['space'])
        if 'space' in keys:
            rt = reaction_clock.getTime()
            break
    
    return playCount, rt

# Stimuli loop setup
audioStimuli = ['audio_1.wav', 'audio_2.wav']


#############################################################################################
'''SPEECH PRODUCTION TASK INSTRUCTION PAGE'''
#############################################################################################
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
        """
        You are about to begin the Speech Production Task.\n
        In this task, you will be presented with a series of paragraphs. Your goal is to read each paragraph aloud while recording your voice.\n\n
        Please make sure to speak clearly and at a natural pace. Once you are ready to record, click the 'Record' button.\n\n
        You can stop the recording by clicking the button again. Make sure to complete reading each paragraph before stopping the recording.\n\n
        When you are ready to begin, click the 'Continue' button below.
        """,
        font='Arial',
        pos=(-0.45, -0.35), 
        height=text_size,  
        wrapWidth=1.1,
        color='black',       
        colorSpace='rgb',
        opacity=1,
        alignText='left'
    )

    # "Continue" button matching the style and position of the welcome page
    continueButton = visual.Rect(win, width=0.2, height=0.07, fillColor='darkgreen', pos=(0.7, -0.4))
    continueButtonText = visual.TextStim(win=win, text="Continue", pos=(0.7, -0.4), height=0.04, color='white')

    scroll_position = -0.10  # Initial scroll position
    mouse = event.Mouse(visible=True, win=win)

    while True:
        # Update the position of the main text based on scroll_position
        speechHeading.setPos((0, 0.49 + scroll_position))
        speechInstructionsText.setPos((0, scroll_position))

        # Draw the heading, text, and button
        speechHeading.draw()
        speechInstructionsText.draw()
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

#############################################################################################
'''SPEECH PRODUCTION TASK (Audio Recording)'''
#############################################################################################
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



# EXPERIMENT BEGINS [CALLING AND CSV MAKING]
display_welcome()
display_instructions()
display_consent_form()



# CSV fFILE SETUP 
csv_file = 'experiment_data_temp.csv'
file_exists = os.path.isfile(csv_file)

# Unique ID for participant
participant_id = str(uuid.uuid4())

# Add session start time
session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Prepare a list to store participant data for appending into one row
participant_data = [participant_id, session_start_time]

# Present each stimulus and gather ratings
for i, audio_file in enumerate(audioStimuli):
    playCount, _ = present_stimulus(audio_file, i)
    
    # Collect ratings and reaction times
    valenceRating, valenceRT = rate_sam(samValenceButtons, valence_images, 
        visual.TextStim(win=win, text="How pleasant was the speaker's voice in the provided audio file? (Press enter to next):", pos=(0, 0.4), height=0.05, color='black'))
    arousalRating, arousalRT = rate_sam(samArousalButtons, arousal_images, 
        visual.TextStim(win=win, text="How excited was the speaker's voice in the provided audio file? (Press enter to next):", pos=(0, 0.4), height=0.05, color='black'))

    # Append data for this stimulus
    participant_data.extend([audio_file, valenceRating, valenceRT, arousalRating, arousalRT, playCount])


# First displaying instructions and then the speech recording task
display_speech_production_instructions()
# After audio stimuli, run the speech production task
speech_production_data = run_speech_production_task(participant_id)
for audio_file, duration in speech_production_data:
    participant_data.extend([audio_file, duration])

# # Add the speech production data to the participant data list
# for i, speech_data in enumerate(speech_production_data):
#     participant_data.append(speech_data)

# Display demographic instructions page before the demographic survey starts
display_demographic_instructions()
selected_answers = display_demographic_questions()
# participant_data.append(selected_answers)
participant_data.extend(selected_answers)



display_psych_demographics()
# Add psychological demographics
# Append the first three responses
# Collect psychological demographics responses
participant_data.extend(responses[:3])  # First three responses: "Sought Help", "Consulting Professional", "Familial Relationship"

# Logic to handle "Yes" or "No" answers
if responses[0] == "Yes":  # If "Sought Help" is Yes
    participant_data.append(responses[3] if len(responses) > 3 else "")  # Mental Health Conditions
    participant_data.append(responses[4] if len(responses) > 4 else "")  # Treatment Types
else:  # If "Sought Help" is No
    participant_data.extend(["", ""])  # Add empty strings for these columns




# Display PHQ-9 Survey after the demographic survey
display_health_survey_instructions()
selected_answers_phq9 = display_phq9_survey()
participant_data.extend(selected_answers_phq9)


# Write data to CSV
with open(csv_file, mode='a', newline='') as file:
    writer = csv.writer(file)

    if not file_exists:
        # Define header row with all necessary columns
        header = ['Participant ID', 'Session Start Time']
        for i in range(len(audioStimuli)):
            header.extend([f'Stimuli Name {i+1}', f'Valence {i+1}', f'Valence RT {i+1}', 
                           f'Arousal {i+1}', f'Arousal RT {i+1}', f'Play Count {i+1}'])
        for i in range(1, 4):
            header.extend([f'Paragraph {i} Audio File', f'Paragraph {i} Audio Duration'])
        header.extend(["Age", "Gender", "Education", "Language Proficiency", 
                       "Hearing Condition", "Hearing Assistance"])
        header.extend([
            "Sought Psychological Help", 
            "Currently Consulting Professional", 
            "Familial Relationship to Mental Illness", 
            "Mental Health Conditions", 
            "Treatment Types"
        ])
        header.extend([f'PHQ9_Q{i+1}' for i in range(9)])
        writer.writerow(header)

    # Write participant data
    writer.writerow(participant_data)


win.close()
core.quit()
