#!/bin/sh

# Kill raspistill process
process=$(ps aux | grep raspistill)
pid=$(echo $process | cut -d " " -f 2)
echo $process
echo Killing process id $pid
kill -9 $pid

# Kill mjpg_streamer process 
process=$(ps aux | grep mjpg_streamer)
pid=$(echo $process | cut -d " " -f 2)
echo $process
echo Killing process id $pid
kill -9 $pid
