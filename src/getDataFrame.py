import pandas as pd
import numpy
import os

def getDataFrame(filename: str) -> pd.DataFrame:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(script_directory, os.pardir, "data")

    df = pd.read_csv(f"{data_directory}/{filename}")

    return df

def createAutoIncrementColumn(dataFrame: pd.DataFrame, columnName = "id") -> pd.DataFrame:
    dataFrame[columnName] = numpy.arange(1, (len(dataFrame) + 1))

    # move column to the first index: https://sparkbyexamples.com/pandas/pandas-change-position-of-a-column/
    temp_cols = dataFrame.columns.tolist()
    cols = temp_cols[-1:] + temp_cols[:-1]
    dataFrame = dataFrame[cols]
    return dataFrame

def createDataDir():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    directory = os.path.join(script_directory, os.pardir, "convertedData")
    os.makedirs(directory, exist_ok=True)
    return directory