import pandas as pd
import numpy as np
from common.crawling import C_CRAWLING
from common.logger import C_LOGGER
from common.args import parse_args
from setting import config
from msg_alerts import C_SLACKALERT



args = parse_args(['dt', 'naver_keyword_csv', 'kr_oil_hist_csv', 'us_10y_hist_csv', 'us_1y_hist_csv', 'us_bb_hist_csv', 'us_bb_tmp_csv', 'log_dir'])


c_logger = C_LOGGER({'name': 'prepare_data', 'log_dir': args.log_dir})
c_logger.consoleHandler()
c_logger.fileHandler()
logger = c_logger.getLogger()


if __name__ == "__main__":
    
    c_slackalert = C_SLACKALERT(logger)
    c_crawling = C_CRAWLING(logger)
    url = 'https://www.opinet.co.kr/glopcoilSelect.do'
    c_crawling.download_oil_to_csv(url, args.kr_oil_hist_csv, '2008', '01', '01', slack_alert=c_slackalert, sleeped_sec=30)
    
    url = 'https://fred.stlouisfed.org/series/BAMLH0A1HYBB'
    c_crawling.download_bb_junkbond_to_csv(url, args.us_bb_tmp_csv, args.us_bb_hist_csv, slack_alert=c_slackalert, sleeped_sec=30)
    
    url = 'https://kr.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data'
    c_crawling.download_us_bond_to_csv(url, args.us_10y_hist_csv, '10y', slack_alert=c_slackalert, sleeped_sec=30)
    
    
    url = 'https://kr.investing.com/rates-bonds/u.s.-1-year-bond-yield-historical-data'
    c_crawling.download_us_bond_to_csv(url, args.us_1y_hist_csv, '1y', slack_alert=c_slackalert, sleeped_sec=30)

    url = "https://openapi.naver.com/v1/datalab/search"
    c_crawling.download_naver_to_csv(url, args.naver_keyword_csv, config.NAVER_CLIENT_ID, config.NAVER_CLIENT_SECRET, args.dt, slack_alert=c_slackalert)


  