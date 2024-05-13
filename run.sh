# activate virtual environment
source ./env/bin/activate

# unzip data file (create /in folder with data)
unzip data.zip

# run script to add emotion labels to each sentence using default arguments
python src/classify_emotions.py

# create and save plots of emotion label frequencies using default arguments
python src/plotting.py

# deactivate virtual environment
deactivate