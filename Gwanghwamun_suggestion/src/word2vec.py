from lib import os,glob,sys,tqdm
from lib import join,basename,dirname
from lib import pd,np,re,plt,fm,openpyxl,sns
from lib import warnings
warnings.filterwarnings(action='ignore')
from lib import Okt,word2vec,DBSCAN,KMeans
from lib import TSNE,matplotlib


def make_vec_model(data,save_root,data_name : str,window_int : int,min_cnt : int):
    okt = Okt()
    result = []
    for line in tqdm(data):
        malist = okt.pos(line, norm=True, stem=True)
        r = []
        for word in malist:
            if not word[1] in ['Josa','Eomi','Punctuation']:
                if len(word[0]) > 1:
                    r.append(word[0])
        rl = (' '.join(r))
        result.append(rl)
    
    data_save_path = join(save_root,data_name + '.nlp')
    with open(data_save_path,'w',encoding='utf-8') as f:
        f.write("\n".join(result))
    
    wData = word2vec.LineSentence(data_save_path)
    wModel =word2vec.Word2Vec(wData, size=100, window=window_int, workers=4 ,min_count=min_cnt, sg=1)
    wModel.save(data_save_path+'.model')
    model = word2vec.Word2Vec.load(data_save_path+'.model')

    return model


def kmeans(model,num_cluster : int):
    num_cluster = num_cluster
    word_vectors = model.wv.syn0
    kmeans_clustering = KMeans(n_clusters=num_cluster)
    idx = kmeans_clustering.fit_predict(word_vectors)
    idx = list(idx)

    names = model.wv.index2word
    word_centroid_map = {names[i]: idx[i] for i in range(len(names))}
    cluster_dict = dict()

    for c in range(num_cluster):
        words_list = list()
        cluster_values = list(word_centroid_map.values())
        for i in range(len(cluster_values)):
            if (cluster_values[i] == c):
                words_list.append(list(word_centroid_map.keys())[i])            
        for w in words_list:
            cluster_dict[w] = c

    vocab = list(model.wv.vocab)
    X = model[vocab]
    print('num_cluster =',num_cluster,' , ','vocab =',len(vocab))

    tsne = TSNE(n_components=2,perplexity=40,init='random')
    X_tsne = tsne.fit_transform(X)
    df = pd.DataFrame(X_tsne, index=vocab, columns=["x", "y"])
    df['cluster'] = np.nan
    for v in vocab:
        df.loc[str(v),'cluster'] = cluster_dict[v]

    return df,num_cluster


def plot_scatter(df,cluster_cnt : int,font_path,plt_title : str):
    prop = fm.FontProperties(fname=font_path)
    cluster_df = df.groupby(df['cluster'])
    cluster_mean = cluster_df.mean()
    cluster_mean['cluster'] = np.nan

    for i in range(0,cluster_cnt):
        cluster_mean.loc[i,'cluster'] = i

    ax = sns.scatterplot(x='x', y='y',hue='cluster',s=30,data=df)
    for word, pos in list(df.iterrows()):
        annotate_coords = (pos['x'],pos['y'])
        ax.annotate(word, annotate_coords , fontsize=11, fontproperties=prop)

    ax = sns.scatterplot(x='x', y='y',s=220,hue='cluster',data=cluster_mean)
    for index, pos in list(cluster_mean.iterrows()):
        annotate_coords = (pos['x'],pos['y'])
        ax.annotate('Cluster' +'_'+ str(index), annotate_coords, fontsize = 11, fontproperties=prop)

    ax.legend_.remove()
    plt.title(plt_title,fontsize=24)
    plt.show()


if __name__ == '__main__':
    root = sys.argv[1]
    font_path = sys.argv[2]
       
    img_save_root = join(dirname(root),'src','img')
    save_root = join(dirname(root),'src','word2vec')
    os.makedirs(save_root,exist_ok=True)

    data_path = glob.glob(join(root,'*.txt'))[-1]
    data = pd.read_csv(data_path,sep='\t',header=None,encoding='utf8')
    data.columns = ['구분','진행상황','생성날짜','ID','좋아요수','제목','내용']


    title_data = data['제목']
    title = list(title_data)
    title_model = make_vec_model(title,save_root,'title',window_int=3,min_cnt=19)
    title_df,title_num_cluster = kmeans(title_model,num_cluster=5)
    plot_scatter(title_df,title_num_cluster,font_path,plt_title='Title')


    text_data = data['내용']
    text = list(text_data)
    text_model = make_vec_model(text,save_root,'text',window_int=5,min_cnt=230)
    text_df,text_num_cluster = kmeans(text_model,num_cluster=6)
    plot_scatter(text_df,text_num_cluster,font_path,plt_title='Text')