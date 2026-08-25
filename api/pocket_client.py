import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
import websockets
from pydantic import BaseModel
from utils.logger import logger
from config.settings import settings

class TradeSignal(BaseModel):
    asset: str
    direction: str  # CALL or PUT
    entry_time: datetime
    expiration: int  # in minutes
    entry_price: float
    indicators: Dict[str, Any]

class PocketOptionClient:
    """Async client for Pocket Option API"""
    
    def __init__(self, ssid: str = None):
        self.ssid = ssid or settings.POCKET_SSID
        self.is_demo = settings.POCKET_DEMO
        self.ws = None
        self.is_connected = False
        self.assets = {}
        self.last_payouts = {}
        
    async def connect(self) -> bool:
        """Establish WebSocket connection to Pocket Option"""
        try:
            # WebSocket URL for Pocket Option
            ws_url = "wss://ws.pocketoption.com/websocket"
            
            self.ws = await websockets.connect(
                ws_url,
                extra_headers={
                    "Cookie": f"ssid={self.ssid}"
                }
            )
            
            # Send authentication message
            auth_msg = {
                "name": "auth",
                "msg": {
                    "session": self.ssid,
                    "is_demo": self.is_demo
                }
            }
            await self.ws.send(json.dumps(auth_msg))
            
            # Wait for auth response
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get('status') == 'success':
                self.is_connected = True
                logger.info("Connected to Pocket Option successfully")
                return True
            else:
                logger.error(f"Authentication failed: {data}")
                return False
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    async def get_assets(self) -> Dict:
        """Get available assets with payouts"""
        try:
            if not self.is_connected:
                await self.connect()
            
            # Request assets list
            msg = {
                "name": "get_assets",
                "msg": {}
            }
            await self.ws.send(json.dumps(msg))
            
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get('status') == 'success':
                self.assets = data.get('data', {})
                return self.assets
            else:
                logger.error(f"Failed to get assets: {data}")
                return {}
                
        except Exception as e:
            logger.error(f"Error getting assets: {e}")
            return {}
    
    async def get_payout(self, asset: str, timeframe: str = "1m") -> Optional[float]:
        """Get payout percentage for specific asset"""
        try:
            if not self.is_connected:
                await self.connect()
            
            msg = {
                "name": "get_payout",
                "msg": {
                    "asset": asset,
                    "timeframe": timeframe
                }
            }
            await self.ws.send(json.dumps(msg))
            
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get('status') == 'success':
                payout = data.get('data', {}).get('payout')
                if payout is not None:
                    self.last_payouts[asset] = payout
                    return payout
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting payout for {asset}: {e}")
            return None
    
    async def get_candles(self, asset: str, timeframe: int, count: int = 100) -> pd.DataFrame:
        """Get candlestick data for asset"""
        try:
            if not self.is_connected:
                await self.connect()
            
            msg = {
                "name": "get_candles",
                "msg": {
                    "asset": asset,
                    "timeframe": timeframe,
                    "count": count
                }
            }
            await self.ws.send(json.dumps(msg))
            
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get('status') == 'success':
                candles = data.get('data', [])
                df = pd.DataFrame(candles)
                df.columns = ['open', 'high', 'low', 'close', 'volume']
                return df
            else:
                logger.error(f"Failed to get candles for {asset}: {data}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error getting candles for {asset}: {e}")
            return pd.DataFrame()
    
    async def place_order(self, asset: str, amount: float, direction: str, duration: int) -> Dict:
        """Place a trade order"""
        try:
            if not self.is_connected:
                await self.connect()
            
            msg = {
                "name": "place_order",
                "msg": {
                    "asset": asset,
                    "amount": amount,
                    "direction": direction,
                    "duration": duration,
                    "is_demo": self.is_demo
                }
            }
            await self.ws.send(json.dumps(msg))
            
            response = await self.ws.recv()
            data = json.loads(response)
            
            if data.get('status') == 'success':
                logger.info(f"Order placed successfully: {data}")
                return data.get('data', {})
            else:
                logger.error(f"Failed to place order: {data}")
                return {}
                
        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return {}
    
    async def subscribe_candles(self, asset: str, timeframe: int, callback):
        """Subscribe to real-time candle updates"""
        try:
            if not self.is_connected:
                await self.connect()
            
            msg = {
                "name": "subscribe_candles",
                "msg": {
                    "asset": asset,
                    "timeframe": timeframe
                }
            }
            await self.ws.send(json.dumps(msg))
            
            # Listen for updates
            while True:
                response = await self.ws.recv()
                data = json.loads(response)
                
                if data.get('name') == 'candle_update':
                    await callback(data.get('data', {}))
                    
        except Exception as e:
            logger.error(f"Error subscribing to candles: {e}")
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        if self.ws:
            await self.ws.close()
            self.is_connected = False
            logger.info("Disconnected from Pocket Option")
