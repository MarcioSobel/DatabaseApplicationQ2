import convertToFile
import convertToServer

answer = input("Do you want to convert to SQL server (recommended)? (Y/n)\n> ")

if (answer.lower() == "n"):
    print("Converting into /convertedData...")
    convertToFile.csvToSQL()
else:
    print("Converting to your local SQL server...")
    convertToServer.csvToSQL()
    