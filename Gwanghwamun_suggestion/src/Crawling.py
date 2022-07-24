from lib import os,glob,sys,join,basename,dirname
from lib import bs,webdriver
from lib import time,tqdm
from lib import Options

def Time_convert():
    now = time.localtime()
    now_convert = '%04d-%02d-%02d,%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    return now_convert

if __name__ == '__main__':
    driver_path = sys.argv[1]
    save_path = sys.argv[2]
    save_file = join(save_path,str(Time_convert()) + '_data.txt')

    driver = webdriver.Chrome(driver_path)
    url = r'https://www.gwanghwamoon1st.go.kr/front/propseTalk/propseTalkListPage.do' # Gwanghwamun suggestion page
    driver.set_window_size(1920,1080) # Can't find any button other than full size (selector)
    driver.get(url)
    driver.implicitly_wait(3)

    last_page_html = driver.page_source
    last_page_soup = bs(last_page_html,'html.parser')
    last_page = last_page_soup.select('button[title=마지막]')[0]['onclick']
    last_page_index = int(str(last_page).replace('go_Page','').replace('(','').replace(')',''))
    time.sleep(1)

    txt = []
    for i in tqdm(range(0,int(last_page_index/10)),desc='Crawling'):
        for x in range(1,11):
            x_page = '#list_div > p.paging.web_only > span > a:nth-child({})'.format(x)
            try:
                if x == 10:
                    driver.find_elements_by_css_selector(x_page)[0].click()
                    time.sleep(1)
                    next_page = driver.find_element_by_xpath('//*[@id="list_div"]/p[1]/button[3]')
                    next_page.click()
                    time.sleep(1)
                else:
                    time.sleep(1)
                    driver.find_elements_by_css_selector(x_page)[0].click()
                    time.sleep(1)
            except:
                pass

            html = driver.page_source
            soup = bs(html,'html.parser')
            tit_box_list = soup.select('div[class=tit_box]')
            title_list = soup.select('strong')[:-1] # last elemnet strong is '개인정보처리방침'
            text_list = soup.select('p[class=text]')
            make_date_list = soup.select('div[class=bottom]')
            user_list = soup.select('span[class=user]')
            like_list = soup.select('li[class=like]')

            for tit_box,title,text,make_date,user,like in zip(tit_box_list,title_list,text_list,make_date_list,user_list,like_list):
                division = tit_box.text.replace(' ','').split('\n')[1]
                situation = tit_box.text.replace(' ','').split('\n')[2]
                text = text.text.replace('\n','').split('\xa0')
                make_date = make_date.text.replace('\n','').replace(' ','').split(':')[1][:10]
                user = user.text.replace('\n','').replace(' ','')
                like = like.text.replace('\n','').replace(' ','').replace('좋아요수','')
                string = f"{division}\t{situation}\t{make_date}\t{user}\t{like}\t{title.text}\t{text}\n"
                txt.append(str(string))

    driver.quit()

    with open(save_file,'w',encoding='utf-8') as f:
        f.writelines(txt)


