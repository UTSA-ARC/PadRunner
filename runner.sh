#!/bin/sh

hd=$PWD
cd ~/PICode

if [ -e ./ABORTED ] 
then
    rm ./ABORTED
fi

./.venv/bin/python ./src/main.py

cd $hd
unset hd
