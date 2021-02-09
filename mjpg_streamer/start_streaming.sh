#!/bin/sh

export LD_LIBRARY_PATH=/usr/local/lib

mkdir -p /tmp/stream
raspistill --nopreview -w 640 -h 480 -q 5 -o /tmp/stream/pic.jpg -tl 100 -t 0 -th 0:0:0 & 1>/dev/null 2>/tmp/stream/raspistill_logs.txt
mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" & 1>/dev/null 2>/tmp/stream/mjpg_streamer_logs.txt
