import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os,glob,sys
from os.path import join,basename,dirname
import re
import datetime as dt
import warnings 
warnings.filterwarnings(action='ignore')
plt.rcParams['font.family']='Malgun Gothic'

if __name__ == '__main__':
    root = sys.argv[1]
    img_root = join(dirname(root),'img','covid-19')
    os.makedirs(img_root,exist_ok=True)
    
    people = pd.read_csv(join(root,'open','new_people.csv'),encoding='cp949')
    suggest = pd.read_csv(join(root,'open','suggest.csv'))
    process = pd.read_csv(join(root,'open','process.csv'))

    twenty_one_sug = suggest[suggest['AGE'] == 21]
    print('21대 국회 총 발의법의안 수: ', len(twenty_one_sug))
    twenty_sug = suggest[suggest['AGE'] == 20]
    print('20대 국회 총 발의법의안 수: ', len(twenty_sug))
    nineteen_sug = suggest[suggest['AGE'] == 19]
    print('19대 국회 총 발의법의안 수: ', len(nineteen_sug))

    law_covid_21=[]
    law_covid_20=[]
    law_covid_19=[]
    rel_covid=['감염병', '의료법', '의료', '코로나', '검역법']

    Okt = Okt()

    # 21대 국회
    for law_name in twenty_one_sug['BILL_NAME']:
        for word in Okt.nouns(law_name):
            if word in rel_covid:
                law_covid_21.append(law_name)
                continue
    law_covid_df_21 = pd.DataFrame({'law': law_covid_21})
                
    # 20대 국회
    for law_name in twenty_sug['BILL_NAME']:
        for word in Okt.nouns(law_name):
            if word in rel_covid:
                law_covid_20.append(law_name)
                continue
    law_covid_df_20 = pd.DataFrame({'law': law_covid_20})

    # 19대 국회
    for law_name in nineteen_sug['BILL_NAME']:
        for word in Okt.nouns(law_name):
            if word in rel_covid:
                law_covid_19.append(law_name)
                continue
    law_covid_df_19 = pd.DataFrame({'law': law_covid_19})

    print("제 21대 감염병 관련 발의법의안 TOP 5")
    print(law_covid_df_21['law'].value_counts().head())
    print("제 20대 감염병 관련 발의법의안 TOP 5")
    print(law_covid_df_20['law'].value_counts().head())
    print("제 19대 감염병 관련 발의법의안 TOP 5")
    print(law_covid_df_19['law'].value_counts().head())


    plt.figure(figsize = (15,25))
    plt.subplot(313)
    plt.grid()
    plt.title('제 21대 국회 감염병 관련 발의법의안 TOP 5', fontsize = 20)
    sns.barplot(law_covid_df_21['law'].value_counts().index[:5],law_covid_df_21['law'].value_counts()[:5])
    plt.xticks(rotation = 5)

    plt.subplot(312)
    plt.title('제 20대 국회 감염병 관련 발의법의안 TOP 5', fontsize = 20)
    plt.grid()
    sns.barplot(law_covid_df_20['law'].value_counts().index[:5],law_covid_df_20['law'].value_counts()[:5])
    plt.xticks(rotation = 5)

    plt.subplot(311)
    plt.title('제 19대 국회 감염병 관련 발의법의안 TOP 5', fontsize = 20)
    plt.grid()
    sns.barplot(law_covid_df_19['law'].value_counts().index[:5],law_covid_df_19['law'].value_counts()[:5])
    plt.xticks(rotation = 5)

    fig = plt.gcf()
    fig.savefig(join(img_root,'최근3대국회감염병관련발의법의안Top5.png'),bbox_inches='tight', pad_inches=0.5)
    
    rel_covid3=['감염병의 예방 및 관리에 관한 법률 일부개정법률안', '의료법 일부개정법률안', '검역법 일부개정법률안'] # 코로나 19관련 3법

    twenty_one_covid_sug = twenty_one_sug[twenty_one_sug['BILL_NAME'].isin(rel_covid3)]
    twenty_covid_sug = twenty_sug[twenty_sug['BILL_NAME'].isin(rel_covid3)]
    nineteen_covid_sug = nineteen_sug[nineteen_sug['BILL_NAME'].isin(rel_covid3)]        

    print("21대 국회의 코로나 3법 입법 비율: ", round(len(twenty_one_covid_sug)/len(twenty_one_sug)*100, 3), "%")
    print("20대 국회의 코로나 3법 입법 비율: ", round(len(twenty_covid_sug)/len(twenty_sug)*100, 3), "%")  
    print("19대 국회의 코로나 3법 입법 비율: ", round(len(nineteen_covid_sug)/len(nineteen_sug)*100, 3), "%")

    plt.figure(figsize = (10,5))

    index=[0,1,2]
    label=['21대', '20대', '19대']
    law_ratio = [len(twenty_one_covid_sug)/len(twenty_one_sug)*100, len(twenty_covid_sug)/len(twenty_sug)*100,
                len(nineteen_covid_sug)/len(nineteen_sug)*100]

    plt.title('입법 비율 비교', fontsize=20)
    plt.xlabel('대수', fontsize=10)
    plt.ylabel('입법 비율 (%)', fontsize=10)
    plt.xticks(index, label, fontsize=15)
    plt.grid()
    plt.bar(index, law_ratio)

    fig = plt.gcf()
    fig.savefig(join(img_root,'최근3대국회감염병관련법안입법비율.png'),bbox_inches='tight', pad_inches=0.5)