#!/bin/bash
./render.py $@
RESULT=$?
if (! [[ $* == *-h* ]]) && [[ $RESULT -eq 0 ]];
then
    for f in jobs/*; do
    	qsub $f
    done
fi