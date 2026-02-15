"""
データ収集モジュールの単体テスト
"""
import pytest
from unittest.mock import Mock, patch
import pandas as pd
from datetime import datetime


def test_e_stat_api_initialization():
    """e-Stat APIクライアントの初期化テスト"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from data_collection.e_stat_api import EStatAPI
    
    api = EStatAPI(api_key="test_key")
    assert api.api_key == "test_key"
    assert api.base_url == "https://api.e-stat.go.jp/rest/3.0/app/"


def test_boj_scraper_initialization():
    """日本銀行スクレイパーの初期化テスト"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from data_collection.boj_scraper import BOJScraper
    
    scraper = BOJScraper()
    assert scraper.base_url == "https://www.boj.or.jp/statistics/"
    assert 'User-Agent' in scraper.headers


def test_xgboost_model_initialization():
    """XGBoostモデルの初期化テスト"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from ml.models.xgboost_model import StockPredictionModel
    
    model = StockPredictionModel()
    assert model.model is not None
    assert model.model.get_params()['objective'] == 'reg:squarederror'


def test_mock_prediction():
    """予測機能のモックテスト"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from ml.models.xgboost_model import StockPredictionModel
    
    model = StockPredictionModel()
    
    # サンプルデータ作成
    sample_data = pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 3, 4, 5, 6],
        'feature3': [3, 4, 5, 6, 7],
    })
    
    sample_target = pd.Series([100, 110, 105, 115, 120])
    
    # 学習テスト
    model.train(sample_data, sample_target)
    
    # 予測テスト
    predictions = model.predict(sample_data)
    
    assert len(predictions) == len(sample_data)
    assert all(isinstance(p, (int, float)) for p in predictions)


if __name__ == "__main__":
    print("Running unit tests...")
    
    try:
        test_e_stat_api_initialization()
        print("✅ e-Stat API initialization test passed")
    except Exception as e:
        print(f"❌ e-Stat API test failed: {e}")
    
    try:
        test_boj_scraper_initialization()
        print("✅ BOJ Scraper initialization test passed")
    except Exception as e:
        print(f"❌ BOJ Scraper test failed: {e}")
    
    try:
        test_xgboost_model_initialization()
        print("✅ XGBoost model initialization test passed")
    except Exception as e:
        print(f"❌ XGBoost model test failed: {e}")
    
    try:
        test_mock_prediction()
        print("✅ Mock prediction test passed")
    except Exception as e:
        print(f"❌ Mock prediction test failed: {e}")
    
    print("\nAll tests completed!")
