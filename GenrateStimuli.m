clear all; close all; clc

%% GENERATE STIMULI VIDEO

%% PARAMETERS
% Duration of variables in seconds & working path (configurable parameters)
lenStimuli = 10; %(sec)
lenPause = 10;  %(sec)
workingDir = 'C:\Users\natad\Documents\SMC\MasterThesis\Stimuli\STIMULI_VIDEO';
videoFlag = 2; % 1 for first video, 2 for second video (to randomize non-coherent stimuli)

% Output filenames
audio_output_filename = 'Audio_Output.wav';
audio_filename_csv = 'audioFileNames.csv';
visual_output_filename = 'Video_Output.avi';
video_filename_csv = 'imageFileNames.csv';


%% CREATE VIDEO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
mainPath = [workingDir '\SelectedStimuli'];

%% GENERATE AUDIO %%
% Define silence and pause
[silence, fs_silence] = audioread('silence.wav');
pause = silence(1:(fs_silence*lenPause),:);
stimuli_silence = silence(1:(fs_silence*lenStimuli),:);
%filename = 'stimuli.mp4';
%fs = 4100;

%% Only One Stimuli Files %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Read files from folder
folderDir = [mainPath '\OnlyOneStimuli'];
cd(folderDir)
dirlist = dir('*.wav');
lenList = length(dirlist);

% Initialize audio output and list of filenames to output
audio = [];
fileNames_audio = strings((lenList*3)+3);

% Randomize audio files
r_index = randperm(lenList);

% Store audios & save the order in cvs file
fileNames_audio(1) = 'Only audio stimuli:';
for i = 1: lenList
    audio_filename = dirlist(r_index(i)).name;
    fileNames_audio(i+1) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y];
    audio = [audio; pause];
end

%% Add silence for images (only visual stimuli)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1: 12
    audio = [audio; pause];
    audio = [audio; stimuli_silence];
end

%% new audio order for coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
folderDir = [mainPath '\CoherentStimuli'];
cd(folderDir)
dirlist = dir('*.wav');
lenList = length(dirlist);

% Store audios & save the order in cvs file
r_index_coherent = randperm(lenList);
fileNames_audio(lenList+2) = 'Coherent audio+image stimuli:';
for i = 1: lenList
    audio_filename = dirlist(r_index_coherent(i)).name;
    fileNames_audio(i+lenList+2) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y; pause];
end

%% New audio order for non-coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%
folderDir = [mainPath '\NonCoherentStimuli'];
cd(folderDir)
dirlist = dir('*.wav');
lenList = length(dirlist);

% Random for non-coherent:
if videoFlag == 1
    r_index = [5 9 3 1 11 12 6 4 7 8 10 2];
elseif videoFlag == 2
    r_index = [8 5 3 10 6 1 11 4 12 9 2 7];
end

% Store audios & save the order in cvs file
fileNames_audio((lenList*2)+3) = 'Non coherent audio+image stimuli:';
for i = 1: lenList
    audio_filename = dirlist(r_index(i)).name;
    fileNames_audio(i+(2*lenList)+3) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y];
    audio = [audio; pause];
end

%% Write audio %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd ..
audiowrite(audio_output_filename,audio,fs);

%% Write audio file names in csv %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fid = fopen(audio_filename_csv, 'w');
fprintf(fid, 'Audio File Names: \n');
for i = 1: length(fileNames_audio)
    fprintf(fid, '%s\n', fileNames_audio(i));
end

fclose(fid) ;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%
%% CREATE IMAGES VIDEO %%
% Inititalize video (take )
mkdir(workingDir)
mkdir(workingDir,'images')

outputVideo = VideoWriter(fullfile(workingDir,visual_output_filename));
outputVideo.FrameRate = 30;
open(outputVideo)

folderDir = [mainPath '\OnlyOneStimuli'];
cd(folderDir)
dirlist = dir('*.jpg');
lenList = length(dirlist);
fileNames_image = strings((lenList*3)+3);

%% Add white image for only audio %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
img = imread(dirlist(1).name);
white = img;
white(:,:,:) = 255;
for ii = 1:lenList
   for j = 1: (lenStimuli + lenPause) * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

%% Only image stimuli %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
r_index = randperm(lenList);
fileNames_image(1) = 'Only image stimuli:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(dirlist(r_index(ii)).name);
       fileNames_image(ii+1) = dirlist(r_index(ii)).name;
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

%% New image order for coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
folderDir = [mainPath '\CoherentStimuli'];
cd(folderDir)
dirlist = dir('*.jpg');
lenList = length(dirlist);

fileNames_image(lenList+2) = 'Coherent audio+image stimuli:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(dirlist(r_index_coherent(ii)).name);
       fileNames_image(ii+lenList+2) = dirlist(r_index_coherent(ii)).name;
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

%% New image order for non-coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%
folderDir = [mainPath '\NonCoherentStimuli'];
cd(folderDir)
dirlist = dir('*.jpg');
lenList = length(dirlist);

% Random for non-coherent:
if videoFlag == 1
    r_index = [12 11 9 5 4 3 1 7 2 6 8 10];
elseif videoFlag == 2
    r_index = [6 10 7 9 1 4 5 8 2 12 11 3];
end


fileNames_image((lenList*2)+3) = 'Non coherent audio+image stimuli:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(dirlist(r_index(ii)).name);
       fileNames_image(ii+(lenList*2)+3) = dirlist(r_index(ii)).name;
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end
close(outputVideo)

%% Write image file names in csv %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd ..
fid = fopen(video_filename_csv, 'w');
fprintf(fid, 'Image File Names: \n');
for i = 1: length(fileNames_image)
    fprintf(fid, '%s\n', fileNames_image(i));
end

fclose(fid) ;

