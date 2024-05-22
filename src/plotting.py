'''
LANGUAGE ANALYTICS @ AARHUS UNIVERSITY, ASSIGNMENT 4: Emotion Analysis

AUTHOR: Louise Brix Pilegaard Hansen

DESCRIPTION:
This script takes an input .csv which contains emotion-labelled sentences and creates two plots;
one which shows the distribution of emotion labels for each season and one which shows the distribution
for each emotion label across all season
'''
# import required modules
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import argparse
import os 
from codecarbon import EmissionsTracker 
from codecarbon import track_emissions

# define emissionstracker to track CO2 emissions (for assignment 5)
tracker = EmissionsTracker(project_name="assignment4_subtasks_plotting",
                           experiment_id="plotting",
                           output_dir='emissions',
                           output_file="assignment4_plotting_subtasks_emissions.csv")

# define argument parser
def argument_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_csv', type=str, help='name of emotion-labelled csv file', default='GoT_labelled.csv')

    args = vars(parser.parse_args())
    
    return args


def create_frequency_df(count_df: pd.DataFrame) -> pd.DataFrame:

    '''
    Takes a df with counts per label per season and transforms the counts into relative frequencies for each season.

    Arguments:
        - count_df: Pandas DataFrame with counts per label per season
    
    Returns;
        - frequency_df: Pandas DataFrame with relative frequency for each label within each season.
    '''

# initialize empty list
    frequency_list =[]

    # loop over length of count_df (= number of seasons)
    for i in range(len(count_df)):

        # save only the columns containing counts (i.e., not 'seasons' column)
        only_counts = count_df.iloc[:, 1:]

        # divide each label's frequency for that season with the total number of sentences in that seasons
        frequency_row = only_counts.iloc[i] / sum(only_counts.iloc[i])
        frequency_list.append(frequency_row)
    
    # convert list to pandas df
    frequency_df = pd.DataFrame(frequency_list)
    
    return frequency_df

def plot_per_season(n_rows: int, n_cols: int, frequency_df: pd.DataFrame, emotion_labels: list):
    '''
    Takes the relative frequency of emotion labels for each season and plots them in a grid.
    Saves the plot in the /out folder.

    Arguments:
        - n_rows: number of rows in the grid-plot
        - n_cols: number of columns in the grid-plot
        - frequency_df: df with relative frequencies for each emotion label for each season
        - emotion_labels: available emotion labels 

    Returns:
        None
    '''
    
    # create subplots with n_rows and n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 20))

    # set colors for each label
    colors = ['red', 'olive', 'purple', 'green', 'orange', 'blue', 'pink']

    # create 'season' variable in order to loop over each season
    n = 0

    # for rows and columns in the grid
    for row in range(n_rows):
        for col in range(n_cols):

                # get distribution of emotion frequencies for that season
                frequencies = frequency_df.iloc[n]

                # plot barplot using relative frequencies
                axes[row][col].bar(emotion_labels, frequencies, color=colors)
                axes[row][col].set_title(f'Season {n + 1}') # +1 because n starts from 0
                axes[row][col].set_ylabel('Relative frequency')

                # add 1 to the 'season' variable to plot the next season in the next grid-space
                n += 1 
    
    # add title
    fig.suptitle('Relative frequency of emotion labels per season', size=24)
    fig.tight_layout()
    fig.subplots_adjust(top=0.92)

    # save in /out folder
    out_path = os.path.join('out', 'frequency_per_season.png')

    plt.savefig(out_path)

def plot_per_label(n_rows: int, n_cols: int, frequency_df: pd.DataFrame, emotion_labels: list):
    '''
    Plots the relative frequency of each emotion label across all seasons.
    Plot is saved in the /out folder

    Arguments:
        - n_rows: number of rows in the grid-plot
        - n_cols: number of columns in the grid-plot
        - frequency_df: df with relative frequencies for each emotion label for each season
        - emotion_labels: available emotion labels 
    
    Returns:
        - None
    '''

    # create subplots with n_rows and n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 20))

    # create list of seasons 1-8 for plotting
    seasons = [f'Season {i + 1}' for i in list(range(len(frequency_df)))]

    # create variable in order to loop over each season
    n = 0

    # for rows and columns in the grid
    for row in range(n_rows):
        for col in range(n_cols):

                # only need 7 plots, but the grid has 8 spaces
                if n >= 7:
                    axes[row][col].axis('off') # remove last grid so the eighth' subplot is empty
                
                else:
                    # get list of frequency of emotion label across all seasons
                    frequency = list(frequency_df.iloc[:, n])

                    # plot barplot using relative frequencies
                    axes[row][col].bar(seasons, frequency)
                    axes[row][col].set_title(emotion_labels[n])
                    axes[row][col].set_ylabel('Relative frequency')

                    # add 1 to the 'season' variable to plot the next season in the next grid-space
                    n += 1 

    # add title
    fig.suptitle('Relative frequency for each emotion across seasons', size=24)
    fig.tight_layout()
    fig.subplots_adjust(top=0.92)

    # save in out folder
    out_path = os.path.join('out', 'frequency_across_seasons.png')

    plt.savefig(out_path)

def plot_results(in_csv:str):
    '''
    This function first counts the relative frequencies of each emotion label for each season.
    It produces two plots; one which plots the relative frequency of each label for each season, and one
    which plots the releative frequency of each label across all seasons. The plots are saved in the /out folder
    
    Arguments:
        - in_csv: Name of csv file with emotion-labelled data
    
    Returns:
        None
    '''

    # define in-path and load labelled df
    in_path = os.path.join('in', in_csv)
    labelled_df = pd.read_csv(in_path)

    # save dataframe with count for each label for each season
    count_df = labelled_df.groupby(['Season', 'label']).size().unstack().reset_index()

    # create df with relative frequencies
    frequency_df = create_frequency_df(count_df)

    # save list of emotion labels
    emotion_labels = list(count_df.columns[1:])

    # track plotting task
    tracker.start_task('Plot results')

    # plot barplots of frequencies for labels per season
    plot_per_season(4, 2, frequency_df, emotion_labels)

    # plot barplots of frequency of each label across seasons
    plot_per_label(4, 2, frequency_df, emotion_labels)

    # stop tracking of task
    plotting_emissions = tracker.stop_task()

    print('Code finished: see plots in /out folder')

    # stop all tracking
    tracker.stop()

@track_emissions(project_name="assignment4_plotting_FULL",
                experiment_id="assignment4_plotting_FULL",
                output_dir='emissions',
                output_file="assignment4_plotting_FULL_emissions.csv")
def main():

    # load args
    args = argument_parser()

    # create plots and save in /out
    plot_results(args['in_csv'])

if __name__ == '__main__':
   main()
