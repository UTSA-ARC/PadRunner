#!/bin/sh

hd=$PWD
cd ~/PICode

if [ -e ./ABORTED ] 
then
    rm ./ABORTED
fi

screen -A -m -d -S picode ./.venv/bin/python ./src/main.py
screen -r

cd $hd
unset hd
