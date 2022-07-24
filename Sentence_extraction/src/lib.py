import os
from os.path import join,basename,dirname
import glob
import json
import sys
from tqdm import tqdm
import numpy as np
import pandas as pd
from tabulate import tabulate
from konlpy.tag import Kkma
from konlpy.tag import Twitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
import warnings
warnings.filterwarnings(action='ignore')


def print_df(df):
    print(tabulate(df,headers='keys',tablefmt='psql'))

def read_pd_csv(csv_path):
    return pd.read_csv(csv_path)