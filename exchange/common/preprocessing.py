import pandas as pd
import numpy as np



class C_PREPROCESSING:
    def __init__(self, logger=None):
        self.logger = logger
        self.df = None
        
        
        
    def set_df(self, df, slack_alert):
        try:
            self.df = df
        except Exception as e:
            self.logger.error(f"set_df : {str(e)}")
            slack_alert.send_msg(str(e))    
        
        
    def csv_to_df(self, file, slack_alert):
        try:
            self.df = pd.read_csv(file)
        except Exception as e:
            self.logger.error(f"csv_to_df : {str(e)}")
            slack_alert.send_msg(str(e))  
        
        
    def index_col_to_datetime(self, slack_alert, index_col='Date'):
        try:
            self.df[index_col] = pd.to_datetime(self.df[index_col])
        except Exception as e:
            self.logger.error(f"index_col_to_datetime : {str(e)}")
            slack_alert.send_msg(str(e))  
            
            
    def set_index(self, slack_alert, index_col='Date'):
        try:
            self.df.set_index(index_col, inplace=True)
        except Exception as e:
            self.logger.error(f"set_index : {str(e)}")
            slack_alert.send_msg(str(e))  
            
    
    def drop_duplicates(self, dict_dtype, slack_alert, index_col='Date'):
        try:
            self.df = self.df.groupby(index_col).agg(dict_dtype)
        except Exception as e:
            self.logger.error(f"drop_duplicates : {str(e)}")
            slack_alert.send_msg(str(e))  
        
        
    def filter_and_rename(self, from_dt, col_name, conv_name, slack_alert, index_col='Date'):
        try:
            self.df = self.df[self.df.index >= from_dt][[col_name]].rename(columns={col_name:conv_name})
        except Exception as e:
            self.logger.error(f"filter_and_rename : {str(e)}")
            slack_alert.send_msg(str(e))  
        
        
    def get_df(self):
        return self.df

    
    
    
    
        