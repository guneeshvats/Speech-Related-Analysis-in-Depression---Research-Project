import os
import pandas as pd
import librosa

# Constants
DATASET_DIR = "path/to/IEMOCAP"  # Replace with the path to your IEMOCAP dataset
OUTPUT_METADATA = "selected_stimuli.csv"
TARGET_EMOTIONS = ["happy", "sad", "neutral", "angry"]
SAMPLES_PER_CATEGORY = 25
MIN_DURATION = 7  # Minimum duration in seconds
MAX_DURATION = 10  # Maximum duration in seconds

def parse_annotations(session_dir):
    """
    Parse the IEMOCAP annotation files to extract metadata for each audio segment.
    Returns a DataFrame with relevant details (file path, emotion, valence, etc.).
    """
    metadata = []
    annotation_path = os.path.join(session_dir, "dialog/EmoEvaluation", "dialog_emotion.txt")
    
    with open(annotation_path, "r") as file:
        for line in file:
            if line.startswith("["):
                parts = line.strip().split()
                start, end = map(float, parts[0][1:-1].split("-"))
                file_id = parts[1]
                emotion = parts[2]
                # Skip emotions not in our target list
                if emotion not in TARGET_EMOTIONS:
                    continue
                metadata.append({
                    "path": os.path.join(session_dir, "sentences", "wav", file_id.split("_")[0], file_id + ".wav"),
                    "emotion": emotion,
                    "start_time": start,
                    "end_time": end
                })
    return pd.DataFrame(metadata)

def calculate_duration(row):
    """
    Calculate the duration of each audio segment and add it to the DataFrame.
    """
    try:
        duration = librosa.get_duration(filename=row['path'])
        return duration
    except Exception as e:
        print(f"Error calculating duration for {row['path']}: {e}")
        return None

def filter_by_duration(df):
    """
    Filter audio files that fall within the specified duration range.
    """
    df['duration'] = df.apply(calculate_duration, axis=1)
    return df[(df['duration'] >= MIN_DURATION) & (df['duration'] <= MAX_DURATION)]

def select_top_samples(df, emotion, gender_balanced=True):
    """
    Select the top stimuli based on valence ratings and gender balance.
    """
    samples = df[df['emotion'] == emotion]
    # Sort by valence (descending for happy and angry, ascending for sad, neutral centered)
    if emotion in ["happy", "angry"]:
        samples = samples.sort_values(by='valence', ascending=False)
    elif emotion == "sad":
        samples = samples.sort_values(by='valence', ascending=True)
    elif emotion == "neutral":
        samples = samples.loc[samples['valence'].abs().sort_values().index]

    if gender_balanced:
        male_samples = samples[samples['speaker_gender'] == 'male'].head(SAMPLES_PER_CATEGORY // 2)
        female_samples = samples[samples['speaker_gender'] == 'female'].head(SAMPLES_PER_CATEGORY // 2)
        return pd.concat([male_samples, female_samples])
    else:
        return samples.head(SAMPLES_PER_CATEGORY)

def main():
    # Prepare metadata from all sessions
    all_metadata = []
    for session in range(1, 6):
        session_dir = os.path.join(DATASET_DIR, f"Session{session}")
        session_metadata = parse_annotations(session_dir)
        all_metadata.append(session_metadata)
    
    # Combine metadata into a single DataFrame
    metadata = pd.concat(all_metadata, ignore_index=True)
    
    # Filter by duration
    print("Filtering by duration...")
    metadata = filter_by_duration(metadata)
    
    # Process each target emotion
    final_selection = []
    for emotion in TARGET_EMOTIONS:
        print(f"Selecting top samples for {emotion}...")
        emotion_samples = select_top_samples(metadata, emotion)
        final_selection.append(emotion_samples)
    
    # Save the selected metadata to a CSV file
    final_df = pd.concat(final_selection, ignore_index=True)
    final_df.to_csv(OUTPUT_METADATA, index=False)
    print(f"Selected stimuli saved to {OUTPUT_METADATA}")

if __name__ == "__main__":
    main()
