import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, TradeRecord

@pytest.fixture(scope="module")
def test_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_trade_record_creation(test_session):
    trade = TradeRecord(symbol="EURUSD", direction="BUY", quantity=1.0, fill_price=1.1000)
    test_session.add(trade)
    test_session.commit()
    
    retrieved = test_session.query(TradeRecord).filter_by(symbol="EURUSD").first()
    assert retrieved is not None
    assert retrieved.direction == "BUY"
    assert retrieved.fill_price == 1.1000
