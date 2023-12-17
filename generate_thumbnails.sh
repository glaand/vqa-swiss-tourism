#!/bin/bash

# Set the directory containing your images
input_directory="input/"

# Set the directory where you want to save the thumbnails
output_directory="output/"

# Set the size of the thumbnails (e.g., 100x100)
thumbnail_size="500x500"

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Generate thumbnails for each image in the input directory
for file in "$input_directory"/*; do
    # Get the filename and extension
    filename=$(basename "$file")
    extension="${filename##*.}"

    # Generate the thumbnail filename
    thumbnail_filename="${output_directory}/${filename%.*}.${extension}"

    # Generate the thumbnail
    convert "$file" -resize "$thumbnail_size^" -gravity center -extent "$thumbnail_size" "$thumbnail_filename"

    echo "Thumbnail generated for: $file"
done
