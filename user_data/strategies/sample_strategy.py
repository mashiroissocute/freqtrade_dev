# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
import requests
from pandas import DataFrame
from typing import Optional, Union
import time
import hmac
import hashlib
import base64
import urllib.parse

from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IStrategy, IntParameter)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# This class is a sample. Feel free to customize it.
class SampleStrategy(IStrategy):
    """
    This is a sample strategy to inspire you.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_entry_trend, populate_exit_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 10000
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -1

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0  # Disabled / not configured

    # Optimal timeframe for the strategy.
    timeframe = '1m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True


    # Hyperoptable parameters
    # emaThr = IntParameter(5, 55, default=200, space="buy")
    period = IntParameter(5, 205, default=1440, space="buy")
    highThr = IntParameter(0, 1, default=0.9, space="buy")
    lowThr = IntParameter(0, 1, default=1.1, space="buy")
    

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 1440

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }


    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """
       
        # EMA
        # dataframe['ema'] = ta.EMA(dataframe, timeperiod=self.emaThr.value)
        dataframe['highest'] = dataframe['high'].rolling(window=self.period.value).max()
        dataframe['lowest'] = dataframe['low'].rolling(window=self.period.value).min()
        # print(dataframe)
        
        # 假设你已经有了一个钉钉机器人的Webhook URL
        dingtalk_webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=126085542789784e1578a069991f6ad19f4ea6885d7e3148fa39eb948e6f38d3'
        timestamp = str(round(time.time() * 1000))
        secret = 'SECaf6f152b63d44f6f19141fedf2ae46f45dfea5583fafced82e9bae68f659d7c5'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        timestamp = '&timestamp=' + timestamp
        sign = '&sign=' + sign
        dingtalk_webhook_url = dingtalk_webhook_url + timestamp + sign
        
        
        # 计算告警条件
        high_alert_condition = dataframe['close'].iloc[-1] / dataframe['highest'].iloc[-1] < self.highThr.value
        low_alert_condition = dataframe['close'].iloc[-1] / dataframe['lowest'].iloc[-1] > self.lowThr.value

        info_message = f"{metadata['pair']}---最高价{dataframe['highest'].iloc[-1]}---最低价{dataframe['lowest'].iloc[-1]}---当前价{dataframe['close'].iloc[-1]}"
        print(info_message)

        # 如果存在告警条件，发送告警消息到钉钉
        if high_alert_condition.any():
            alert_message = f"{metadata['pair']}---最高价{dataframe['highest'].iloc[-1]}---当前价{dataframe['close'].iloc[-1]}"
            payload = {
                "msgtype": "text",
                "text": {
                    "content": alert_message
                }
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(dingtalk_webhook_url, json=payload, headers=headers)
        #     if response.status_code == 200:
        #         print("告警消息已成功发送到钉钉")
        #         print(alert_message)
        #     else:
        #         print("告警消息发送失败，错误码：", response.status_code)
        # else:
        #     print("未触发告警条件")

        
        
        if low_alert_condition.any():
            alert_message = f"{metadata['pair']}---最低价{dataframe['lowest'].iloc[-1]}---当前价{dataframe['close'].iloc[-1]}"
            payload = {
                "msgtype": "text",
                "text": {
                    "content": alert_message
                }
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(dingtalk_webhook_url, json=payload, headers=headers)
        #     if response.status_code == 200:
        #         print("告警消息已成功发送到钉钉")
        #         print(alert_message)
        #     else:
        #         print("告警消息发送失败，错误码：", response.status_code)
        # else:
        #     print("未触发告警条件")

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        dataframe.loc[
            (
                (dataframe['volume'] < 0)  # Make sure Volume is not 0
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        dataframe.loc[
            (
            ),

            'exit_long'] = 0

        return dataframe
