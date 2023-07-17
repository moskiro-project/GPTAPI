import openai
import pandas as pd
import time
import json
import ast

cluster_file = "./Data/TitleClusters Cleaned.xlsx"
data_file = "./Data/FullDataset_fromNER_v1.xlsx"



def assign_cluster(row, result_dict):
    print(row[4])
    if str(row[4]) in result_dict:
        return result_dict[str(row[4])][1]
    return "_"

def main():
    df = pd.read_excel(cluster_file)
    result_dict = df.set_index(df.columns[1]).T.to_dict('list')
    print(result_dict)
    
    data = pd.read_excel(data_file)
    
    print("Start")
    data["Cluster"] = data.apply(assign_cluster, args=(result_dict,), axis = 1)
    print("End")
    output_file = './data/Complete Data Clustered.xlsx'
    data.to_excel(output_file, index=False)
    
if __name__ == '__main__':
    main()