# Assignment 4 - Emotion analysis with pretrained language models

This assignment is the fourth assignment for the portfolio exam in the Language Analytics course at Aarhus University, spring 2024.

### Contributions

The code was written by me, but code provided in the notebooks for the course has been reused. 

### Assignment description

For this assignment, you should write code which does the following:

- Predict emotion scores for all lines in the data
- For each season
    - Plot the distribution of all emotion labels in that season
- For each emotion label
    - Plot the relative frequency of each emotion across all seasons

### Contents of the repository


| <div style="width:120px"></div>| Description |
|---------|:-----------|
|```in```| Contains the input csv files used for this assignment |
| ```out``` | Contains the output plots showing frequencies of emotion labels|
| ```src```  | Contains the Python scripts for assigning emotion labels to each sentence and plotting the distribution of these. |
| ```run.sh```    | Bash script for running all code with default arguments|
| ```setup.sh```  | Bash script for setting up virtual environment |
| ```requirements.txt```  | Packages required to run the code|

### Methods
This project contains the code to examine the emotion label of each sentence in a dataset of spoken lines in the Game of Thrones television series

More specifically, the script ```scr/classify_emotions.py``` takes an input csv file where each row represents a sentence and assigns an emotion label to these sentences. This is done using a HuggingFace classification [pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines), which uses the **j-hartmann/emotion-english-distilroberta-base** pretrained emotion classifier. Using the pipeline, the model can assign probabilities of each emotion label,
"anger", "disgust", "fear", "joy", "neutral", "sadness", and "surprise". The label with the highest probably is chosen as the sentence's 'emotion label' and added to the dataframe in a seperate column. The labelled dataframe is saved to a csv file in the ```/in``` folder as **GoT_labelled.csv**.

The script ```src/plotting.py``` takes this emotion-labelled dataframe and creates different visualizations. First, the relative frequencies for each emotion label for each season are calculated and plotted in a grid of barplots, which can be found at **out/frequency_per_season.png**. Next, relative frequencies for each emotion label *across* all seasons are calculated and plotted in a single barplot, which can be found at **out/frequency_across_seasons.png**.


### Data

The datasets consists of 22,300 sentences of spoken lines in all eight seasons of the Game of Thrones television series. The dataset can be found on [Kaggle](https://www.kaggle.com/datasets/albenft/game-of-thrones-script-all-seasons?select=Game_of_Thrones_Script.csv) and in the ```in``` folder of this repository. 

### Usage

All code for this assignment was designed to run on an Ubuntu 22.04 operating system using Python version 3.10.12. It is therefore not guaranteed that it will work on other operating systems.

It is important that you run all code from the main folder, i.e., *assignment-4-emotion-analysis-louisebphansen*. Your terminal should look like this:

```
--your_path-- % assignment-4-emotion-analysis-louisebphansen %
```

#### Set up virtual environment

To run the code in this repo, clone it using ```git clone```.

In order to set up the virtual environment, the *venv* package for Python needs to be installed first:

```
sudo apt-get update

sudo apt-get install python3-venv
```

Next, run:

```
bash setup.sh
```

This will create a virtual environment in the directory (```env```) and install the required packages to run the code.

#### Run code

To run the code, you can do the following:

##### Run script with predefined arguments

To run the code in this repo with predefined/default arguments, run:
```
bash run.sh
```

This will activate the virual environment and run the 
