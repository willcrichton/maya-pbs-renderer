#!/bin/bash
rm -f *.o*
FAILED="$(find . -name '*.e*' | xargs -L 1 grep -l 'Maya exited' | sed -e 's/\.e.*/\.job/g')"
if [[ $FAILED =~ / ]]; then
    echo "not done :("

    while read line; do 
	qsub jobs/$line
	echo $line
    done <<< "$FAILED"
else
    echo "done for now";
fi
rm -f *.e*