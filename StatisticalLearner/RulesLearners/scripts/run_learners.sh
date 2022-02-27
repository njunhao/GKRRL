#!/usr/bin/bash
# run this script in the folder where all the files are at
if [ $# == 1 ] 
then
	../bin/ruleslearners config.cfg ./ $1
else
	../bin/ruleslearners config.cfg ./
fi