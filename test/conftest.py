import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock
from datetime import datetime


@pytest.fixture
def sample_company_overview_data():
    """Sample data for company overview"""
    return pd.DataFrame([{
        'symbol': 'VCB',
        'company_name': 'Vietcombank',
        'industry': 'Banking',
        'market_cap': 1000000000000,
        'pe_ratio': 12.5,
        'pb_ratio': 2.1,
        'roe': 0.18,
        'roa': 0.015
    }])


@pytest.fixture
def sample_company_news_data():
    """Sample data for company news"""
    return pd.DataFrame([
        {
            'title': 'VCB announces Q3 results',
            'publish_date': '2024-10-15',
            'content': 'Strong quarterly performance...',
            'source': 'TCBS'
        },
        {
            'title': 'VCB dividend announcement',
            'publish_date': '2024-10-10',
            'content': 'Dividend payment schedule...',
            'source': 'TCBS'
        }
    ])


@pytest.fixture
def sample_company_events_data():
    """Sample data for company events"""
    return pd.DataFrame([
        {
            'event_type': 'AGM',
            'event_date': '2024-04-15',
            'description': 'Annual General Meeting',
            'status': 'Completed'
        },
        {
            'event_type': 'Dividend',
            'event_date': '2024-05-01',
            'description': 'Dividend payment',
            'status': 'Completed'
        }
    ])


@pytest.fixture
def sample_shareholders_data():
    """Sample data for shareholders"""
    return pd.DataFrame([
        {
            'shareholder_name': 'State Bank of Vietnam',
            'ownership_percentage': 75.2,
            'share_quantity': 3760000000
        },
        {
            'shareholder_name': 'Public shareholders',
            'ownership_percentage': 24.8,
            'share_quantity': 1240000000
        }
    ])


@pytest.fixture
def sample_officers_data():
    """Sample data for officers"""
    return pd.DataFrame([
        {
            'name': 'John Doe',
            'position': 'CEO',
            'status': 'working',
            'appointment_date': '2020-01-01'
        },
        {
            'name': 'Jane Smith',
            'position': 'CFO',
            'status': 'working',
            'appointment_date': '2021-06-01'
        }
    ])


@pytest.fixture
def sample_subsidiaries_data():
    """Sample data for subsidiaries"""
    return pd.DataFrame([
        {
            'subsidiary_name': 'VCB Securities',
            'ownership_percentage': 100,
            'business_type': 'subsidiary'
        },
        {
            'subsidiary_name': 'VCB Insurance',
            'ownership_percentage': 51,
            'business_type': 'subsidiary'
        }
    ])


@pytest.fixture
def sample_financial_data():
    """Sample data for financial statements"""
    return pd.DataFrame([
        {
            'period': '2023',
            'revenue': 50000000000,
            'profit_before_tax': 15000000000,
            'net_profit': 12000000000,
            'total_assets': 2000000000000,
            'total_equity': 150000000000
        },
        {
            'period': '2022',
            'revenue': 45000000000,
            'profit_before_tax': 13500000000,
            'net_profit': 10800000000,
            'total_assets': 1800000000000,
            'total_equity': 140000000000
        }
    ])


@pytest.fixture
def sample_fund_data():
    """Sample data for funds"""
    return pd.DataFrame([
        {
            'symbol': 'VFMVN30',
            'fund_name': 'VFM VN30 ETF',
            'fund_type': 'STOCK',
            'nav': 25.5,
            'total_assets': 5000000000
        },
        {
            'symbol': 'DCDS',
            'fund_name': 'Dragon Capital Dividend Fund',
            'fund_type': 'BALANCED',
            'nav': 15.2,
            'total_assets': 2000000000
        }
    ])


@pytest.fixture
def sample_quote_history_data():
    """Sample data for quote history"""
    return pd.DataFrame([
        {
            'time': '2024-01-01',
            'open': 100.0,
            'high': 105.0,
            'low': 98.0,
            'close': 103.0,
            'volume': 1000000
        },
        {
            'time': '2024-01-02',
            'open': 103.0,
            'high': 107.0,
            'low': 101.0,
            'close': 106.0,
            'volume': 1200000
        }
    ])


@pytest.fixture
def sample_gold_price_data():
    """Sample data for gold prices"""
    return pd.DataFrame([
        {
            'date': '2024-01-01',
            'buy_price': 75000000,
            'sell_price': 76000000,
            'type': 'SJC Gold Bar'
        }
    ])


@pytest.fixture
def sample_exchange_rate_data():
    """Sample data for exchange rates"""
    return pd.DataFrame([
        {
            'currency': 'USD',
            'buy_rate': 24000,
            'sell_rate': 24200,
            'date': '2024-01-01'
        },
        {
            'currency': 'EUR',
            'buy_rate': 26000,
            'sell_rate': 26300,
            'date': '2024-01-01'
        }
    ])


@pytest.fixture
def sample_industries_data():
    """Sample data for industries"""
    return pd.DataFrame([
        {
            'icb_code1': '1000',
            'icb_name1': 'Technology',
            'icb_code2': '1100',
            'icb_name2': 'Software'
        },
        {
            'icb_code1': '2000',
            'icb_name1': 'Banking',
            'icb_code2': '2100',
            'icb_name2': 'Commercial Banks'
        }
    ])


