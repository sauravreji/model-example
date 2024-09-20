import os
from tqdm import tqdm

def csv_files_in_dir(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and os.path.isfile(os.path.join(directory, filename)):
            files.append(filename)
    return files

folder_path = "/Users/sauravreji/Internship/model"
output_file_train = "output_train.csv"
output_file_val = "output_val.csv"
vocab_file = "vocab.txt"

files = csv_files_in_dir(folder_path)
total_files = len(files)

split_index = int(total_files * 0.9) ##90% for training and 10% for validation
files_train = files[:split_index]
files_val = files[split_index:]
vocab = set()


with open(output_file_train, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_train,total = len(files_train)):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)
    
with open(output_file_val, "w", encoding="utf-8") as outfile:
    for filename in tqdm(files_val,total = len(files_val)):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)



with open(vocab_file, "w", encoding="utf-8") as vfile:
    for char in sorted(vocab):
        vfile.write(char + "\n")