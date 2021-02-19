#!/bin/sh

rg="IoTPlayground"
hub="iothub-5736gv"
priority=$(date +"%y%m%d%H%M")
deployment="vision-edge-$priority"
condition="tags.type='raspberry-pi'"
az iot edge deployment create -g $rg --hub-name $hub -d $deployment --pri $priority --tc $condition -k config/deployment.json