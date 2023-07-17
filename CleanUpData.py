import openai
import pandas as pd
import time
import json
import ast

excel_file = "./Data/TitleClusters Cleaned.xlsx"

def is_int(value):
    if value is None:
        return False
    try:
        int(value)
        return True
    except:
        return False

def clean_index(row):
    index = str(row["Cluster"])
    if('.' in index):
        index = index.split('.')[0]
    if(is_int(index)):
        if(int(index) < 52 and int(index) > 0):
            return int(index)
    return index + "_correction needed!"

def main():
    df = pd.read_excel(excel_file)
    print("Start")
    df["CleanedCluster"] = df.apply(clean_index, axis = 1)
    print("End")
    output_file = './data/TitleClusters Cleaned 2.xlsx'
    df.to_excel(output_file, index=False)
    
if __name__ == '__main__':
    main()