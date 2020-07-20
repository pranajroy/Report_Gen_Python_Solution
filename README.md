# Table extraction from html files

## Libraries used :

* Beautiful Soup
* Pandas

## Working of code:

* The code extracts the table data from the html files which resides in the "SAPtab" folder. While extracting the data timestampis embedded with each data and placed it in csv file.

* Each html file have tab "SAP" - data is extracted from the table and placed in csv file.

* Duplicate data have timestamp embedded with it in the output file.

## How to run: 

* python report.py <path to the folder> <output filename> 