'''
LANGUAGE ANALYTICS @ AARHUS UNIVERSITY, ASSIGNMENT 4: Emotion Analysis

AUTHOR: Louise Brix Pilegaard Hansen

DESCRIPTION:
This script takes an input .csv file containing spoken sentences and gives it an emotion label using a
pretrained transfomer model using a HuggingFace pipeline.
'''
# import required modules
import pandas as pd 
from transformers import pipeline 
from datasets import Dataset
import argparse
import os 
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm
from codecarbon import EmissionsTracker 
from codecarbon import track_emissions

# define emissionstracker to track CO2 emissions (for assignment 5)
tracker = EmissionsTracker(project_name="assignment4_subtasks_classification",
                           experiment_id="classify_emotions",
                           output_dir='emissions',
                           output_file="assignment4_classification_subtasks_emissions.csv")

# define argument parser
def argument_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_csv', type=str, help='name of .csv to extract emotion labels for', default = 'Game_of_Thrones_Script.csv')
    parser.add_argument('--model', type=str, help='name of pre-trained emotion classifier available on HuggingFace', default = 'j-hartmann/emotion-english-distilroberta-base')
    parser.add_argument('--labelled_csv', type=str, help = 'what to call the emotion-labelled csv file', default = 'GoT_labelled.csv')

    args = vars(parser.parse_args())
    
    return args

def classify_emotions(df: pd.DataFrame, classifier) -> pd.DataFrame:

    '''
    Function which assigns an emotion label for each text sentence in a dataset using a HuggingFace classification pipeline

    Arguments:
        - df: dataset with rows containing sentences to assign emotion labels to
        - classifier: pre-trained HuggingFace emotion classification pipeline
    
    Returns:
        Pandas dataframe with emotion label and score for each sentence
    '''

    # remove rows with NA value
    df_cleaned = df.dropna()

    # converting the dataset from pandas to HuggingFace dataset (recommended by HuggingFace in ther documentation)
    dataset = Dataset.from_pandas(df_cleaned)

    # initialize empty lists
    labels = []
    scores = []

    # classify each sentence in dataset and save labels and scores to list (again, using the recommended method from HuggingFace pipeline documentation for optimal use)
    for out in tqdm(classifier(KeyDataset(dataset, "Sentence"))):
        
        try:
            labels.append(out['label'])
            scores.append(out['score'])
        
        except Exception as e:
            print(e)
            labels.append(pd.NA)
            scores.append(pd.NA)

    # add labels and scores as new columns to DataFrame
    df_cleaned['label'] = labels 
    df_cleaned['score'] = scores

    return df_cleaned

def assign_emotion_labels(in_csv:str, model:str, labelled_csv:str):

    '''
    Assign emotion labels to a dataframe column of text and save dataframe with assigned emotion labels to csv in /in folder 

    Arguments:
        - in_csv: name of .csv to extract emotion labels for
        - model: name of pre-trained emotion classifier available on HuggingFace
        - labelled_csv: what to call the emotion-labelled csv file

    Returns:
        None

    '''

    # define in path
    in_path = os.path.join('in', in_csv)

    # read csv as pandas df
    df = pd.read_csv(in_path)
       
    # track model loading
    tracker.start_task('Initializing HF classification pipeline')

    # loading pre-trained HuggingFace emotion classifier
    classifier = pipeline("text-classification", 
                    model=model, 
                    return_all_scores=False) # only return the most probable emotion label
    # stop tracker
    loading_emissions = tracker.stop_task()

    # track emotion classification
    tracker.start_task('Classifying emotions')

    # classify emotions and add emotion labels to df
    df_labelled = classify_emotions(df, classifier)

    # stop tracking of classification
    classification_emissions = tracker.stop_task()

    # define path
    labelled_data_path = os.path.join('in', labelled_csv)

    # save labelled df to csv
    df_labelled.to_csv(labelled_data_path)

    # stop all tracking
    tracker.stop()

# create new tracker using a decorator to track emissions for running the entire script
@track_emissions(project_name="assignment4_classification_FULL",
                experiment_id="assignment4_classification_FULL",
                output_dir='emissions',
                output_file="assignment4_classification_FULL_emissions.csv")
def main():

    # load args
    args = argument_parser()

    # assign emotion labels
    assign_emotion_labels(args['in_csv'], args['model'], args['labelled_csv'])

if __name__ == '__main__':
   main()
