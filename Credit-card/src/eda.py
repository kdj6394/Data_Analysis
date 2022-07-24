import os,glob,sys
from os.path import join,basename,dirname
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rc('font', family='Malgun Gothic')
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from collections import Counter
import missingno as msno
import warnings
warnings.filterwarnings('ignore')

def cat_plot(column,img_root,png_title):
  f, ax = plt.subplots(1, 3, figsize=(16, 6))

  sns.countplot(x = column,
                data = train_0,
                ax = ax[0],
                order = train_0[column].value_counts().index)
  ax[0].tick_params(labelsize=12)
  ax[0].set_title('credit = 0')
  ax[0].set_ylabel('count')
  ax[0].tick_params(rotation=50)

  sns.countplot(x = column,
                data = train_1,
                ax = ax[1],
                order = train_1[column].value_counts().index)
  ax[1].tick_params(labelsize=12)
  ax[1].set_title('credit = 1')
  ax[1].set_ylabel('count')
  ax[1].tick_params(rotation=50)

  sns.countplot(x = column,
                data = train_2,
                ax = ax[2],
                order = train_2[column].value_counts().index)
  ax[2].tick_params(labelsize=12)
  ax[2].set_title('credit = 2')
  ax[2].set_ylabel('count')
  ax[2].tick_params(rotation=50)
  plt.subplots_adjust(wspace=0.3, hspace=0.3)
  plt.grid()
  plt.tight_layout()
  fig = plt.gcf()
  fig.savefig(join(img_root,png_title+'.png'))

def num_plot(column,img_root,png_title):
  fig, axes = plt.subplots(1, 3, figsize=(16, 6))

  sns.distplot(train_0[column],
                ax = axes[0])
  axes[0].tick_params(labelsize=12)
  axes[0].set_title('credit = 0')
  axes[0].set_ylabel('count')

  sns.distplot(train_1[column],
                ax = axes[1])
  axes[1].tick_params(labelsize=12)
  axes[1].set_title('credit = 1')
  axes[1].set_ylabel('count')

  sns.distplot(train_2[column],
                ax = axes[2])
  axes[2].tick_params(labelsize=12)
  axes[2].set_title('credit = 2')
  axes[2].set_ylabel('count')

  plt.subplots_adjust(wspace=0.3, hspace=0.3)
  plt.tight_layout()
  fig = plt.gcf()
  fig.savefig(join(img_root,png_title+'.png'))


