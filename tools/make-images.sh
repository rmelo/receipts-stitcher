#!/bin/bash

printf "Proccess started.\n\n"

path=$1
opt=$2
original_path="$path/Original"
high_path="$path/High"
low_path="$path/Low"

if [ -d "$high_path" ]; then
    rm -rf $high_path
fi

if [ -d "$low_path" ]; then
    rm -rf $low_path
fi

echo "High and Low directories destroyed.   [ok]"

mkdir $high_path
mkdir $low_path

echo "Copying original files..."

cp $original_path/*.HEIC $high_path

echo "Original files copied.   [ok]"

echo "Converting to jpeg..."

mogrify -format jpeg ${high_path}/*.HEIC

echo "Files converted to jpeg format.   [ok]"

echo "Rotating images..."

mogrify -rotate -90 ${high_path}/*.jpeg

echo "Images rotated.	[ok]"

echo "Renaming files to sequence..."

rm ${high_path}/*.HEIC
i=0
for f in ${high_path}/*.jpeg;
    do 
        i=$(($i+1))
        mv $f "$high_path/receipt-$i.jpeg"
done

echo "Files renamed to sequence.   [ok]"

echo "Converting files to low format..."

cp $high_path/*.jpeg $low_path
mogrify -resize 75% $low_path/*.jpeg

echo "Files converted to low data format.   [ok]"

printf "\n\nProccess Complete!"
