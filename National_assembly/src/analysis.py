import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os,glob,sys
from os.path import join,basename,dirname
import re
import datetime as dt
import warnings 
warnings.filterwarnings(action='ignore')
plt.rcParams['font.family']='Malgun Gothic'

if __name__ == '__main__':
    root = sys.argv[1]
    img_root = join(dirname(root),'img','history')
    os.makedirs(img_root,exist_ok=True)
    
    people = pd.read_csv(join(root,'open','new_people.csv'),encoding='cp949')
    suggest = pd.read_csv(join(root,'open','suggest.csv'))
    process = pd.read_csv(join(root,'open','process.csv'))


    plt.figure(figsize=(8,4))
    plt.grid(True)
    plt.title('대수별 국회의원수')
    sns.countplot(people['DAESU'],palette='bright')
    fig = plt.gcf()
    fig.savefig(join(img_root,'대수별_국회의원수.png'),bbox_inches='tight', pad_inches=0.5)


    people['POSI_province'] = people['POSI'].apply(lambda x : np.nan if pd.isnull(x) else x.split()[0])
    people['POSI_province'] = people['POSI_province'].replace({'경기도':'경기','충청북도':'충북','파주':'경기','경상남도':'경남',
                                                            '원주':'강원','강원도':'강원','포항':'경북','경기포천':'경기','부여':'충남',
                                                            '충청남도':'충남','대구광역시':'대구','전라북도':'전북','전남목포':'전남',
                                                            '광주광역시':'광주','경남고성':'경남','익산시':'전북','아산':'충남','대전시':'대전',
                                                            '남제주':'제주','울산시':'울산','경상북도':'경북','황해도':'황해','나주':'전남',
                                                            '부산광역시':'부산','평안남도':'평남','함경남도':'함남','제주도':'제주','논산':'충남',
                                                            '함경북도':'함북','선산':'경북','대전광역시':'대전','인천시':'인천','전라남도':'전남',
                                                            '전라도':'전라','서울시':'서울','광주시':'광주','서울특별시':'서울','전북부안':'전북',
                                                            '인천광역시':'인천','신안군':'전남','의왕':'경기','평안북도':'평북','대구시':'대구',
                                                            '광주시':'광주','울산광역시':'울산','전남도':'전남','대전직할시':'대전','부산시':'부산',
                                                            '서울종로':'서울','강워도':'강원','전남보성':'전남','평양시':'평양','전북고창':'전북',
                                                            '안동':'경북','마산':'경남','청주':'충북','전주':'전북','진주':'경남','합천':'경남',
                                                            '강릉':'강원'})
    people['POSI_province'].unique()
    plt.figure(figsize=(8,4))
    plt.grid(True)
    plt.title('출신지역')
    sns.countplot(people['POSI_province'],order=people['POSI_province'].value_counts().index,palette='bright')
    plt.xticks(rotation=50)
    fig = plt.gcf()
    fig.savefig(join(img_root,'출신지역.png'),bbox_inches='tight', pad_inches=0.5)


    plt.figure(figsize=(8,4))
    plt.grid(True)
    plt.title('대수별 발의법의안 건수')
    sns.countplot(suggest['AGE'],palette='bright')
    fig = plt.gcf()
    fig.savefig(join(img_root,'대수별발의법의안건수.png'),bbox_inches='tight', pad_inches=0.5)


    suggest['PROPOSE_DT'] = pd.to_datetime(suggest['PROPOSE_DT'])

    mask = (suggest['PROPOSE_DT']>='2016-01-01')
    filtered_df = suggest.loc[mask]

    filtered_df['PROPOSE_DT_YEAR'] = filtered_df['PROPOSE_DT'].dt.year
    filtered_df['PROPOSE_DT_MONTH'] = filtered_df['PROPOSE_DT'].dt.month

    filtered_16 = filtered_df[filtered_df['PROPOSE_DT_YEAR']==2016]['PROPOSE_DT_MONTH'].value_counts().sort_index()
    filtered_17 = filtered_df[filtered_df['PROPOSE_DT_YEAR']==2017]['PROPOSE_DT_MONTH'].value_counts().sort_index()
    filtered_18 = filtered_df[filtered_df['PROPOSE_DT_YEAR']==2018]['PROPOSE_DT_MONTH'].value_counts().sort_index()
    filtered_19 = filtered_df[filtered_df['PROPOSE_DT_YEAR']==2019]['PROPOSE_DT_MONTH'].value_counts().sort_index()
    filtered_20 = filtered_df[filtered_df['PROPOSE_DT_YEAR']==2020]['PROPOSE_DT_MONTH'].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(8,4))
    plt.title('최근 5년 월별 발의법의안 건수')
    ax.plot(filtered_16,linewidth=3,color='silver', label='2016')
    ax.plot(filtered_17,linewidth=3,color='darkgray',label='2017')
    ax.plot(filtered_18,linewidth=3,color='gray',label='2018')
    ax.plot(filtered_19,linewidth=3,color='dimgray',label='2019')
    ax.plot(filtered_20,linewidth=3,color='k',label='2020')
    plt.grid(True)
    plt.legend()
    fig = plt.gcf()
    fig.savefig(join(img_root,'16대이후월별발의법의안건수.png'),bbox_inches='tight', pad_inches=0.5)

    grouped = suggest.groupby(['AGE','PROC_RESULT']).size().to_frame()
    grouped = grouped.rename(columns={0:'count'})
    grouped = grouped.dropna(axis=0)
    grouped = grouped.reset_index()

    grouped['cum_count']=grouped.groupby('AGE')['count'].cumsum(axis=0)
    grouped['norm_count']=grouped.groupby('AGE')['count'].apply(lambda x : x/sum(x))
    grouped['cum_norm_count']=grouped.groupby('AGE')['norm_count'].cumsum(axis=0)
    grouped = grouped.sort_values(by=['cum_norm_count'],ascending=False)
    plt.figure(figsize=(8,4))
    sns.barplot(x='AGE',y='cum_norm_count',hue='PROC_RESULT',data=grouped,dodge=False)
    plt.legend(loc='upper right',bbox_to_anchor=(1.3,1.0))
    plt.title('대수별 발의법의안 처리방법 비율')
    fig = plt.gcf()
    fig.savefig(join(img_root,'대수별발의법의안처리방법비율.png'),bbox_inches='tight', pad_inches=0.5)

    top5 = suggest['RST_PROPOSER'].value_counts()[:5]
    plt.figure(figsize=(8,4))
    plt.grid(True)
    plt.title('발의법의안을 제일 많이한 국회의원 top5')
    sns.barplot(x=top5.index,y=top5)
    fig = plt.gcf()
    fig.savefig(join(img_root,'발의법의안Top5.png'),bbox_inches='tight', pad_inches=0.5)


    suggest_copy = suggest

    suggest_copy['BILL_NAME'] = suggest_copy['BILL_NAME'].apply(lambda x : x.split()) 
    suggest_copy['BILL_NAME'] = suggest_copy['BILL_NAME'].apply(lambda x : x[0]) 

    suggest_copy = suggest_copy.groupby(['AGE','BILL_NAME']).size().to_frame()
    suggest_copy = suggest_copy.reset_index()
    suggest_copy = suggest_copy.rename(columns={0:'count'})

    def top_5(suggest_copy,n=5,column='count'):
        return suggest_copy.sort_values(by='count',ascending=False)[:n]

    grouped_top5 = suggest_copy.groupby('AGE').apply(top_5,column='count',n=5)

    grouped_17 = grouped_top5[grouped_top5['AGE']==17]
    grouped_18 = grouped_top5[grouped_top5['AGE']==18]
    grouped_19 = grouped_top5[grouped_top5['AGE']==19]
    grouped_20 = grouped_top5[grouped_top5['AGE']==20]
    grouped_21 = grouped_top5[grouped_top5['AGE']==21]

    fig = plt.figure(figsize=(14,10))

    ax1 = fig.add_subplot(2,3,1) 
    plt.title('17대수 법의발의안 top5')
    plt.grid(True)
    plt.xticks(rotation=30)
    ax2 = fig.add_subplot(2,3,2)
    plt.title('18대수 법의발의안 top5')
    plt.grid(True)
    plt.xticks(rotation=30)
    ax3 = fig.add_subplot(2,3,3)
    plt.title('19대수 법의발의안 top5')
    plt.grid(True)
    plt.xticks(rotation=30)
    ax4 = fig.add_subplot(2,3,4) 
    plt.title('20대수 법의발의안 top5')
    plt.grid(True)
    plt.xticks(rotation=30)
    ax5 = fig.add_subplot(2,3,5)
    plt.title('21대수 법의발의안 top5')
    plt.grid(True)
    plt.xticks(rotation=30)


    sns.barplot(x=grouped_17['BILL_NAME'],y=grouped_17['count'],ax=ax1)
    sns.barplot(x=grouped_18['BILL_NAME'],y=grouped_18['count'],ax=ax2)
    sns.barplot(x=grouped_19['BILL_NAME'],y=grouped_19['count'],ax=ax3)
    sns.barplot(x=grouped_20['BILL_NAME'],y=grouped_20['count'],ax=ax4)
    sns.barplot(x=grouped_21['BILL_NAME'],y=grouped_21['count'],ax=ax5)

    fig.savefig(join(img_root,'지난5대수법의발의안종류.png'))


    plt.figure(figsize=(8,4))
    plt.title('대수별 본회의 처리안건수')
    plt.grid(True)
    sns.countplot(process['AGE'],palette='bright')
    fig = plt.gcf()
    fig.savefig(join(img_root,'대수별본회의처리안건수.png'),bbox_inches='tight', pad_inches=0.5)


    vote_cnt = process[['AGE','VOTE_TCNT','YES_TCNT','NO_TCNT','BLANK_TCNT']]

    vote_cnt['yes_ratio'] = vote_cnt['YES_TCNT']/vote_cnt['VOTE_TCNT']
    vote_cnt['no_ratio'] = vote_cnt['NO_TCNT']/vote_cnt['VOTE_TCNT']
    vote_cnt['blank_ratio'] = vote_cnt['BLANK_TCNT']/vote_cnt['VOTE_TCNT']

    vote_cnt['yes_ratio'] = vote_cnt['yes_ratio'].apply(lambda x : x if x >=0 else 0)
    vote_cnt['no_ratio'] = vote_cnt['no_ratio'].apply(lambda x : x if x >=0 else 0)
    vote_cnt['blank_ratio'] = vote_cnt['blank_ratio'].apply(lambda x : x if x >=0 else 0)

    mean_yes_ratio = vote_cnt['yes_ratio'].groupby(vote_cnt['AGE']).mean()
    mean_no_ratio = vote_cnt['no_ratio'].groupby(vote_cnt['AGE']).mean()
    mean_blank_ratio = vote_cnt['blank_ratio'].groupby(vote_cnt['AGE']).mean()

    mean_ratio = pd.DataFrame({'age': mean_yes_ratio.index,
                            'mean_yes_ratio': mean_yes_ratio,
                            'mean_no_ratio': mean_no_ratio,
                            'mean_blank_ratio': mean_blank_ratio})
    mean_ratio.reset_index(inplace=True)
    mean_ratio.drop('AGE',axis=1,inplace=True)
    print(mean_ratio)

    mean_ratio = mean_ratio[-2:]
    mean_ratio_20 = mean_ratio.iloc[[0],1:4]
    mean_ratio_21 = mean_ratio.iloc[[1],1:4]

    mean_ratio_20.round(2)
    mean_ratio_21.round(2)

    df_cnt_ratio = pd.DataFrame({'age':[20,20,20,21,21,21],
                                'kind':['yes','no','blank','yes','no','blank'],
                                'mean_ratio': [0.18,0,0,0.62,0.01,0.02]})
    df_cnt_ratio
    print(df_cnt_ratio)

    plt.figure(figsize=(8,4))
    sns.catplot(x="age", y="mean_ratio", hue="kind",
                    capsize=.2, kind="bar", data=df_cnt_ratio)
    plt.title('20대,21대 찬성,반대,기권 투표비율의 평균 비교')
    plt.grid(True)
    fig = plt.gcf()
    fig.savefig(join(img_root,'20,21대투표비율평균.png'),bbox_inches='tight', pad_inches=0.5)


    process_copy = process[['PROPOSE_DT','ANNOUNCE_DT','AGE']]

    process_notnull = process_copy[process_copy['ANNOUNCE_DT'].notnull()]
    process_notnull.reset_index(inplace=True)
    process_notnull.drop('index',axis=1,inplace=True)

    process_notnull['PROPOSE_DT'] = pd.to_datetime(process_notnull['PROPOSE_DT'])
    process_notnull['ANNOUNCE_DT'] = pd.to_datetime(process_notnull['ANNOUNCE_DT'],errors = 'coerce') # Out of Boundary Error

    process_notnull['diff_dt'] = process_notnull['ANNOUNCE_DT'] - process_notnull['PROPOSE_DT']
    process_notnull = process_notnull[process_notnull['PROPOSE_DT'] <= process_notnull['ANNOUNCE_DT']] # 제안일이 공포일보다 전에 일어난 경우만

    process_notnull['diff_dt'] = process_notnull['diff_dt'].astype('str')
    process_notnull['diff_dt'] = process_notnull['diff_dt'].apply(lambda x : re.findall('\d+',x)[0])
    process_notnull.head(3)

    process_notnull['diff_dt'] = process_notnull['diff_dt'].astype('int')
    mean_diff_dt = process_notnull.groupby('AGE')['diff_dt'].mean()
    mean_diff_dt = mean_diff_dt.to_frame()
    mean_diff_dt.reset_index(inplace=True)
    mean_diff_dt.head(3)

    plt.figure(figsize=(8,4))
    plt.title('대수별 제안일에서 공포일까지 걸리는 시간')
    plt.grid(True)
    sns.barplot(x=mean_diff_dt['AGE'],y=mean_diff_dt['diff_dt'],palette='bright')
    fig = plt.gcf()
    fig.savefig(join(img_root,'대수별제안에서공포까지시간.png'),bbox_inches='tight', pad_inches=0.5)



    process_dt = process

    process_dt['PROPOSE_DT'] = pd.to_datetime(process_dt['PROPOSE_DT'])
    process_dt['ANNOUNCE_DT'] = pd.to_datetime(process_dt['ANNOUNCE_DT'],errors = 'coerce') # Out of Boundary Error

    process_dt['propose_month'] = process_dt['PROPOSE_DT'].dt.month
    process_dt['announce_month'] = process_dt['ANNOUNCE_DT'].dt.month
    process_dt['propose_weekday'] = process_dt['PROPOSE_DT'].dt.weekday # weekday (0:월 1:화 2:수 3:목 4:금 5:토 6:일)
    process_dt['announce_weekday'] = process_dt['ANNOUNCE_DT'].dt.weekday

    process_dt = process_dt[['propose_month','announce_month','propose_weekday','announce_weekday']]
    process_dt['announce_month'] = pd.to_numeric(process_dt['announce_month'],downcast='integer',errors='coerce')

    fig = plt.figure(figsize=(10,4))
    ax1 = fig.add_subplot(1,2,1)
    plt.title('월별 제안일 수')
    plt.grid(True)
    ax2 = fig.add_subplot(1,2,2)
    plt.title('요일별 제안일 수')
    plt.grid(True)
    sns.countplot(process_dt['propose_month'],ax=ax1,palette='bright')
    sns.countplot(process_dt['propose_weekday'],ax=ax2,palette='bright')
    fig.savefig(join(img_root,'월별,요일별제안일수.png'),bbox_inches='tight', pad_inches=0.5)


    fig = plt.figure(figsize=(10,4))
    ax1 = fig.add_subplot(1,2,1)
    plt.title('월별 공포일 수')
    plt.grid(True)
    ax2 = fig.add_subplot(1,2,2)
    plt.title('요일별 공포일 수')
    plt.grid(True)
    sns.countplot(process_dt['announce_month'],ax=ax1,palette='bright')
    sns.countplot(process_dt['announce_weekday'],ax=ax2,palette='bright')
    fig.savefig(join(img_root,'월별,요일별공포일수.png'),bbox_inches='tight', pad_inches=0.5)