if __name__ == '__main__':
    root = sys.argv[1]
    tarin_root = join(root,'open','train.csv')
    img_root = join(dirname(root),'img')
    os.makedirs(img_root,exist_ok=True)

    train = pd.read_csv(tarin_root)
    
    # 결측치
    msno.bar(df=train.iloc[:,:])
    plt.grid()
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(join(img_root,'결측치.png'),pad_inches=1)
    
    # 신용등급비율
    train = train.astype({'credit': 'object'})
    print(train.dtypes)

    plt.subplots(figsize = (8,8))
    plt.pie(train['credit'].value_counts(), labels = train['credit'].value_counts().index, 
            autopct="%.2f%%", shadow = False, startangle = 90, explode=[0.1,0.1,0.1])
    plt.title('신용 등급 비율', size=20)
    plt.tight_layout()
    plt.grid()
    fig = plt.gcf()
    fig.savefig(join(img_root,'신용등급비율.png'))

    
    # 신용등급에 따른 차이를 보기위한 분류 및 정의

    train_0 = train[train['credit']==0.0]
    train_1 = train[train['credit']==1.0]
    train_2 = train[train['credit']==2.0]

    cat_plot("gender",img_root,'신용등급에따른성별')
    cat_plot('car',img_root,'신용등급에따른차량소유')
    cat_plot('reality',img_root,'신용등급에따른부동산소유')
    # 높은 신용등급에서 학생은 없음
    # 낮은 신용등급에서는 학생 존재 -> 신분특성반영?
    cat_plot('income_type',img_root,'신용등급에따른소득분류') 
    # 신용등급에 따라 교육수준차이는 없어보임
    cat_plot('edu_type',img_root,'신용등급에따른교육수준')
    # 모든등급에서 기혼자가 많음.
    cat_plot('family_type',img_root,'신용등급에따른결혼여부')
    # 모든등급에서 생활방식의 차이는 없음
    cat_plot('house_type',img_root,'신용등급에따른생활방식')
    # 마찬가지 핸드폰 소유도 차이 없음
    cat_plot('FLAG_MOBIL',img_root,'신용등급에따른핸드폰소유')

    # 신용등급에 따른 직업유형
    train_0 = train_0.fillna({'occyp_type':'No job'})
    train_1 = train_1.fillna({'occyp_type':'No job'})
    train_2 = train_2.fillna({'occyp_type':'No job'})
    f, ax = plt.subplots(1, 3, figsize=(16, 6))
    sns.countplot(y = 'occyp_type', data = train_0, order = train_0['occyp_type'].value_counts().index, ax=ax[0])
    sns.countplot(y = 'occyp_type', data = train_1, order = train_1['occyp_type'].value_counts().index, ax=ax[1])
    sns.countplot(y = 'occyp_type', data = train_2, order = train_2['occyp_type'].value_counts().index, ax=ax[2])
    plt.subplots_adjust(wspace=0.5, hspace=0.3)
    plt.grid()
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(join(img_root,'신용등급별직업유형.png'),pad_inches=1)

    # 신용등급에 따른 자녀수 차이, 연간소득차이
    num_plot("child_num",img_root,'신용등급별자녀수')
    num_plot("income_total",img_root,'신용등급별수입')

    plt.clf()
    sns.distplot(train_0['income_total'],label='0.0', hist=False)
    sns.distplot(train_1['income_total'],label='0.1', hist=False)
    sns.distplot(train_2['income_total'],label='0.2', hist=False)
    plt.legend()
    plt.tight_layout()
    fig = plt.gcf()
    fig.savefig(join(img_root,'신용등급별수입_겹쳐서.png'),pad_inches=1)


    # 연령대
    train_0['Age'] = abs(train_0['DAYS_BIRTH'])/360
    train_1['Age'] = abs(train_1['DAYS_BIRTH'])/360
    train_2['Age'] = abs(train_2['DAYS_BIRTH'])/360
    train_0['Age'].head()

    train_0 = train_0.astype({'Age': 'int'})
    train_1 = train_1.astype({'Age': 'int'})
    train_2 = train_2.astype({'Age': 'int'})
    train_0['Age'].head()

    num_plot("Age",img_root,'신용등급별연령')

    # 신용등급에 따른 업무 기간 차이
    train_0['EMPLOYED']= train_0['DAYS_EMPLOYED'].map(lambda x: 0 if x>0 else x)
    train_0['EMPLOYED']= train_0['DAYS_EMPLOYED'].map(lambda x: 0 if x>0 else x)
    train_1['EMPLOYED']= train_1['DAYS_EMPLOYED'].map(lambda x: 0 if x>0 else x)
    train_2['EMPLOYED']= train_2['DAYS_EMPLOYED'].map(lambda x: 0 if x>0 else x)
    train_0['EMPLOYED'] = abs(train_0['EMPLOYED'])/360
    train_1['EMPLOYED'] = abs(train_1['EMPLOYED'])/360
    train_2['EMPLOYED'] = abs(train_2['EMPLOYED'])/360
    train_0['EMPLOYED'].head()
    train_0 = train_0.astype({'EMPLOYED': 'int'})
    train_1 = train_1.astype({'EMPLOYED': 'int'})
    train_2 = train_2.astype({'EMPLOYED': 'int'})
    num_plot("EMPLOYED",img_root,'신용등급별직업')
    num_plot("family_size",img_root,'신용등급별가족수')

    # 카드발급기간
    train_0['Month'] = abs(train_0['begin_month'])
    train_1['Month'] = abs(train_1['begin_month'])
    train_2['Month'] = abs(train_2['begin_month'])
    train_0 = train_0.astype({'Month': 'int'})
    train_1 = train_1.astype({'Month': 'int'})
    train_2 = train_2.astype({'Month': 'int'})
    train_0['Month'].head()
    num_plot("Month",img_root,'신용등급별발급개월수')