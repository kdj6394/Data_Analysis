# train data refine

from lib import *

if __name__ == '__main__':
    # refine data
    root = sys.argv[1]
    raw_data = join(root,'train.jsonl')

    with open(raw_data,'r',encoding='utf-8') as raw:
        datas = raw.readlines()

    save_path = join(root,'article_original.txt')

    with open(save_path,'w',encoding='utf-8') as s_p:
        for data in tqdm(datas,ascii=True):
            data = json.loads(data)
            data_ori = data['article_original']
            string = f"{data_ori}\n"
            s_p.writelines(string)