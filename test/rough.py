import pandas as pd

df = pd.read_csv("data/raw/participants.tsv", sep="\t")
print(df["participant_id"].head(10))
print(df["participant_id"].tail(10))
print("Total:", len(df))