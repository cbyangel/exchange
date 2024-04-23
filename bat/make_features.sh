#!/usr/bin/env bash

WORK_DIR=$(dirname $0)

. $WORK_DIR/configure.sh 


echo "python $EXCHANGE_DIR/make_features.py --dt $TDY --naver_keyword_csv $NAVER_KEYWORD_CSV --kr_oil_hist_csv $KR_OIL_HIST_CSV --us_10y_hist_csv $US_10Y_HIST_CSV --us_1y_hist_csv $US_1Y_HIST_CSV --us_bb_hist_csv $US_BB_HIST_CSV --train_csv $TRAIN_CSV --log_dir $LOG_DIR"
python $EXCHANGE_DIR/make_features.py --dt $TDY --naver_keyword_csv $NAVER_KEYWORD_CSV --kr_oil_hist_csv $KR_OIL_HIST_CSV --us_10y_hist_csv $US_10Y_HIST_CSV --us_1y_hist_csv $US_1Y_HIST_CSV --us_bb_hist_csv $US_BB_HIST_CSV --train_csv $TRAIN_CSV --log_dir $LOG_DIR


rc=$?
if [ $rc -ne 0 ]; then
    error_msg="[ERROR] 2. make_features "
    echo $error_msg
    #aiflow-alert --conf $CONF_DIR/msg_alerts.py --msg "$error_msg" 
    exit $rc
fi  