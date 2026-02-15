"""
データベース接続管理
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import os
from typing import Generator

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://stock_user:stock_pass@localhost:5432/stock_prediction"
)

# TimescaleDB用のエンジン設定
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 接続確認
    connect_args={
        "connect_timeout": 10,
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator[Session, None, None]:
    """データベースセッションを取得"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """データベースを初期化"""
    from .models import Base
    Base.metadata.create_all(bind=engine)


def setup_timescale():
    """TimescaleDB用の設定を実施"""
    with engine.begin() as connection:
        # TimescaleDB拡張を有効化
        connection.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
        
        # stock_prices テーブルをハイパーテーブルに変換
        try:
            connection.execute("""
                SELECT create_hypertable('stock_prices', 'date',
                    if_not_exists => TRUE);
            """)
        except Exception as e:
            print(f"Hypertable creation note: {e}")
        
        # インデックスを作成
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol_date
            ON stock_prices (symbol, date DESC)
            WHERE date > now() - interval '1 year';
        """)
