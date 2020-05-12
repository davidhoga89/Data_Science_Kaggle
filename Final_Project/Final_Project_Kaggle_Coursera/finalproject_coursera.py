import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import joblib

from sklearn import preprocessing
from sklearn import metrics

df = pd.read_csv("../sales_train.csv")
print(df.head(10))
df.describe()
