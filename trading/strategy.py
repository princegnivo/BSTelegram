import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from trading.indicators import TechnicalIndicators
from utils.logger import logger

class TradingStrategy:
    """Trading strategy implementation for signals"""
    
    def __init__(self):
        self.indicators = TechnicalIndicators()
    
    def analyze_1m(self, df: pd.DataFrame) -> Dict:
        """Analyze 1-minute timeframe strategy"""
        try:
            # Calculate Heikin Ashi
            ha = self.indicators.calculate_heikin_ashi(df)
            
            # Calculate Bollinger Bands (20, 2)
            bb = self.indicators.bollinger_bands(ha, period=20, deviation=2)
            
            # Calculate SMAs
            sma2 = self.indicators.sma(ha, period=2, column='ha_close')
            sma5 = self.indicators.sma(ha, period=5, column='ha_close')
            
            # Calculate RSI
            rsi = self.indicators.rsi(df, period=8)
            
            # Current values
            current = {
                'ha_close': ha['ha_close'].iloc[-1],
                'bb_lower': bb['lower'].iloc[-1],
                'bb_upper': bb['upper'].iloc[-1],
                'sma2': sma2.iloc[-1],
                'sma5': sma5.iloc[-1],
                'rsi': rsi.iloc[-1]
            }
            
            # Check for CALL signal
            call_signal = (
                current['ha_close'] <= current['bb_lower'] * 1.002 and  # Touch lower band
                current['sma2'] > current['sma5'] and  # SMA crossover up
                current['rsi'] > 30 and current['rsi'] < 60 and  # RSI conditions
                rsi.iloc[-1] > rsi.iloc[-2]  # RSI moving up
            )
            
            # Check for PUT signal
            put_signal = (
                current['ha_close'] >= current['bb_upper'] * 0.998 and  # Touch upper band
                current['sma2'] < current['sma5'] and  # SMA crossover down
                current['rsi'] > 40 and current['rsi'] < 70 and  # RSI conditions
                rsi.iloc[-1] < rsi.iloc[-2]  # RSI moving down
            )
            
            return {
                'call': bool(call_signal),
                'put': bool(put_signal),
                'ha_close': current['ha_close'],
                'bb_lower': current['bb_lower'],
                'bb_upper': current['bb_upper'],
                'rsi': current['rsi']
            }
            
        except Exception as e:
            logger.error(f"Error in 1m strategy: {e}")
            return {'call': False, 'put': False}
    
    def analyze_2m(self, df: pd.DataFrame) -> Dict:
        """Analyze 2-minute timeframe strategy"""
        try:
            # Calculate Heikin Ashi
            ha = self.indicators.calculate_heikin_ashi(df)
            
            # Calculate Bollinger Bands (6, 1.3)
            bb = self.indicators.bollinger_bands(ha, period=6, deviation=1.3)
            
            # Calculate MACD (6, 19, 6)
            macd = self.indicators.macd(df, fast=6, slow=19, signal=6)
            
            # Current values
            current = {
                'ha_close': ha['ha_close'].iloc[-1],
                'bb_lower': bb['lower'].iloc[-1],
                'bb_upper': bb['upper'].iloc[-1],
                'macd': macd['macd'].iloc[-1],
                'signal': macd['signal'].iloc[-1],
                'histogram': macd['histogram'].iloc[-1]
            }
            
            # Previous values for cross detection
            prev = {
                'macd': macd['macd'].iloc[-2],
                'signal': macd['signal'].iloc[-2],
                'histogram': macd['histogram'].iloc[-2]
            }
            
            # MACD cross conditions
            macd_cross_up = current['macd'] > current['signal'] and prev['macd'] <= prev['signal']
            macd_cross_down = current['macd'] < current['signal'] and prev['macd'] >= prev['signal']
            
            # Check for CALL signal
            call_signal = (
                macd_cross_down and  # MACD cross down
                current['histogram'] < 0 and  # Histogram below 0
                current['ha_close'] <= current['bb_lower'] * 1.005  # Near lower band
            )
            
            # Check for PUT signal
            put_signal = (
                macd_cross_up and  # MACD cross up
                current['histogram'] > 0 and  # Histogram above 0
                current['ha_close'] >= current['bb_upper'] * 0.995  # Near upper band
            )
            
            return {
                'call': bool(call_signal),
                'put': bool(put_signal),
                'ha_close': current['ha_close'],
                'bb_lower': current['bb_lower'],
                'bb_upper': current['bb_upper'],
                'macd': current['macd'],
                'signal': current['signal'],
                'histogram': current['histogram']
            }
            
        except Exception as e:
            logger.error(f"Error in 2m strategy: {e}")
            return {'call': False, 'put': False}
    
    def analyze_5m(self, df: pd.DataFrame) -> Dict:
        """Analyze 5-minute timeframe strategy"""
        # Similar to 1m but with different parameters
        return self.analyze_1m(df)
