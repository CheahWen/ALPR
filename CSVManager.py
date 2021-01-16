import csv
from datetime import date 
import traceback
from LogManager import LogManager

class CSVManager:
    @staticmethod
    def writeRow(filename, data):
        try:
            # Write CSV file
            with open(filename, "a") as fp:
                writer = csv.writer(fp, delimiter=",")
                #writer.writerow(["Car plate number", "Time"])  # write header
                
                writer.writerow(data)   
                fp.close()
        except:
            LogManager.makeLog(message="Cannot save CSV file!", type=1)
            LogManager.makeLog(message=f'{traceback.format_exc()}', type=1)