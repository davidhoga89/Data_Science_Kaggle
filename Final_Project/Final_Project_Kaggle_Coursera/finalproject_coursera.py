import pandas as pd
import numpy as np
import seaborn as sns
from mathplotlib import pyplot
import os
import joblib

from sklearn import preprocessing
from sklearn import metrics

df = open_csv("sales_train.csv")
