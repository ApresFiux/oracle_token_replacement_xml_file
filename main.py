import csv
import json
import os, sys
import fileinput
import cx_Oracle
import argparse

def Search_And_Replace(filename, text_to_search, replacement_text): #Search and replace function
    with fileinput.FileInput(filename, inplace=True, backup='.bak') as file: #backup is not necessary
        for line in file:
            print(line.replace(text_to_search, replacement_text), end='')

def TokenFile_Import(tokenFile, CONFIG_XML): #this function takes the json ready file, reads the keys [tokens] and than performs the replacement with "Search_And_Replace" function
    with open(tokenFile) as f:
        data = json.loads(f.read())
    for i in reversed(sorted(data)):
        Search_And_Replace(CONFIG_XML, i, data[i])
        if i in data:
            del data[i] #[removes if there a duplicate key, but as it's goes reversally , its ignores the old keys [tokens]

def CONVERT_CSV_TO_JSON (csvFile, jsonFile, FieldList, CONFIG_XML):
    with open(csvFile, 'rU') as f:
        csv_data = csv.DictReader(f, fieldnames=FieldList)
        json_data = json.dumps([row for row in csv_data])
    with open(jsonFile, 'w') as f:
        f.write(json_data)
    TokenFile_Import(jsonFile, CONFIG_XML)

def Oracle_Export(OracleDBConnection, SQL, CSV_OUTPUT_FILE, jsonFile, FieldList, CONFIG_XML): #
    connection = raw_input(OracleDBConnection)
    orcl = cx_Oracle.connect(connection)
    cursor = orcl.cursor()
    cursor.execute(SQL)
    file = open(CSV_OUTPUT_FILE, 'w')
    output = csv.writer(file, dialect='excel')
    for i in cursor:
        output.writerow(i)
    cursor.close()
    connection.close()
    file.close()
    CONVERT_CSV_TO_JSON(CSV_OUTPUT_FILE, jsonFile, FieldList, CONFIG_XML)

parser = argparse.ArgumentParser('Token_Replacer')
parser.add_argument('-u', '--username')
parser.add_argument('-p', '--password')
parser.add_argument('-c', '--configfile')
args = parser.parse_args()

DB_USER = args.username
DB_PASS = args.password
DB_NAME = "" 
CONFIG_XML_FILE = args.configfile
SQL_MATHOD = "" #example - SELECT * FROM TABL
CSV_OUT = "CSV_FILE.csv" #temorary file could be used for debuggin or hard coded
JSON_FNAME = "JSON_FILE.json" #temorary file could be used for debuggin or hard coded
CSV_FIELDS = ["field_1_name", "field_2_name", "field_3_name"] #have to fill all of the fields
if __name__ == "__main__":
    Oracle_Export(DB_USER + "/" + DB_PASS + "@" + DB_NAME, SQL_MATHOD, CSV_OUT, JSON_FNAME, CSV_FIELDS , CONFIG_XML_FILE)

"""
this is just an untested example of token replacement
takes a table or any sql execution result to csv file
than translates csv file to json and perform search and replace
the table structure should be "TOKEN": "VALUE" for this spesific script
the config.xml file should be written as first argument
all 'static'/'temporary' files variables could be statically configured in this script
"""