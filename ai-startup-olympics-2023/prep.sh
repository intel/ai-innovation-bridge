#!/bin/bash

wget https://www.mydrive.ch/shares/43421/11a215a5749fcfb75e331ddd5f8e43ee/download/420938129-1629953099/pill.tar.xz

mkdir models

tar -xf pill.tar.xz

mkdir -p data/{train/{good,bad},test/{good,bad},blind/}

cd pill/train/good/
cp $(ls | head -n 210) ../../../data/train/good/
cp $(ls | tail -n 65) ../../../data/test/good/

cd ../../../

cd pill/test/combined
cp $(ls | head -n 17) ../../../data/train/bad/
cp $(ls | tail -n 5) ../../../data/test/bad/

cd ../../../

cd pill/test/combined
cp $(ls | head -n 50) ../../../data/blind/

echo "completed data prep"
