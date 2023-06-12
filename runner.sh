#!/bin/sh

hd=$PWD
cd ~/PICode

if [ -e ~/PICode/ABORTED ] 
then
    rm ~/PICode/ABORTED
fi

if ! screen -list | grep -q "picode"
then
    screen -A -m -d -S picode ./.venv/bin/python ./src/main.py
fi

screen -r

cd $hd
unset hd
