#!/usr/bin/env bash

WORK_DIR=$(dirname $0)

. $WORK_DIR/configure.sh 


echo "python $EXCHANGE_DIR/predict.py --dt $TDY --train_csv $TRAIN_CSV --log_dir $LOG_DIR"
python $EXCHANGE_DIR/predict.py --dt $TDY --train_csv $TRAIN_CSV --log_dir $LOG_DIR


rc=$?
if [ $rc -ne 0 ]; then
    error_msg="[ERROR] 3. predict "
    echo $error_msg
    #aiflow-alert --conf $CONF_DIR/msg_alerts.py --msg "$error_msg" 
    exit $rc
fi  