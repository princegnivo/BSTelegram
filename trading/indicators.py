import pandas as pd
import numpy as np
from typing import Tuple, Optional

class TechnicalIndicators:
    """Technical indicators calculator for trading strategies"""
    
    @staticmethod
    def calculate_heikin_ashi(df: pd.DataFrame) -> pd.DataFrame:
        """Calculate Heikin Ashi candles"""
        ha = pd.DataFrame(index=df.index)
        
        # Calculate Heikin Ashi
        ha['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
        ha['ha_open'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
        ha['ha_open'].fillna(df['open'], inplace=True)
        
        ha['ha_high'] = ha[['ha_open', 'ha_close']].max(axis=1)
        ha['ha_high'] = ha[['ha_high', df['high']]].max(axis=1)
        
        ha['ha_low'] = ha[['ha_open', 'ha_close']].min(axis=1)
        ha['ha_low'] = ha[['ha_low', df['low']]].min(axis=1)
        
        return ha
    
    @staticmethod
    def bollinger_bands(df: pd.DataFrame, period: int = 20, deviation: float = 2) -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        bb = pd.DataFrame(index=df.index)
        bb['middle'] = df['close'].rolling(window=period).mean()
        bb['std'] = df['close'].rolling(window=period).std()
        bb['upper'] = bb['middle'] + (bb['std'] * deviation)
        bb['lower'] = bb['middle'] - (bb['std'] * deviation)
        return bb
    
    @staticmethod
    def sma(df: pd.DataFrame, period: int, column: str = 'close') -> pd.Series:
        """Calculate Simple Moving Average"""
        return df[column].rolling(window=period).mean()
    
    @staticmethod
    def macd(df: pd.DataFrame, fast: int = 6, slow: int = 19, signal: int = 6) -> pd.DataFrame:
        """Calculate MACD"""
        macd_df = pd.DataFrame(index=df.index)
        macd_df['macd'] = df['close'].ewm(span=fast, adjust=False).mean() - df['close'].ewm(span=slow, adjust=False).mean()
        macd_df['signal'] = macd_df['macd'].ewm(span=signal, adjust=False).mean()
        macd_df['histogram'] = macd_df['macd'] - macd_df['signal']
        return macd_df
    
    @staticmethod
    def rsi(df: pd.DataFrame, period: int = 8) -> pd.Series:
        """Calculate RSI"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
