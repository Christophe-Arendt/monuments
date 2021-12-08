import os
import pandas as pd

def csv_path(data_path):
    # Define datapath
    path = []
    target = []
    for monument in os.listdir(data_path+"/photos"):
      for photo in os.listdir(data_path+f"/photos/{monument}"):
        target.append(monument)
        path.append(data_path + f"/photos/{monument}/{photo}")

    # Create dataframe
    df = pd.DataFrame()
    df['path'] = path
    df['target'] = target

    # Save as csv
    #df.to_csv(f"{data_path}/path_csv.csv", index=False)
    return df


if __name__ == '__main__':
    data_path = os.getcwd()
    df = csv_path(data_path)
    print(df.shape)
    print(df.groupby('target').count())

