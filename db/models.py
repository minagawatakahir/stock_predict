"""
SQLAlchemy モデル定義
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class StockPrice(Base):
    """株価データ（時系列）"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float, nullable=False)
    volume = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_symbol_date', 'symbol', 'date'),
    )


class MacroIndicator(Base):
    """マクロ経済指標"""
    __tablename__ = "macro_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(100), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(50))
    source = Column(String(100))  # e-Stat, BOJ, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_indicator_date', 'indicator_name', 'date'),
    )


class PolicyData(Base):
    """国策・政策データ"""
    __tablename__ = "policy_data"
    
    id = Column(Integer, primary_key=True, index=True)
    policy_type = Column(String(100), nullable=False, index=True)
    announcement_date = Column(DateTime, nullable=False, index=True)
    effective_date = Column(DateTime)
    policy_score = Column(Float)  # 0-100
    description = Column(Text)
    budget_amount = Column(Float)  # 予算額
    affected_sectors = Column(String(500))  # JSON形式で保存
    impact_on_sector = Column(String(50))  # positive, negative, neutral
    source = Column(String(200))  # データソース
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_policy_date', 'policy_type', 'announcement_date'),
    )


class Prediction(Base):
    """予測結果"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    prediction_date = Column(DateTime, nullable=False, index=True)
    target_date = Column(DateTime, nullable=False)
    current_price = Column(Float, nullable=False)
    predicted_price = Column(Float, nullable=False)
    confidence_score = Column(Float)  # 0-100
    model_version = Column(String(50))
    
    # 各モデルの予測
    lstm_prediction = Column(Float)
    xgboost_prediction = Column(Float)
    transformer_prediction = Column(Float)
    
    # 政策スコア
    policy_score = Column(Float)
    
    # 実績（後で更新）
    actual_price = Column(Float)
    error_percentage = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_symbol_target_date', 'symbol', 'target_date'),
    )


class DataCollectionLog(Base):
    """データ収集ログ"""
    __tablename__ = "data_collection_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    data_source = Column(String(100), nullable=False)  # yfinance, e-Stat, BOJ
    status = Column(String(20))  # success, failed, partial
    records_count = Column(Integer)
    error_message = Column(Text)
    execution_time_seconds = Column(Float)
    executed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_source_date', 'data_source', 'executed_at'),
    )
