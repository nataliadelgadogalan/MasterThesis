# MasterThesis

This repository contains the scripts employed to develop my master thesis. It is divided into folders to separate the different tasks

The first task was the generation of video containing the stimuli desired to carry out the experiments. I wrote a code to make sure 
all excepts had the same length and to have possibility of easily changing the length of pauses or stimuli, and to change some stimuli 
id desired.

The second is EEG feature extraction (still to be uploaded). OpenVibe is required for this part. It extracts alpha, beta, theta, gamma, 
and various combinations of arousal and valence comptured from the previous. These are the most relevant features to observe what we wish
in this project.

Third is to extract audio features. The 'Music Extractor' from Essentia (http://essentia.upf.edu/documentation/) is used for this task. 

Next, to avoid overfitting, feature selection is done. To avoid overfitting, it is recommended to use around 10% of samples, which were 
100 per audio. In this case we extract 12, to obtain 3 of each feature type: harmony, melody, rhythm, and timbre.

Finally, univariant and multivariant correlation are computed. There is one folder for each (still to be uploaded)
