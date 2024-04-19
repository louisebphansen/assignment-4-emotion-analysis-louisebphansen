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
| ```src```  | Contains the Python scripts for assigning emotion labels to each sentence and plotting the distribution of these |
| ```run.sh```    | Bash script for running all code with default arguments|
| ```setup.sh```  | Bash script for setting up virtual environment |
| ```requirements.txt```  | Packages required to run the code|

### Methods
This project contains the code to examine the emotion label of each sentence in a dataset of spoken lines in the Game of Thrones television series.

More specifically, the script ```src/classify_emotions.py``` takes an input csv file where each row represents a sentence and assigns an emotion label to these sentences. This is done using a HuggingFace classification [pipeline](https://huggingface.co/docs/transformers/main_classes/pipelines), which uses the **'j-hartmann/emotion-english-distilroberta-base'** pretrained emotion classifier. Using the pipeline, the model calculates probabilities of each emotion label,
"anger", "disgust", "fear", "joy", "neutral", "sadness", and "surprise". The label with the highest probably is chosen as the sentence's 'emotion label' and added to the dataframe in a seperate column. The labelled dataframe is saved to a csv file in the ```/in``` folder as **GoT_labelled.csv**.

The script ```src/plotting.py``` takes this emotion-labelled dataframe and creates different visualizations. First, the relative frequencies for each emotion label for each season are calculated and plotted in a grid of barplots, which can be found at **out/frequency_per_season.png**. Next, relative frequencies for each emotion label across all seasons are calculated and plotted in a grid of barplots, which can be found at **out/frequency_across_seasons.png**.


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

This will activate the virual environment and run the ```src/classify_emotions.py``` and ```src/plotting.py``` scripts with default arguments. The classification script outputs an emotion-labelled df, **in/GoT_labelled.csv** whereas the plotting script outputs two image files which can be found in the ```out``` folder.

##### Define arguments yourself

Alternatively, the script(s) can be run with different arguments:

```
# activate the virtual environment
source ./env/bin/activate

python3 src/classify_emotions.py --in_csv <in_csv> --out_csv <out_csv>

```

**Arguments:**

- **in_csv:** Name of .csv in ```in``` folder to extract emotion labels for. Default: 'Game_of_Thrones_Script.csv'
- **out_csv:** What to call the emotion-labelled, output csv file to be placed in ```in```. Default: 'GoT_labelled.csv'.

```
# activate the virtual environment
source ./env/bin/activate

python3 src/plotting.py --in_csv <in_csv>

```

**Arguments:**
- **in_csv:** Name of emotion-labelled csv file in ```in``` folder. Default: 'GoT_labelled.csv'.

### Results
![image](https://github.com/louisebphansen/assignment-4-emotion-analysis-louisebphansen/assets/75262659/e0c5d6ed-ab05-466c-8e0a-153091cfc257)

![image](https://github.com/louisebphansen/assignment-4-emotion-analysis-louisebphansen/assets/75262659/b089508b-f1c6-48ab-b7d4-6a45ccaa964f)

It is clearly evident that the most common emotion throughout the entire series is 'neutral'. This makes sense as there are probably a lot of sentences which doesn't have any emotional valence, but rather just someone saying *hello* or asking someone to bring out the horses. Interestingly, the most common emotions after 'neutral' are 'anger', 'disgust' and 'surprise'. 'anger' being the second-most frequent emotion is probably because Game of Thrones is a series containing a lot of hostility, violence and war-scenes. The frequency of the 'disgust' emotion probably also reflects this hostility as well as the disputes between the different houses which is one of the core themes throughout the series. 

When looking at the relative frequencies of labels across seasons (second plot), 'disgust' and 'sadness' stands out as the distribution of frequencies seem to change across seasons. The characters apparently express *less* disgust as the series progress towards the later seasons. Throughout seasons 3-6, it seems like the expression of sadness in spoken lines are increasing until reaching its maximum for season 6. Apparently, season 7 is the *least* sad season in Game of Thrones. When looking at the frequency of the 'anger' label across seasons, it is interesting that the frequency is highest in the final season (season 8), which could be because this is where some of the series' final battles are fought, resulting in many hostile and angry sentences spoken. 