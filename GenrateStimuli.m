clear all; close all; clc

%% GENERATE STIMULI VIDEO

%% VARIABLES
% duration variables in seconds
lenStimuli = 10; 
lenPause = 5; 

[silence, fs_silence] = audioread('silence.wav');
pause = silence(1:(fs_silence*lenPause),:);
stimuli_silence = silence(1:(fs_silence*lenStimuli),:);
audio_output_filename = 'audioOutput.wav';
visual_output_filename = 'visualOutput.jpg';

filename = 'stimuli.mp4';
addpath( 'C:\Users\natad\Documents\SMC\Master Thesis\Stimuli\STIMULI_VIDEO\SelectedStimuli');
%addpath('C:/Users/natad/Documents/SMC/Master Thesis/Stimuli/STIMULI_VIDEO/SelectedStimuli');

fs = 4100;

%% CREATE VIDEO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% GENERATE AUDIO %%
% read files from folder
cd 'C:\Users\natad\Documents\SMC\Master Thesis\Stimuli\STIMULI_VIDEO\SelectedStimuli'
dirlist = dir('*.wav');
lenList = length(dirlist);
audio = [];
fileNames_audio = strings((lenList*3)+3);

% Randomize audio files
r_index = randperm(lenList);

% store audios
fileNames_audio(1) = 'Only audio stimuli:';
for i = 1: lenList
    audio_filename = dirlist(r_index(i)).name;
    fileNames_audio(i+1) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y];
    audio = [audio; pause];
end
%add silence for images
for i = 1: 12
    audio = [audio; pause];
    audio = [audio; stimuli_silence];
end

% new audio order for coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% store audios
r_index_coherent = randperm(lenList);
fileNames_audio(lenList+2) = 'Coherent audio+image stimuli:';
for i = 1: lenList
    %audio_filename = dirlist(r_index_coherent(i)).name;
    audio_filename = dirlist(i).name;
    fileNames_audio(i+lenList+2) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y; pause];
   % audio = [audio; pause];
end

% new audio order for non-coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Randomize audio files
r_index = randperm(lenList);

% store audios
fileNames_audio((lenList*2)+3) = 'Non coherent audio+image stimuli:';
for i = 1: lenList
    audio_filename = dirlist(r_index(i)).name;
    fileNames_audio(i+(2*lenList)+3) = audio_filename;
    [y,fs] = audioread(audio_filename);
    y = y(1:(fs*lenStimuli),:);
    audio = [audio; y];
    audio = [audio; pause];
end

%sound(audio,fs)

% write audio %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
cd ..
audiowrite(audio_output_filename,audio,fs);

% write audio file names %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fid = fopen('audioFileNames.csv', 'w');
fprintf(fid, 'Audio File Names: \n');
for i = 1: length(fileNames_audio)
    fprintf(fid, '%s\n', fileNames_audio(i));
end

fclose(fid) ;

%% CREATE IMAGES VIDEO %%

workingDir = 'C:\Users\natad\Documents\SMC\Master Thesis\Stimuli\STIMULI_VIDEO';
mkdir(workingDir)
mkdir(workingDir,'images')

shuttleVideo = VideoReader('imageStimuliOutput.avi');

ii = 1;

while hasFrame(shuttleVideo)
   img = readFrame(shuttleVideo);
   filename = [sprintf('%03d',ii) '.jpg'];
   fullname = fullfile(workingDir,'images',filename);
   imwrite(img,fullname)    % Write out to a JPEG file (img1.jpg, img2.jpg, etc.)
   ii = ii+1;
end


outputVideo = VideoWriter(fullfile(workingDir,'shuttle_out.avi'));
outputVideo.FrameRate = shuttleVideo.FrameRate;
open(outputVideo)

imageNames = dir(fullfile(workingDir,'SelectedStimuli','*.jpg'));
imageNames = {imageNames.name}';
lenList = length(imageNames);
fileNames_image = strings((lenList*3)+3);

% add white image for only audio %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
img = imread(fullfile(workingDir,'SelectedStimuli',imageNames{1}));
white = img;
white(:,:,:) = 255;
for ii = 1:lenList
   for j = 1: (lenStimuli + lenPause) * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

% only image stimuli %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
r_index = randperm(lenList);
fileNames_image(1) = 'Only image stimuli:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(fullfile(workingDir,'SelectedStimuli',imageNames{r_index(ii)}));
       fileNames_image(i+1) = imageNames{r_index(ii)};
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

% new image order for coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fileNames_image(1) = 'Coherent audio+image:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(fullfile(workingDir,'SelectedStimuli',imageNames{r_index_coherent(ii)}));
       fileNames_image(i+lenList+2) = imageNames{r_index(ii)};
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end

% new image order for non-coherent audio+image %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
r_index = randperm(lenList);
fileNames_image(1) = 'Non-coherent audio+image:';
for ii = 1:lenList
   for j = 1: lenStimuli * outputVideo.FrameRate
       img = imread(fullfile(workingDir,'SelectedStimuli',imageNames{r_index(ii)}));
       fileNames_image(i+(lenList*2)+3) = imageNames{r_index(ii)};
       writeVideo(outputVideo,img)
   end
   for j = 1: lenPause * outputVideo.FrameRate
       writeVideo(outputVideo,white)
   end
end
close(outputVideo)

% write image file names %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fid = fopen('imageFileNames.csv', 'w');
fprintf(fid, 'Image File Names: \n');
for i = 1: length(fileNames_image)
    fprintf(fid, '%s\n', fileNames_image(i));
end

fclose(fid) ;


% %initalize video
% v = VideoWriter(visual_output_filename, 'Archival');
% v.FrameRate = 1; 
%     %movie = avifile(filename, 'fps', 10, 'compression', 'none');
% open(v)
% 
% 
% % add blanc image for audio
% cd 'C:\Users\natad\Documents\SMC\Master Thesis\Stimuli\STIMULI_VIDEO\SelectedStimuli'
% white = imread('C1.jpg');
% 
% for v = 1:(lenStimuli + lenPause)*12
%    %frame=getframe(white);
%    writeVideo(v,white)
% end
% 
% % add first images
% dirlist = dir('*.jpg');
% for i =  1: len(dirlist)
%     imag_filename = dirlist.name(i);
%     image = imread(imag_filename);
%     writeVideo(v,image);
%     %frame = im2frame(image);
%     %movie = addframe(movie, frame);
%     for v = 1:lenStimuli
%         writeVideo(v,image)
%     end
% end
% %close
% close(v)
%     %movie = close(movie);
