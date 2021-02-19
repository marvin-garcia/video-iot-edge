#!/bin/sh

module=$1
tag=$2
arch=$3
imagename=$(echo "$module" | tr '[:upper:]' '[:lower:]')
relativedir=`dirname $0`

cd $relativedir/modules/$module/
docker build -t marvingarcia/$imagename:$tag -f ./Dockerfile.$arch .
docker push marvingarcia/$imagename:$tag