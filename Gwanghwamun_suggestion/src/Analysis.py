from lib import os,glob,sys,join,basename,dirname
from lib import np,pd,plt,sns
plt.rc('font',family='Malgun Gothic')
from lib import warnings
warnings.filterwarnings(action='ignore')

def barh_plot(data,x:str,y:str,str_color:str):
    plt.figure(figsize=(15,8))
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(x+'별'+y,fontsize=15)
    plt.barh(data[x],data[y],label=y)
    for i,v in enumerate(data[x]):
        str_val = data[y][i]
        plt.text(data[y][i],v,str_val,
                fontsize=9,color=str_color,horizontalalignment = 'left',
                verticalalignment = 'center',fontweight='bold')
    plt.grid()
    plt.draw()
    fig = plt.gcf()
    return fig

def plot(data,x:str,y:str,str_color:str):
    plt.figure(figsize=(15,8))
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(x+'별'+y,fontsize=15)
    plt.plot(data[x],data[y],'-',label=y)
    plt.xticks(fontsize=7,rotation=65)
    plt.legend()
    for i,v in enumerate(data[y]):
        str_val = data[x][i]
        plt.text(data[x][i],v,str_val,fontsize=8,color=str_color,
        horizontalalignment = 'left',verticalalignment = 'center',fontweight = 'bold')
    plt.draw()
    fig = plt.gcf()
    return fig


if __name__ == '__main__':
    root = sys.argv[1]

    img_save_root = join(dirname(root),'src','img')
    os.makedirs(img_save_root,exist_ok=True)

    data_path = glob.glob(join(root,'*.txt'))[-1]
    data = pd.read_csv(data_path,sep='\t',header=None,encoding='utf8')
    
    data.columns = ['구분','진행상황','생성날짜','ID','좋아요수','제목','내용']
    

    division_df = pd.DataFrame(data['구분'])
    unique_list = division_df['구분'].unique()
    value = division_df['구분'].value_counts()
    division_df_count = division_df['구분'].value_counts().rename_axis('구분목록').reset_index(name='청원횟수')
    division_df_count = division_df_count.sort_values(by=['청원횟수'], ascending = True).reset_index()
    fig = barh_plot(division_df_count,'구분목록','청원횟수','red')
    fig.savefig(join(img_save_root,'구분별청원횟수.png'),dpi=fig.dpi)

    
    situation_df = pd.DataFrame(data['진행상황'])
    unique_list = situation_df['진행상황'].unique()
    value = situation_df['진행상황'].value_counts()
    situation_df_count = situation_df['진행상황'].value_counts().rename_axis('진행상황목록').reset_index(name='목록횟수')
    situation_df_count = situation_df_count.sort_values(by=['목록횟수'], ascending = True).reset_index()
    fig = barh_plot(situation_df_count,'진행상황목록','목록횟수','red')
    fig.savefig(join(img_save_root,'진행상황별목록횟수.png'),dpi=fig.dpi)
    

    date_df = pd.DataFrame(data['생성날짜'])
    unique_list = date_df['생성날짜'].unique()
    value = date_df['생성날짜'].value_counts()
    date_df_count = date_df['생성날짜'].value_counts().rename_axis('생성날짜목록').reset_index(name='청원횟수')
    date_df_count = date_df_count.sort_values(by=['생성날짜목록'], ascending = True).reset_index()
    fig = plot(date_df_count,'생성날짜목록','청원횟수','black')
    fig.savefig(join(img_save_root,'생성날짜별청원횟수.png'),dpi=fig.dpi)


    division_like_df = pd.DataFrame(data[['구분','좋아요수']]).sort_values(by=['구분'])
    mean_data = division_like_df.groupby(['구분'], as_index = False).mean().round(3)
    mean_data = mean_data.rename(columns={'좋아요수' : 'mean_like'})
    max_data = division_like_df.groupby(['구분'], as_index = False).max()
    max_data = max_data.rename(columns={'좋아요수' : 'max_like'})
    mean_max_data = pd.concat([mean_data,max_data['max_like']],axis=1)
    print(mean_max_data)

    plt.figure(figsize=(15,8))
    plt.xlabel('구분',fontsize=15)
    plt.ylabel('좋아요수',fontsize=15)
    plt.title('구분별 좋아요수',fontsize=15)
    plt.scatter(division_like_df['구분'],division_like_df['좋아요수'],label='좋아요수')
    for i,v in enumerate(mean_max_data['구분']):
        str_val = mean_max_data['구분'][i]
        mean_like,max_like = mean_max_data['mean_like'][i], mean_max_data['max_like'][i]
        plt.text(str_val,max_like,'Max : {}\nMean : {}'.format(max_like,mean_like),fontsize=9,color='black',
        horizontalalignment = 'left',verticalalignment = 'center',fontweight = 'bold')
    plt.grid()
    plt.legend()
    plt.draw()
    fig = plt.gcf()
    fig.savefig(join(img_save_root,'구분별좋아요수.png'),dpi=fig.dpi)
