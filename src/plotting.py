'''
This script takes an input .csv which contains emotion-labelled sentences and creates two plots;
one which shows the distribution of emotion labels for each season and one which shows the distribution
of emotion labels across all seasons.
'''
# import required modules
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import argparse
import os 

# define argument parser
def argument_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument('--in_csv', type=str, help='name of emotion-labelled csv file', default='GoT_labelled.csv')

    args = vars(parser.parse_args())
    
    return args

def relative_frequencies(count_df, n_sentences):
    '''
    This function takes a grouped pandas dataframe object containing counts per season and turns it into relative frequencies.

    Arguments:
        - count_df: grouped pandas dataframe containg counts per season
        - n_sentences: total number of sentences per season

    Returns:
        frequencies_list: list containing lists of relative frequencies for each emotion label for each season.
    '''

    # create empty list
    frequencies_list = []

    # loop over length of count_df (i.e., number of seasons)
    for i in range(len(count_df)):
        
        # save counts for each emotion label for that season
        counts = list(count_df.iloc[i, 1:])

        # create empty list
        counts_freq = []

        # go through the count for each emotion label and turn it into relative frequency
        for n in counts:

            # divide by the total amount of sentences for that season
            freq = n / n_sentences[i]

            # append to list
            counts_freq.append(freq)

        # append relative frequencies to list
        frequencies_list.append(counts_freq)
    
    return frequencies_list

def plot_grid(n_rows, n_cols, frequencies_list, emotion_labels):
    '''
    Takes the relative frequency of emotion labels for each season and plots them in a grid.
    Saves the plot in the /out folder.

    Arguments:
        - n_rows: number of rows in the grid-plot
        - n_cols: number of columns in the grid-plot
        - frequencies_list: list of relative frequencies for each emotion label for each season
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
                # plot barplot using relative frequencies
                axes[row][col].bar(emotion_labels, frequencies_list[n], color=colors)
                axes[row][col].set_title(f'Season {n + 1}')
                axes[row][col].set_ylabel('Relative frequency')

                # add 1 to the 'season' variable to plot the next season in the next grid-space
                n += 1 
    
    # add title and save in /out folder
    fig.suptitle('Relative frequency of emotion labels per season', size=24)
    fig.tight_layout()
    fig.subplots_adjust(top=0.92)
    plt.savefig('out/frequency_per_season.png')

def plot_seasons_freq(labelled_df):
    '''
    This function counts the relative frequencies of each emotion label for each season and plots them in a grid.
    
    Arguments:
        - labelled_df: Pandas DataFrame with emotion-labelled data
    
    Returns:
        None

    '''
    # save dataframe with count for each label for each season
    count_df = labelled_df.groupby(['Season', 'label']).size().unstack().reset_index()

    # save list of total number of sentences for each season
    n_sentences = list(labelled_df.groupby('Season').size())

    # convert raw counts to relative frequencies
    frequencies_list = relative_frequencies(count_df, n_sentences)

    # save list of emotion labels
    emotion_labels = list(count_df.columns[1:])

    # plot barplot of frequencies for labels for each season
    plot_grid(4, 2, frequencies_list, emotion_labels)

def plot_freq_all(labelled_df):
    '''
    Counts and plots the relative frequency of emotion labels across all seasons.
    Plot is saved in the /out folder

    Arguments:
        - labelled_df: Pandas DataFrame with emotion-labelled data
    
    Returns:
        - None
    '''

    # get count of each emotion label across all seasons
    all_counts = list(labelled_df.groupby('label').size())

    # calculate relative frequencies by dividing by total amount of sentences
    rel_freqs = [n / len(labelled_df) for n in all_counts]

    # get list of labels (sorting them alphabetically)
    labels = list(np.sort(labelled_df['label'].unique()))

    # create plot
    fig, ax = plt.subplots()
    colors = ['red', 'olive', 'purple', 'green', 'orange', 'blue', 'pink']

    # create barplot with labels and relative frequencies
    ax.bar(labels, rel_freqs, color=colors)
    ax.set_ylabel('Relative frequency')
    ax.set_title('Relative frequency across all seasons')

    # save in out folder
    plt.savefig('out/frequency_across_seasons.png')

def main():

    # load args
    args = argument_parser()

    # define in-path and load labelled df
    in_path = os.path.join('in', args['in_csv'])
    labelled_df = pd.read_csv(in_path)

    # create plot of frequencies of labels for each season and save in /out
    plot_seasons_freq(labelled_df)

    # create plot of frequencies of labels across all seasons
    plot_freq_all(labelled_df)

    print('Code finished: see plots in /out folder')

if __name__ == '__main__':
   main()
