#!/usr/bin/env bash

BAT_DIR=$(dirname $0)
HOME_DIR="$BAT_DIR/.."
EXCHANGE_DIR="$HOME_DIR/exchange"
DATA_DIR="$HOME_DIR/data"
LOG_DIR="$HOME_DIR/log"
CONF_DIR="$HOME_DIR/conf"

### for linux
# YM=$(date +'%Y%m')
# TDY=$(date +'%Y%m%d')
# YSTRDY=$(date +'%Y%m%d' -d "1 days ago")

YM=$(date '+%Y-%m')
TDY=$(date '+%Y-%m-%d')
YSTRDY=$(date -v-1d '+%Y-%m-%d')

mkdir -p "$LOG_DIR"

NAVER_KEYWORD_CSV="$DATA_DIR/naver_keyword_data.csv"
KR_OIL_HIST_CSV="$DATA_DIR/kr_oil_historical_data.csv"
US_10Y_HIST_CSV="$DATA_DIR/us_10year_bond_yield_historical_data.csv"
US_1Y_HIST_CSV="$DATA_DIR/us_1year_bond_yield_historical_data.csv"
US_BB_HIST_CSV="$DATA_DIR/us_bb_high_yield_historical_data.csv"
US_BB_TMP_CSV="$DATA_DIR/us_bb_tmp_data.csv"
TRAIN_CSV="$DATA_DIR/train.csv"

