import convertToFile
import convertToServer
import mySqlToMongo

print("Choose your option:")

options = ["Convert CSVs to SQL files", "Convert CSVs to SQL Server", "Migrate from MySQL to MongoDB"]
for i in range(len(options)):
    print(f"{i+1}. {options[i]}")

answer = ""
while True:
    answer = input("\n> ")

    try:
        answer = int(answer)
        if answer < 1 or answer > len(options):
            raise Exception()
    except:
        print("Please insert a valid option")
        continue
    break

print("Operating...")
match (answer):
    case 1:
        convertToFile.csvToSQL()
    case 2:
        convertToServer.csvToSQL()
    case 3:
        mySqlToMongo.mySQLtoMongoDB()