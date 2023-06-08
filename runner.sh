#!/bin/sh

hd=$PWD 
cd ~/PICode
./.venv/bin/python ./src/main.py

cd $hd
unset hd
