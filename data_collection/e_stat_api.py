"""
e-Stat (政府統計ポータル) API クライアント
"""
import requests
from datetime import datetime
import pandas as pd
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class EStatAPI:
    """e-Stat API クライアント"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.e-stat.go.jp/rest/3.0/app/"
        
    def fetch_gdp(self, start_year: Optional[int] = None) -> pd.DataFrame:
        """
        GDP統計を取得
        
        Args:
            start_year: 開始年（デフォルト: 過去5年）
            
        Returns:
            GDP統計データフレーム
        """
        if start_year is None:
            start_year = datetime.now().year - 5
            
        params = {
            "appId": self.api_key,
            "lang": "J",
            "statsDataId": "0003410379",  # GDP統計ID
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
            "sectionHeaderFlg": "1",
        }
        
        try:
            response = requests.get(
                f"{self.base_url}json/getStatsData",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_stats_data(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch GDP data: {e}")
            return pd.DataFrame()
    
    def fetch_cpi(self, months: int = 12) -> pd.DataFrame:
        """
        消費者物価指数（CPI）を取得
        
        Args:
            months: 取得する月数
            
        Returns:
            CPI データフレーム
        """
        params = {
            "appId": self.api_key,
            "lang": "J",
            "statsDataId": "0003426263",  # CPI統計ID
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
        }
        
        try:
            response = requests.get(
                f"{self.base_url}json/getStatsData",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_stats_data(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch CPI data: {e}")
            return pd.DataFrame()
    
    def fetch_unemployment_rate(self) -> pd.DataFrame:
        """
        失業率を取得
        
        Returns:
            失業率データフレーム
        """
        params = {
            "appId": self.api_key,
            "lang": "J",
            "statsDataId": "0003103532",  # 失業率統計ID
            "metaGetFlg": "Y",
            "cntGetFlg": "N",
        }
        
        try:
            response = requests.get(
                f"{self.base_url}json/getStatsData",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            return self._parse_stats_data(data)
            
        except requests.RequestException as e:
            logger.error(f"Failed to fetch unemployment rate: {e}")
            return pd.DataFrame()
    
    def _parse_stats_data(self, response_data: Dict) -> pd.DataFrame:
        """
        e-Stat APIレスポンスをDataFrameに変換
        
        Args:
            response_data: APIレスポンス
            
        Returns:
            パース済みデータフレーム
        """
        try:
            result = response_data.get("GET_STATS_DATA", {}).get("STATISTICAL_DATA", {})
            data_inf = result.get("DATA_INF", {})
            values = data_inf.get("VALUE", [])
            
            if not values:
                logger.warning("No data found in response")
                return pd.DataFrame()
            
            records = []
            for item in values:
                records.append({
                    'date': item.get('@time'),
                    'value': float(item.get('$', 0)),
                    'unit': item.get('@unit', ''),
                })
            
            df = pd.DataFrame(records)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df = df.sort_values('date')
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to parse stats data: {e}")
            return pd.DataFrame()
