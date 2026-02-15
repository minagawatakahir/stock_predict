"""
シンプルな単体テスト（依存関係なし）
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_imports():
    """モジュールのインポートテスト"""
    print("Testing imports...")
    
    try:
        from data_collection.e_stat_api import EStatAPI
        print("✅ e_stat_api module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import e_stat_api: {e}")
        return False
    
    try:
        from data_collection.boj_scraper import BOJScraper
        print("✅ boj_scraper module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import boj_scraper: {e}")
        return False
    
    try:
        from db.models import StockPrice, MacroIndicator, PolicyData
        print("✅ db.models module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import db.models: {e}")
        return False
    
    return True


def test_e_stat_api():
    """e-Stat API クライアントのテスト"""
    print("\nTesting e-Stat API client...")
    
    try:
        from data_collection.e_stat_api import EStatAPI
        
        api = EStatAPI(api_key="test_key_12345")
        assert api.api_key == "test_key_12345", "API key mismatch"
        assert "e-stat.go.jp" in api.base_url, "Base URL incorrect"
        
        print("✅ e-Stat API client initialization passed")
        return True
    except Exception as e:
        print(f"❌ e-Stat API test failed: {e}")
        return False


def test_boj_scraper():
    """日本銀行スクレイパーのテスト"""
    print("\nTesting BOJ Scraper...")
    
    try:
        from data_collection.boj_scraper import BOJScraper
        
        scraper = BOJScraper()
        assert "boj.or.jp" in scraper.base_url, "Base URL incorrect"
        assert 'User-Agent' in scraper.headers, "Headers missing User-Agent"
        
        print("✅ BOJ Scraper initialization passed")
        return True
    except Exception as e:
        print(f"❌ BOJ Scraper test failed: {e}")
        return False


def test_database_models():
    """データベースモデルのテスト"""
    print("\nTesting database models...")
    
    try:
        from db.models import StockPrice, MacroIndicator, PolicyData, Prediction, DataCollectionLog
        
        # クラスが正しく定義されているか確認
        assert hasattr(StockPrice, '__tablename__'), "StockPrice missing __tablename__"
        assert hasattr(MacroIndicator, '__tablename__'), "MacroIndicator missing __tablename__"
        assert hasattr(PolicyData, '__tablename__'), "PolicyData missing __tablename__"
        
        print("✅ Database models passed")
        return True
    except Exception as e:
        print(f"❌ Database models test failed: {e}")
        return False


def test_file_structure():
    """プロジェクト構造のテスト"""
    print("\nTesting project structure...")
    
    project_root = os.path.join(os.path.dirname(__file__), '..')
    
    required_files = [
        'docker-compose.yml',
        'requirements.txt',
        '.env.example',
        'README.md',
        '.gitignore',
    ]
    
    required_dirs = [
        'airflow/dags',
        'api',
        'data_collection',
        'db',
        'ml/models',
    ]
    
    all_passed = True
    
    for file in required_files:
        path = os.path.join(project_root, file)
        if os.path.exists(path):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_passed = False
    
    for directory in required_dirs:
        path = os.path.join(project_root, directory)
        if os.path.isdir(path):
            print(f"✅ {directory}/ exists")
        else:
            print(f"❌ {directory}/ missing")
            all_passed = False
    
    return all_passed


if __name__ == "__main__":
    print("=" * 60)
    print("株価予測アプリ - シンプル単体テスト")
    print("=" * 60)
    
    results = []
    
    results.append(("File Structure", test_file_structure()))
    results.append(("Module Imports", test_imports()))
    results.append(("e-Stat API", test_e_stat_api()))
    results.append(("BOJ Scraper", test_boj_scraper()))
    results.append(("Database Models", test_database_models()))
    
    print("\n" + "=" * 60)
    print("テスト結果サマリー")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<40} {status}")
    
    print(f"\n合計: {passed}/{total} テスト合格")
    
    if passed == total:
        print("\n🎉 全てのテストが成功しました！")
        sys.exit(0)
    else:
        print(f"\n⚠️  {total - passed} 個のテストが失敗しました")
        sys.exit(1)
