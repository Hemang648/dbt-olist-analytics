import kagglehub
import shutil
import os

# Download dataset
path = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

# Your project folder
project_folder = r"E:\DBT PROJECT"

# Destination folder
destination = os.path.join(project_folder, "Brazilian_E-Commerce_Public_Dataset_by_Olist")

# Copy downloaded dataset into project folder
shutil.copytree(path, destination, dirs_exist_ok=True)

print("Dataset successfully saved to:", destination)

# Display downloaded files
for file in os.listdir(destination):
    print(file)
