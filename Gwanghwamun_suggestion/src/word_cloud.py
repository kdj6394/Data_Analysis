from lib import os,glob,sys,join,basename,dirname
from lib import np,pd,plt
plt.rc('font',family='Malgun Gothic')
from lib import WordCloud,Image,ImageColorGenerator,Komoran,nltk
from lib import Okt
from lib import warnings
warnings.filterwarnings(action='ignore')

def make_mask_word(img_path,font_path,data,str_color):
    img_mask = np.array(Image.open(img_path))
    word = WordCloud(min_font_size=20,max_font_size=200,
            font_path=font_path,background_color=(255,255,255),mask=img_mask,
            colormap=str_color).generate_from_frequencies(text_data)
    plt.figure(figsize=(10,10))
    plt.axis('off')
    plt.margins(x=0,y=0)
    plt.imshow(word,interpolation="bilinear")
    plt.draw()
    fig = plt.gcf()
    return fig

def make_word(font_path,data):
    word = WordCloud(min_font_size=1,max_font_size=100,
                        font_path=font_path,background_color=(255,255,255)
                        ).generate_from_frequencies(data)
    plt.figure(figsize=(10,10))
    plt.title(x,fontsize=30)
    plt.axis('off')
    plt.margins(x=0,y=0)
    plt.imshow(word,interpolation="bilinear")
    plt.draw()
    fig = plt.gcf()
    return fig



if __name__ == '__main__':
    root = sys.argv[1]
    img_path = sys.argv[2]
    font_path = sys.argv[3]

    img_save_root = join(dirname(root),'src','img')
    os.makedirs(img_save_root,exist_ok=True)
    data_path = glob.glob(join(root,'*.txt'))[-1]
    data = pd.read_csv(data_path,sep='\t',header=None,encoding='utf8')
    data.columns = ['구분','진행상황','생성날짜','ID','좋아요수','제목','내용']

    text_df = pd.DataFrame(data['내용'])
    text_data = str(np.array(text_df['내용'].tolist()))
    stop = set()
    stop.update(['인','해','또한','이','내','다른','등','위','가장','다시','도','것','더'])
    okt = Okt()
    text_data = okt.nouns(text_data)
    text_data = [each_word for each_word in text_data if each_word not in stop]
    text_data = nltk.Text(text_data)
    text_data = text_data.vocab().most_common(1000)
    text_data = dict(text_data)
    fig = make_mask_word(img_path,font_path,text_data,'Dark2')
    fig.savefig(join(img_save_root,'all_word_cloud.png'),dpi=fig.dpi)


    division_word_cloud = join(img_save_root,'division_word_cloud')
    os.makedirs(division_word_cloud,exist_ok=True)

    division_text_df = pd.DataFrame(data[['구분','내용']])
    for_division_list = division_text_df['구분'].unique()

    for x in for_division_list:
        text_df = division_text_df[division_text_df['구분'] == x]
        text_df = text_df.iloc[:,1:]
        text_data = str(np.array(text_df['내용'].tolist()))
        stop = set()
        stop.update(['인','것','등','이','시','제안','내용','수','각','더','및','회'])
        okt = Okt()
        text_data = okt.nouns(text_data)
        text_data = [each_word for each_word in text_data if each_word not in stop]
        text_data = nltk.Text(text_data)
        text_data = text_data.vocab().most_common(1000)
        text_data = dict(text_data)

        division_fig = make_word(font_path,text_data)
        division_fig.savefig(join(division_word_cloud,x+'_word_cloud.png'),dpi=fig.dpi)



    date_text_df = pd.DataFrame(data[['생성날짜','내용']])
    check_date_text_df = date_text_df['생성날짜'].value_counts()
    print(check_date_text_df)
    for_date_list = ['2020-04-01','2018-10-30','2019-03-04','2019-04-30','2019-03-05','2020-03-31',
                    '2019-11-21','2019-03-30','2019-10-10','2020-04-04','2019-10-11','2019-11-07','2019-11-20']

    date_word_cloud_path = join(img_save_root,'date_word_cloud')
    os.makedirs(date_word_cloud_path,exist_ok=True)

    for x in for_date_list:
        text_df = date_text_df[date_text_df['생성날짜'] == x]
        text_df = text_df.iloc[:,1:]
        text_data = str(np.array(text_df['내용'].tolist()))
        stop = set()
        stop.update(['인','이','수','위','함','및','등','것','시','제안','내용','각','더'])
        okt = Okt()
        text_data = okt.nouns(text_data)
        text_data = [each_word for each_word in text_data if each_word not in stop]
        text_data = nltk.Text(text_data)
        text_data = text_data.vocab().most_common(1000)
        text_data = dict(text_data)

        date_fig = make_word(font_path,text_data)
        date_fig.savefig(join(date_word_cloud_path,x+'_word_cloud.png'),dpi=date_fig.dpi)