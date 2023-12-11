#!/bin/bash
if ! [ -d video_frames ]
then
    mkdir video_frames
fi
for ((i=0; i<50; i++))
do
    if ! [ -d video_frames/${i}_frames ]
    then
        mkdir video_frames/${i}_frames
    else
        rm video_frames/${i}_frames/*
    fi
    ffmpeg -i ./videos/$i.mp4 -vf fps=1 video_frames/${i}_frames/out%d.jpg
done