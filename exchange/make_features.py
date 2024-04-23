import pandas as pd
import numpy as np
import FinanceDataReader as fdr
from common.preprocessing import C_PREPROCESSING
from common.logger import C_LOGGER
from common.args import parse_args
from setting import config
from msg_alerts import C_SLACKALERT


args = parse_args(['dt', 'naver_keyword_csv', 'kr_oil_hist_csv', 'us_10y_hist_csv', 'us_1y_hist_csv', 'us_bb_hist_csv', 'train_csv', 'log_dir'])


c_logger = C_LOGGER({'name': 'make_features', 'log_dir': args.log_dir})
c_logger.consoleHandler()
c_logger.fileHandler()
logger = c_logger.getLogger()


if __name__ == "__main__":
    
    c_preprocessing = C_PREPROCESSING()
    c_slackalert = C_SLACKALERT(logger)
    
    df_usd_krw = fdr.DataReader('USD/KRW', '2016-01-01')
    c_preprocessing.set_df(df_usd_krw, slack_alert=c_slackalert)
    c_preprocessing.drop_duplicates({'Open':'max', 'High':'max', 'Low':'max', 'Close':'max', 'Volume':'max'}, slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'Close', 'y', slack_alert=c_slackalert)
    df_usd_krw = c_preprocessing.get_df()
    
      
    df_kospi = fdr.DataReader('KS11', '2016-01-01')
    c_preprocessing.set_df(df_kospi, slack_alert=c_slackalert)
    c_preprocessing.drop_duplicates({'Open':'max', 'High':'max', 'Low':'max', 'Close':'max', 'Volume':'max'}, slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'Close', 'close_kospi', slack_alert=c_slackalert)
    df_kospi = c_preprocessing.get_df()
    
    
    c_preprocessing.csv_to_df(args.kr_oil_hist_csv, slack_alert=c_slackalert)
    c_preprocessing.index_col_to_datetime(slack_alert=c_slackalert)
    c_preprocessing.set_index(slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'dubai', 'dubai', slack_alert=c_slackalert)
    df_oil = c_preprocessing.get_df()
    
    
    c_preprocessing.csv_to_df(args.us_10y_hist_csv, slack_alert=c_slackalert)
    c_preprocessing.index_col_to_datetime(slack_alert=c_slackalert)
    c_preprocessing.set_index(slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'close', 'close_10y', slack_alert=c_slackalert)
    df_us_bond_10y = c_preprocessing.get_df()
    
    
    c_preprocessing.csv_to_df(args.us_1y_hist_csv, slack_alert=c_slackalert)
    c_preprocessing.index_col_to_datetime(slack_alert=c_slackalert)
    c_preprocessing.set_index(slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'close', 'close_1y', slack_alert=c_slackalert)
    df_us_bond_1y = c_preprocessing.get_df()
    
    
    c_preprocessing.csv_to_df(args.us_bb_hist_csv, slack_alert=c_slackalert)
    c_preprocessing.index_col_to_datetime(slack_alert=c_slackalert)
    c_preprocessing.set_index(slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'hybb', 'hybb', slack_alert=c_slackalert)
    df_us_bond_bb = c_preprocessing.get_df()
    
    
    c_preprocessing.csv_to_df(args.naver_keyword_csv, slack_alert=c_slackalert)
    c_preprocessing.index_col_to_datetime(slack_alert=c_slackalert)
    c_preprocessing.set_index(slack_alert=c_slackalert)
    c_preprocessing.filter_and_rename('2016-01-01', 'keyword', 'keyword', slack_alert=c_slackalert)
    df_naver_kwd = c_preprocessing.get_df()
    
    
    df_us_bond = df_us_bond_10y.join(df_us_bond_1y)
    df_us_bond['close_diff'] = df_us_bond['close_10y'] - df_us_bond['close_1y']
    df_us_bond = df_us_bond[['close_diff']]
        
    df_data = df_usd_krw.join(df_kospi, how='left').join(df_oil, how='left')\
                .join(df_us_bond, how='left').join(df_us_bond_bb, how='left').join(df_naver_kwd, how='left')
    
    df_data.loc[df_data.hybb == '.', 'hybb'] = None
    df_data.fillna(method='pad', inplace=True)
    df_data.fillna(method='bfill', inplace=True)

    df_data.to_csv(args.train_csv)

  