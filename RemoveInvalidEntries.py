import openai
import pandas as pd
import time
import json
import ast

cluster_file = "./Data/Complete Data Clustered.xlsx"


def main():
    df = pd.read_excel(cluster_file)
    df = df[df["Cluster"] != "_"]
    output_file = './data/Complete Data Clustered Cleaned.xlsx'
    df.to_excel(output_file, index=False)
    
if __name__ == '__main__':
    main()