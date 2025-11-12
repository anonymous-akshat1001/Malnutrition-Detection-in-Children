# I have images in different folders in the folder fulldataset : 
# back , frontal1 , frontal2 , frontal3, frontal4 , handswide , lateralleft , lateralright , selfie 
# This code merges them into a single new folder so that for each child the image is consecutive.

import os
import shutil
import pandas as pd

# Get the folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Point to the folder containing images folder relative to this script
ANTHROVISION_DIR = os.path.join(BASE_DIR, "Anthrovision")

# Now build all dataset paths relative to that
DATASET_ROOT = os.path.join(ANTHROVISION_DIR, "fulldataset")
CSV_PATH = os.path.join(ANTHROVISION_DIR, "anthrovision_labels.csv")
OUTPUT_FOLDER = os.path.join(ANTHROVISION_DIR, "merged_dataset")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read CSV file
df = pd.read_csv(CSV_PATH)

# Define the image columns
image_columns = [
    "image_path_frontal1",
    "image_path_frontal2",
    "image_path_frontal3",
    "image_path_frontal4",
    "image_path_back",
    "image_path_lateralleft",
    "image_path_lateralright",
    "image_path_selfie",
]

print(f"Found {len(df)} children in the CSV.")

# Loop to merge all the subfolders into a single folder for each child
for idx, row in df.iterrows():
    tag = str(row['tag'])

    # Create a subfolder for each child (optional)
    # child_folder = os.path.join(OUTPUT_FOLDER, tag)
    # os.makedirs(child_folder, exist_ok=True)

    for col in image_columns:
        img_path = row[col]
        # Skip missing entries
        if pd.isna(img_path) or not img_path.strip():
            continue  

        full_img_path = os.path.normpath(os.path.join(ANTHROVISION_DIR, img_path))

        if not os.path.exists(full_img_path):
            print(f"Missing file: {full_img_path}")
            continue

        # Construct new filename so that all images of the same child appear together
        new_filename = f"{idx:04d}_{tag}_{col}.jpg"          # Adds padding of 4 to child tag
        # Example path : 0001_childtag_image_path_frontal1.jpg

        # Output directory 
        new_path = os.path.join(OUTPUT_FOLDER, new_filename)

        # Copy image
        shutil.copy2(full_img_path, new_path)

print("Merging completed! All images copied to:", OUTPUT_FOLDER)


