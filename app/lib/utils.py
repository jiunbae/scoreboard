import pandas as pd

def get_assignments():
    df = pd.read_csv('./data/assignments.csv')
    return [{k:v for k, v in zip(df.columns, val)} for val in df.values]

def get_assignment(id):
    df = pd.read_csv('./data/assignments.csv')
    return dict(df.iloc[id])
