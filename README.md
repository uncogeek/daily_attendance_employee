# Employee Attendance Processor

This Python script processes attendance data from a device export file (uFace202), matches employee codes with a database, and generates reports in both text and Excel formats. It's designed to streamline the attendance tracking process for organizations using specific attendance tracking devices.

## Key Features

- Converts `.dat` files to `.txt` format
- Cleans and processes attendance log data
- Matches employee codes with names from a CSV database
- Generates reports in both `.txt` and `.xlsx` formats
- Uses Jalali (Shamsi) calendar for date conversion and file naming

## How It Works

1. **File Selection and Conversion**: 
   - Uses a GUI to select the input `.dat` file
   - Converts the `.dat` file to `.txt` format

2. **Data Cleaning**:
   - Removes unnecessary characters from each line
   - Extracts employee codes

3. **Employee Matching**:
   - Loads a CSV database with employee codes and names
   - Matches cleaned codes with the database to retrieve employee names

4. **Report Generation**:
   - Creates a text file with the count of records and employee names
   - Generates an Excel file with the same information
   - Names output files using the current Jalali (Shamsi) date

5. **File Management**:
   - Cleans up temporary files after processing

## Additional Features

- **Date Conversion**: Includes a function to convert Gregorian dates to Jalali (Shamsi) calendar
- **File Cleaning**: Removes temporary `.txt` and `.dat` files to keep the working directory clean

## Dependencies

- pandas
- xlsxwriter
- tkinter

## Usage

Run the script and select the `.dat` file when prompted. The script will process the file and generate the output reports in the same directory.
