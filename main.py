import re
from pathlib import Path
import pathlib
import pandas as pd
import os
import shutil
from tkinter.filedialog import askopenfilename
import xlsxwriter
from datetime import datetime

#Function: remove temporary txt and Dat files to cleanup folder
def file_cleaner():
    dir_name = pathlib.Path().resolve()
    #dir_name = "/Users/John/downloads/"
    get_file_in_directory = os.listdir(dir_name)
    for item in get_file_in_directory:
        if item.endswith(".txt"):
            if(item != "final_result.txt"):
                os.remove(os.path.join(dir_name, item))
        elif item.endswith(".dat"):
                os.remove(os.path.join(dir_name, item))


#Function: gonvert Gregorian date to Jalali (Shamsi)
def gregorian_to_jalali(gy, gm, gd):
 g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
 if (gm > 2):
  gy2 = gy + 1
 else:
  gy2 = gy
 days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
 jy = -1595 + (33 * (days // 12053))
 days %= 12053
 jy += 4 * (days // 1461)
 days %= 1461
 if (days > 365):
  jy += (days - 1) // 365
  days = (days - 1) % 365
 if (days < 186):
  jm = 1 + (days // 31)
  jd = 1 + (days % 31)
 else:
  jm = 7 + ((days - 186) // 30)
  jd = 1 + ((days - 186) % 30)
 return [jy, jm, jd]


                
#Convert Today Gregorian date to Jalali
year =  datetime.today().strftime('%Y')
month =  datetime.today().strftime('%m')
day =  datetime.today().strftime('%d')
jalali_date = gregorian_to_jalali(int(year), int(month), int(day))
jalali_date = str(jalali_date[0]) + "-" + str(jalali_date[1]) + "-" + str(jalali_date[2])
print(f"Today: {jalali_date}")


#Clean folder from mass and unwanted files such as files created before
file_cleaner()

# Open a dialog window and select a file
filename = askopenfilename()

# Extract the base name of the file (i.e., the file name without the path)
file_name = os.path.basename(filename)

# Define the destination path (root of the Python project)
destination_path = os.path.join(os.getcwd(), file_name)

# Copy the file to the destination path
shutil.copy(filename, destination_path)




p = Path(file_name)
#it means: p = Path('3574203200056_attlog.dat')

# Convert Dat file to Txt file
# .Dat file is the file we Exported from attendance device
p = p.rename(p.with_suffix('.txt'))


# get all string lines from file
with open(p, 'r') as f:
    lines = f.readlines()

new_lines = []

# remove unrelated characters and clean string to get the employee number
for line in lines:
    line = re.sub(r'1403-.*', '', line)
    line = line.strip()
    new_lines.append(line + "\n")



cleaned_numbers = [line.strip() for line in new_lines]


# Load the Database CSV file that include all employee names and codes
file_path = 'database.csv'
df = pd.read_csv(file_path, header=None, names=['Number', 'Name'])



# Search for the name with the each number we have in cleaned lines to confirm registered codes.
'''
This piece of code is performing a lookup operation to match employee numbers with their corresponding names using the database you loaded earlier. Here's a breakdown of what it does:

1. It initializes an empty list called finalResult to store the results.
2. It iterates through each line in the cleaned_numbers list, which presumably contains employee numbers extracted from the attendance log.
3. For each number:
 - It strips any leading or trailing whitespace from the line.
 - It searches the df DataFrame (which was loaded from 'database.csv') for a row where the 'Number' column matches the current line (converted to an integer).
 - The matching row (or an empty DataFrame if no match is found) is stored in the temp variable.
 - This temp result is then appended to the finalResult list.


The purpose of this code is to take the list of employee numbers from the attendance log and find the corresponding employee names from your database.
It's essentially translating the attendance log numbers into actual employee names.
'''

finalResult = []
for line in cleaned_numbers:
    line = line.strip()
    # Try to find the matching row
    temp = df[df['Number'] == int(line)]
    try:
        # print names found
        # print(temp['Name'].values[0])
        # append name found in db to our temporary list > finalResult[]
        finalResult.append(temp['Name'].values[0])
    except:
        print(f"Error | Code not exist in database: {line}")
    

# Get the count of results
count = len(finalResult)

# Prepare the content for the output file
output_content = f"{count}\n" + "\n".join(finalResult)

# Write the output content to a text file
output_path = 'final_result.txt'
with open(output_path, 'w',encoding='utf-8') as f:
    f.write(output_content)
    
    
# write into an excel file
xbook = xlsxwriter.Workbook(jalali_date + ".xlsx")
xsheet = xbook.add_worksheet('stats')

for idx, month in enumerate(finalResult):
    xsheet.write(idx,0,finalResult[idx])

xbook.close()

print(f"{count} Final results have been written to {output_path}")
file_cleaner()

os.rename('final_result.txt', jalali_date + ".txt")
