"""
XGBoostベースの予測モデル
"""
import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import pickle
import logging
from typing import Tuple, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class XGBoostStockPredictor:
    """XGBoostを使用した株価予測モデル"""
    
    def __init__(self, model_version: str = "1.0"):
        self.model = None
        self.scaler = StandardScaler()
        self.model_version = model_version
        self.feature_names = []
        self.feature_importance = {}
        
    def prepare_features(self, df: pd.DataFrame, lookback: int = 90) -> Tuple[np.ndarray, np.ndarray]:
        """
        特徴量を準備
        
        Args:
            df: 価格とマクロ指標を含むデータフレーム
            lookback: 過去N日を使用
            
        Returns:
            X: 特徴量行列
            y: ターゲット値
        """
        features = []
        
        # テクニカル指標を計算
        df['sma_20'] = df['close_price'].rolling(20).mean()
        df['sma_50'] = df['close_price'].rolling(50).mean()
        df['sma_200'] = df['close_price'].rolling(200).mean()
        
        # ボラティリティ
        df['volatility'] = df['close_price'].pct_change().rolling(20).std()
        
        # RSI計算
        delta = df['close_price'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['close_price'].ewm(span=12, adjust=False).mean()
        exp2 = df['close_price'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        
        # ラグ特徴量
        for lag in [1, 5, 20]:
            df[f'price_lag_{lag}'] = df['close_price'].shift(lag)
            df[f'return_lag_{lag}'] = df['close_price'].pct_change(lag)
        
        # ボリューム特徴量
        df['volume_sma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma']
        
        self.feature_names = [col for col in df.columns 
                             if col not in ['close_price', 'date', 'symbol']]
        
        # NaNを削除
        df = df.dropna()
        
        # 特徴量とターゲット
        X = df[self.feature_names].values
        y = df['close_price'].values
        
        # 正規化
        X = self.scaler.fit_transform(X)
        
        return X, y
    
    def train(self, X: np.ndarray, y: np.ndarray, 
              test_size: float = 0.2, **xgb_params) -> Dict[str, float]:
        """
        モデルを学習
        
        Args:
            X: 特徴量行列
            y: ターゲット値
            test_size: テストセットの割合
            **xgb_params: XGBoostハイパーパラメータ
            
        Returns:
            評価メトリクス
        """
        # デフォルトハイパーパラメータ
        default_params = {
            'objective': 'reg:squarederror',
            'max_depth': 8,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
        }
        default_params.update(xgb_params)
        
        # 時系列スプリット
        tscv = TimeSeriesSplit(n_splits=5)
        scores = []
        
        for train_idx, test_idx in tscv.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # モデル学習
            self.model = xgb.XGBRegressor(**default_params, n_estimators=1000)
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_test, y_test)],
                early_stopping_rounds=50,
                verbose=False
            )
            
            # 評価
            y_pred = self.model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mape = mean_absolute_percentage_error(y_test, y_pred)
            scores.append({'rmse': rmse, 'mape': mape})
        
        # 最終モデル（全データで学習）
        self.model = xgb.XGBRegressor(**default_params, n_estimators=1000)
        self.model.fit(X, y)
        
        # 特徴量重要度
        self.feature_importance = dict(zip(
            self.feature_names,
            self.model.feature_importances_
        ))
        
        avg_rmse = np.mean([s['rmse'] for s in scores])
        avg_mape = np.mean([s['mape'] for s in scores])
        
        metrics = {
            'rmse': avg_rmse,
            'mape': avg_mape,
            'model_version': self.model_version,
        }
        
        logger.info(f"Model trained: RMSE={avg_rmse:.2f}, MAPE={avg_mape:.4f}")
        
        return metrics
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        予測を実施
        """
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def save_model(self, path: str):
        """モデルを保存"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'feature_importance': self.feature_importance,
                'model_version': self.model_version,
            }, f)
        logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """モデルを読み込む"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data['feature_names']
            self.feature_importance = data['feature_importance']
            self.model_version = data['model_version']
        logger.info(f"Model loaded from {path}")
