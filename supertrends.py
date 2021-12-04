import ccxt as ccxt
import pandas as pd


def get_ohlcv(exchange_name: str, symbol: str) -> pd.DataFrame:
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class()
    bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
    dataframe = pd.DataFrame(
        bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='ms')
    return dataframe


def get_true_range(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['previous_close'] = dataframe['close'].shift(1)
    dataframe['(high-low)'] = dataframe['high'] - dataframe['low']
    dataframe['(high-previous_close)'] = abs(dataframe['high'] -
                                             dataframe['previous_close'])
    dataframe['(low-previous_close)'] = abs(dataframe['low'] -
                                            dataframe['previous_close'])
    dataframe['TR'] = dataframe[[
        '(high-low)', '(high-previous_close)', '(low-previous_close)']].max(axis=1)

    return dataframe


def get_average_true_range(dataframe: pd.DataFrame, period: int, multiplier: int) -> pd.DataFrame:
    dataframe['ATR'] = dataframe['TR'].rolling(period).mean()
    dataframe['upperband'] = (
        dataframe['high']+dataframe['low'] / 2) + (dataframe['ATR']*multiplier)
    dataframe['lowerband'] = (
        dataframe['high']+dataframe['low'] / 2) - (dataframe['ATR']*multiplier)
    trend_values = [True]

    for current_idx in range(1, len(dataframe.index)):
        prev_idx = current_idx - 1
        if (dataframe['close'][current_idx] > dataframe['upperband'][prev_idx]):
            trend_values.append(True)
        elif (dataframe['close'][current_idx] < dataframe['lowerband'][prev_idx]):
            trend_values.append(False)
        else:
            trend_values.append(trend_values[-1])

    dataframe['in_uptrend'] = trend_values
    return dataframe


def get_supertrend(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe = get_true_range(dataframe)
    dataframe = get_average_true_range(dataframe, 7, 3)
    return dataframe


def check_for_signals(exchange_name: str, symbol: str):
    ohlcv_dataframe = get_ohlcv(exchange_name, symbol)
    dataframe = get_supertrend(ohlcv_dataframe)
    print(dataframe.tail(2))

    if not dataframe['in_uptrend'].iloc[-2] and dataframe['in_uptrend'].iloc[-1]:
        print("Changed to Uptrend, BUY!!!!!!")

    if dataframe['in_uptrend'].iloc[-2] and not dataframe['in_uptrend'].iloc[-1]:
        print("Changed to Downtrend, SELL!!!!!!")
