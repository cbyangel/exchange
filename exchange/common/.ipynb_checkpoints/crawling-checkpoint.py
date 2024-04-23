import os, sys
import pandas as pd
import numpy as np
import FinanceDataReader as fdr
import requests
import time, math, datetime, urllib.request
import webbrowser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager



class C_CRAWLING:
    def __init__(self, logger=None):
        self.logger = logger
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=webdriver.ChromeOptions())
       
    
    
    def download_us_bond_to_csv(self, url, us_bond_to_csv, type_year, slack_alert, sleeped_sec=10):
        try:
            self.driver.get(url)
            content = BeautifulSoup(self.driver.page_source, 'html.parser')
            containers = content.find('table', 'freeze-column-w-1 w-full overflow-x-auto text-xs leading-4').find('tbody').find_all('tr')

            list_dt, list_close, list_open, list_high, list_low, list_change = [], [], [], [], [], []
            for idx in range(len(containers)):
                list_dt.append(containers[idx].find('time')['datetime'].replace(' ', ''))
                list_tmp = [ float(td.text)  for td in containers[idx].find_all('td', {'class':'min-w-[77px]'})  ]
                list_close.append(list_tmp[0])
                list_open.append(list_tmp[1])
                list_high.append(list_tmp[2])
                list_low.append(list_tmp[3])
                list_change.append(containers[idx].find_all('td', {'class':'datatable_cell__LJp3C'})[-1].text.replace('+', ''))

            df_us_bond_for_crawling = pd.DataFrame()
            df_us_bond_for_crawling['Date'] = list_dt
            df_us_bond_for_crawling['close'] = list_close
            df_us_bond_for_crawling['open'] = list_open
            df_us_bond_for_crawling['high'] = list_high
            df_us_bond_for_crawling['low'] = list_low
            df_us_bond_for_crawling['change'] = list_change
            
            df_us_bond = pd.read_csv(us_bond_to_csv)
            pd.concat([df_us_bond, df_us_bond_for_crawling]).drop_duplicates().sort_values(by='Date').to_csv(us_bond_to_csv, index=False)
        except Exception as e:
            self.logger.error(f"download_{type_year}_bond_to_csv : {str(e)}")
            slack_alert.send_msg(str(e))
                
                
    
    def download_oil_to_csv(self, url, oil_csv, from_year, from_mm, from_dd, slack_alert, sleeped_sec=10):
        try:
            self.driver.get(url)
            select = Select(self.driver.find_element(By.NAME, 'STA_Y'))
            select.select_by_value(from_year)
            select = Select(self.driver.find_element(By.NAME, 'STA_M'))
            select.select_by_value(from_mm)
            select = Select(self.driver.find_element(By.NAME, 'STA_D'))
            select.select_by_value(from_dd)

            el = self.driver.find_element(By.ID, 'qucik_toggle')
            el.click()
            el = self.driver.find_element(By.ID, 'div_dar')
            el.click()
            el = self.driver.find_element(By.ID, 'glopcoilSelect')
            actions = ActionChains(self.driver).move_to_element(el)
            actions.perform()
            el.click()
            time.sleep(sleeped_sec)

            content = BeautifulSoup(self.driver.page_source, 'html.parser')
            containers = content.find('table', 'tbl_type10').find(id='tbody2').find_all('tr')

            list_dt, list_dubai, list_brent, list_wti = [], [], [], []
            for idx in range(len(containers)):
                dt = containers[idx].select('td')[0].text.replace('\t', '').replace('\n', '')
                dubai = containers[idx].select('td')[1].text.replace('\t', '').replace('\n', '')
                brent = containers[idx].select('td')[2].text.replace('\t', '').replace('\n', '')
                wti = containers[idx].select('td')[3].text.replace('\t', '').replace('\n', '')

                list_dt.append(''.join(['20', dt.replace('년','-').replace('월', '-').replace('일', '')]))
                list_dubai.append(float(dubai) if dubai != '-' else np.nan)
                list_brent.append(float(brent) if brent != '-' else np.nan)
                list_wti.append(float(wti) if wti != '-' else np.nan)

            df_oil = pd.DataFrame()
            df_oil['Date'] = list_dt
            df_oil['dubai'] = list_dubai
            df_oil['brent'] = list_brent
            df_oil['wti'] = list_wti

            df_oil.to_csv(oil_csv,  index=False)
            
        except Exception as e:
            self.logger.error(f"download_oil_to_csv : {str(e)}")
            slack_alert.send_msg(str(e))
                

                
    def download_bb_junkbond_to_csv(self, url, bb_bond_tmp_csv, bb_hist_csv, slack_alert, sleeped_sec=10):
        try:
            self.driver.get(url)
     
            el = self.driver.find_element(By.ID, 'download-button')
            el.click()
            time.sleep(sleeped_sec)

            content = BeautifulSoup(self.driver.page_source, 'html.parser')
            csv = requests.get('https://fred.stlouisfed.org' + content.find('a', 'dropdown-item fg-download-csv-chart-gtm fg-download-gtm')['href'])
            open(bb_bond_tmp_csv, 'wb').write(csv.content)
            time.sleep(sleeped_sec)
            
            df_bb_tmp = pd.read_csv(bb_bond_tmp_csv, names=['Date', 'hybb'], skiprows=1)
            df_bb_bond = pd.read_csv(bb_hist_csv, names=['Date', 'hybb'], skiprows=1)
            pd.concat([df_bb_bond, df_bb_tmp]).drop_duplicates().sort_values(by='Date').to_csv(bb_hist_csv,  index=False)
            
        
        except Exception as e:
            self.logger.error(f"download_bb_junkbond_to_csv : {str(e)}")
            slack_alert.send_msg(str(e))
                
                
                
                
    def download_naver_to_csv(self, url, naver_keyword_csv, client_id, client_secret, dt, slack_alert):
        try:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",client_id)
            request.add_header("X-Naver-Client-Secret",client_secret)
            request.add_header("Content-Type","application/json")
            
            
            body_dict={} #검색 정보를 저장할 변수
            body_dict['startDate']='2016-01-01'
            body_dict['endDate']=dt
            body_dict['timeUnit']='date'
            body_dict['keywordGroups']=[ {'groupName':'환율 전망', 'keywords':['환율 전망']} ]
            body=str(body_dict).replace("'",'"') # ' 문자로는 에러가 발생해서 " 로 변환

            response = urllib.request.urlopen(request, data=body.encode("utf-8"))
            rescode = response.getcode()
            if(rescode==200):
                response_body = response.read()
                dict_naver_index = response_body.decode('utf-8')
            else:
                self.logger.error("Error Code:" + rescode)
                
            list_naver_dt = [d['period'] for d in eval(dict_naver_index)['results'][0]['data']]
            list_naver_idx = [d['ratio'] for d in eval(dict_naver_index)['results'][0]['data']]

            df_naver = pd.DataFrame({'Date':list_naver_dt, 'keyword':list_naver_idx})
            df_naver.to_csv(naver_keyword_csv, index=False)
              
        except Exception as e:
            self.logger.error(f"download_naver_to_csv : {str(e)}")
            slack_alert.send_msg(str(e))
