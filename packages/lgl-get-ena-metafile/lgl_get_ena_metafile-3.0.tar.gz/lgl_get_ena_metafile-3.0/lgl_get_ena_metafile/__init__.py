#-*- codeing = utf-8 -*-
#@time : 2021-08-12 18:30
#@Author : liugeliang
#@File : __init__.py
#@Software : PyCharm

import os
import shutil
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

def dir_judge(dir_path):
    if os.path.exists(dir_path) == True:
        pass
    else:
        print(f"{dir_path}路径不存在，已自动创建路径！")
        os.mkdir(dir_path)

def get_ena_metafile(input_list_txt,download_path,chromedriver):
    dir_judge(download_path)
    #日志文件
    log_path = os.path.join(download_path, 'log')
    log_file_path = os.path.join(download_path, 'log/history.txt')
    error_file_path = os.path.join(download_path, 'log/error_number.txt')


    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
          "download.default_directory": download_path,   ##设置浏览器下载路径
          "download.prompt_for_download": False,
        })
    chrome_options.add_argument("--headless")  ##设置无头浏览
    chrome_options.add_argument('--disable-gpu')
    driver=webdriver.Chrome(options=chrome_options,executable_path = chromedriver)

    txt = open(input_list_txt, 'r')
    txt_list = txt.read()
    txt.close()
    number_list = txt_list.split('\n')

    log_file = os.path.exists(log_file_path)
    error_file = os.path.exists(error_file_path)
    print(f"列表数据共{len(number_list)}条，注意核实，即将开始下载数据...")

    if log_file == True and error_file == True:
        print('已存在下载记录，将从未下载的编码开始下载...')
        historytxt = open(log_file_path, 'r')
        history = historytxt.read()
        historytxt.close()
        history_list = set(history.split('\n')[:-1])

        noresulttxt = open(error_file_path, 'r')
        no_result = noresulttxt.read()
        noresulttxt.close()
        noresult_list = set(no_result.split('\n')[:-1])

        number_list = list(set(number_list) - noresult_list)
        number_list = list(set(number_list) - history_list)
        print(f'剩余下载{len(number_list)}条...')
        print('=================================')

    elif log_file == True and error_file == False:
        print('已存在下载记录...')
        historytxt = open(log_file_path, 'r')
        history = historytxt.read()
        historytxt.close()
        history_list = set(history.split('\n')[:-1])
        number_list = list(set(number_list) - history_list)
        print(f'剩余下载{len(number_list)}条...')
        print('=================================')
    else:
        dir_judge(log_path)
        print("首次下载，不存在下载记录...")
        print(f"共需下载{len(number_list)}条...")
        print('=================================')

    num = 1
    for i in number_list:
        sleep(2)
        ena_url = f'https://www.ebi.ac.uk/ena/browser/view/{i}'
        print(f"正在处理第{num}个...")
        try:
            driver.get(ena_url)
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view-content-col"]/h3')))
            element = driver.find_element_by_xpath('//*[@id="view-content-col"]/h3').text
            print(element)
            sra_accession_number = element.split(': ')[1]
            download_url = f'https://www.ebi.ac.uk/ena/portal/api/filereport?accession={sra_accession_number}&result=read_run&fields=study_accession,sample_accession,experiment_accession,run_accession,tax_id,scientific_name,fastq_ftp,submitted_ftp,sra_ftp&format=tsv&download=true'
            driver.get(download_url)
            file_name = f'filereport_read_run_{sra_accession_number}_tsv.txt'
            # print(file_name)
            download_file_path = os.path.join(download_path,file_name)
            download_file_path_2 = os.path.join(download_path,f'{i}')
            while os.path.exists(download_file_path) == False:
                sleep(2)
            else:
                os.mkdir(download_file_path_2)
                print(f'{download_file_path}>>>{download_file_path_2}')
                shutil.move(download_file_path,download_file_path_2)
            with open(log_file_path, 'a') as history_record:
                history_record.write(i)
                history_record.write('\n')
        except:
            with open(error_file_path, 'a') as error_record:
                error_record.write(i)
                error_record.write('\n')
        num+=1