@pytest.fixture
def sample_symbols_data():
    """Sample data for symbols listing"""
    return pd.DataFrame([
        {
            'symbol': 'VCB',
            'company_name': 'Vietcombank',
            'exchange': 'HOSE',
            'industry': 'Banking'
        },
        {
            'symbol': 'VIC',
            'company_name': 'Vingroup',
            'exchange': 'HOSE',
            'industry': 'Real Estate'
        }
    ])


@pytest.fixture
def mock_tcbs_company():
    """Mock TCBS Company class"""
    mock = Mock()
    mock.overview.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'company_name': 'Vietcombank'
    }])
    mock.news.return_value = pd.DataFrame([{
        'title': 'Test news',
        'date': '2024-01-01'
    }])
    mock.events.return_value = pd.DataFrame([{
        'event': 'Test event',
        'date': '2024-01-01'
    }])
    mock.shareholders.return_value = pd.DataFrame([{
        'name': 'Test shareholder',
        'percentage': 10.5
    }])
    mock.officers.return_value = pd.DataFrame([{
        'name': 'Test officer',
        'position': 'CEO'
    }])
    mock.subsidiaries.return_value = pd.DataFrame([{
        'name': 'Test subsidiary',
        'percentage': 100
    }])
    mock.dividends.return_value = pd.DataFrame([{
        'year': 2023,
        'dividend': 1000
    }])
    mock.insider_deals.return_value = pd.DataFrame([{
        'date': '2024-01-01',
        'volume': 1000
    }])
    return mock


@pytest.fixture
def mock_vci_company():
    """Mock VCI Company class"""
    mock = Mock()
    mock.reports.return_value = pd.DataFrame([{
        'report_name': 'Test report',
        'date': '2024-01-01'
    }])
    mock.ratio_summary.return_value = pd.DataFrame([{
        'ratio_name': 'PE',
        'value': 12.5
    }])
    mock.trading_stats.return_value = pd.DataFrame([{
        'date': '2024-01-01',
        'volume': 1000000
    }])
    return mock


@pytest.fixture
def mock_vci_listing():
    """Mock VCI Listing class"""
    mock = Mock()
    mock.industries_icb.return_value = pd.DataFrame([{
        'icb_code': '1000',
        'icb_name': 'Technology'
    }])
    mock.symbols_by_group.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'group': 'VN30'
    }])
    mock.symbols_by_industries.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'industry': 'Banking'
    }])
    mock.symbols_by_exchange.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'exchange': 'HOSE'
    }])
    return mock


@pytest.fixture
def mock_vci_finance():
    """Mock VCI Finance class"""
    mock = Mock()
    mock.income_statement.return_value = pd.DataFrame([{
        'period': '2023',
        'revenue': 1000000
    }])
    mock.balance_sheet.return_value = pd.DataFrame([{
        'period': '2023',
        'total_assets': 5000000
    }])
    mock.cash_flow.return_value = pd.DataFrame([{
        'period': '2023',
        'operating_cash_flow': 500000
    }])
    mock.ratio.return_value = pd.DataFrame([{
        'period': '2023',
        'pe_ratio': 12.5
    }])
    mock._get_report.return_value = pd.DataFrame([{
        'period': '2023',
        'raw_data': 'test'
    }])
    return mock


@pytest.fixture
def mock_quote():
    """Mock Quote class"""
    mock = Mock()
    mock.history.return_value = pd.DataFrame([{
        'time': '2024-01-01',
        'close': 100.0
    }])
    mock.intraday.return_value = pd.DataFrame([{
        'time': '09:00:00',
        'price': 100.5
    }])
    mock.price_depth.return_value = pd.DataFrame([{
        'bid_price': 100.0,
        'ask_price': 100.5
    }])
    return mock


@pytest.fixture
def mock_fund():
    """Mock Fund class"""
    mock = Mock()
    mock.listing.return_value = pd.DataFrame([{
        'symbol': 'VFMVN30',
        'fund_name': 'VFM VN30 ETF'
    }])
    mock.filter.return_value = pd.DataFrame([{
        'symbol': 'VFMVN30',
        'fund_name': 'VFM VN30 ETF'
    }])
    
    # Mock details sub-object
    details_mock = Mock()
    details_mock.nav_report.return_value = pd.DataFrame([{
        'date': '2024-01-01',
        'nav': 25.5
    }])
    details_mock.top_holding.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'percentage': 10.5
    }])
    details_mock.industry_holding.return_value = pd.DataFrame([{
        'industry': 'Banking',
        'percentage': 25.0
    }])
    details_mock.asset_holding.return_value = pd.DataFrame([{
        'asset_type': 'Stock',
        'percentage': 80.0
    }])
    mock.details = details_mock
    return mock


@pytest.fixture
def mock_trading():
    """Mock Trading class"""
    mock = Mock()
    mock.price_board.return_value = pd.DataFrame([{
        'symbol': 'VCB',
        'price': 100.0,
        'volume': 1000000
    }])
    return mock


@pytest.fixture
def mock_gold_price_func():
    """Mock gold price functions"""
    return pd.DataFrame([{
        'date': '2024-01-01',
        'buy_price': 75000000,
        'sell_price': 76000000
    }])


@pytest.fixture
def mock_exchange_rate_func():
    """Mock exchange rate function"""
    return pd.DataFrame([{
        'currency': 'USD',
        'buy_rate': 24000,
        'sell_rate': 24200
    }])
