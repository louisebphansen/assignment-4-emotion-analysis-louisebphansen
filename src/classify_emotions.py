'''
This script takes an input .csv file containing sentences and gives it an emotion label using the
pretrained model 'j-hartmann/emotion-english-distilroberta-base' using a HuggingFace transfomer pipeline.
'''
# import required modules
import pandas as pd 
from transformers import pipeline 
from datasets import Dataset
import argparse
import os 
from transformers.pipelines.pt_utils import KeyDataset
from tqdm.auto import tqdm

# define argument parser
def argument_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_csv', type=str, help='name of .csv to extract emotion labels for', default = 'Game_of_Thrones_Script.csv')
    parser.add_argument('--out_csv', type=str, help = 'what to call the emotion-labelled csv file', default = 'GoT_labelled.csv')

    args = vars(parser.parse_args())
    
    return args

def classify_emotions(df):

    '''
    Function which assigns an emotion label for each text sentence in a dataset using a transformer pipeline

    Arguments:
        - df: dataset with rows containing sentences to assign emotion labels to
    
    Returns:
        Pandas dataframe with emotion label and score for each sentence
    '''

    # remove rows with NA value
    df_cleaned = df.dropna()

    # converting the dataset from pandas to HuggingFace dataset (recommended by HuggingFace in ther documentation)
    dataset = Dataset.from_pandas(df_cleaned)

    # loading pre-trained HuggingFace emotion classifier
    classifier = pipeline("text-classification", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    return_all_scores=False) # only return the most probably emotion label

    # initialize empty lists
    labels = []
    score = []

    # 
    for out in tqdm(classifier(KeyDataset(dataset, "Sentence"))):
        
        labels.append(out['label'])
        score.append(out['score'])

    # add labels and scores as new columns to DataFrame
    df_cleaned['label'] = labels 
    df_cleaned['score'] = score

    return df_cleaned

def main():

    # load args
    args = argument_parser()
    
    # define in path
    in_path = os.path.join('in', args['in_csv'])

    # read csv as pandas df
    df = pd.read_csv(in_path)

    # add emotion labels to df
    df_labelled = classify_emotions(df)

    # define out path
    out_path = os.path.join('in', args['out_csv'])

    # save labelled df
    df_labelled.to_csv(out_path)

if __name__ == '__main__':
   main()
