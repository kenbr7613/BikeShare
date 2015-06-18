# coding: utf-8
import pandas as pd
data = pd.read_csv("sampleSubmission.csv")
data.to_csv("submission1.csv",index=False)
