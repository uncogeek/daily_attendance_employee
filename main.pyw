import re
from pathlib import Path
import pathlib
import pandas as pd
import os
import shutil
from tkinter.filedialog import askopenfilename
import common




common.file_cleaner()


# Open a dialog window and select a file
filename = askopenfilename()

# Extract the base name of the file (i.e., the file name without the path)
file_name = os.path.basename(filename)


# Define the destination path (root of the Python project)
destination_path = os.path.join(os.getcwd(), file_name)

# Copy the file to the destination path
shutil.copy(filename, destination_path)




p = Path(file_name)
#p = Path('3574203200056_attlog.dat')
p = p.rename(p.with_suffix('.txt'))

#Read file txt and replace spaces
# first get all lines from file
with open(p, 'r') as f:
    lines = f.readlines()



new_lines = []

# remove spaces



for line in lines:
    line = re.sub(r'1403-.*', '', line)
    line = line.strip()
    new_lines.append(line + "\n")


# finally, write lines in the file
with open('file.txt', 'w') as f:
    f.writelines(new_lines)


#clean lines
cleaned_numbers = []
with open('file.txt', 'r') as f:
    cleaned_numbers = [line.strip() for line in f]



#find name for every code we have
# Load the CSV file
file_path = 'database.csv'
df = pd.read_csv(file_path, header=None, names=['Number', 'Name'])

# Search for the name with the number 206
finalResult = []
for line in cleaned_numbers:
    line = line.strip()
    temp = df[df['Number'] == int(line)]
    finalResult.append(temp)

# Combine all results into a single DataFrame
result_df = pd.concat(finalResult)

# Extract only the 'Name' column
names = result_df['Name'].tolist()

# Get the count of results
count = len(names)

# Prepare the content for the output file
output_content = f"{count} نفر \n" + "\n".join(names)

# Write the output content to a text file
output_path = 'final_result.txt'
with open(output_path, 'w') as f:
    f.write(output_content)

print(f"Final results have been written to {output_path}")
common.file_cleaner()
os.rename('final_result.txt', 'آمار.txt')