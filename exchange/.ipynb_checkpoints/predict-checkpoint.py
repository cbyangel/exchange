import os
import pandas as pd
import numpy as np
from common.logger import C_LOGGER
from common.preprocessing import C_PREPROCESSING
from common.args import parse_args
from setting import config
from msg_alerts import C_SLACKALERT
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError



args = parse_args(['dt', 'train_csv', 'log_dir'])


c_logger = C_LOGGER({'name': 'train', 'log_dir': args.log_dir})
c_logger.consoleHandler()
c_logger.fileHandler()
logger = c_logger.getLogger()


if __name__ == "__main__":
    try:
        c_slackalert = C_SLACKALERT(logger)
        c_preprocessing = C_PREPROCESSING()
        
        df = pd.read_csv(args.train_csv)
        c_preprocessing.set_df(df, c_slackalert)
        c_preprocessing.index_col_to_datetime(c_slackalert)
        c_preprocessing.set_index(c_slackalert)
        df = c_preprocessing.get_df()
        
        poly = PolynomialFeatures(degree=4, include_bias=True)
        scaler = StandardScaler()

        X = df.values[:, 1:6]
        y = df.values[:, 0]

        # 훈련 데이터셋 X_train 의 거듭제곱을 생성한 뒤, 훈련 데이터셋 X_train 에 새로운 변수로 추가
        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)


        X_train = X_poly[:int(len(X_poly) - 3)]
        X_test = X_poly[int(len(X_poly) - 3):]
        y_train = y[:int(len(X_poly) - 3)]
        y_test = y[int(len(X_poly) - 3):]


        lin_reg = LinearRegression()
        lin_reg.fit(X_train, y_train)
        logger.info(f"model score : {np.round(lin_reg.score(X_train, y_train), 2)}" )
        
 
        y_real = [int(y) for y in y[-3:]]
        y_pred = [int(y) for y in lin_reg.predict(X_test)]
        txt_message = f'{args.dt}\n 실제 : {y_real}\n 예측 : {y_pred}'
        c_slackalert.send_msg(txt_message)
        
    except Exception as e:
        logger.error(f" {str(e)}")
                
        
    
        
    