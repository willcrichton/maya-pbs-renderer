#!/bin/bash
for file in /home/wcrichto/maya-output/**/*.jpg; do
    if [ "$(identify $file)" == "" ]; then 
	if [[ $# -ne 1 ]]; then
	    echo $file
	else
	    rm $file	    
	fi
    fi
done
