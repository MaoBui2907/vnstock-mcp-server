import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from src.vnstock_mcp.tools.company_tools import (
    get_company_overview,
    get_company_news,
    get_company_events,
    get_company_shareholders,
    get_company_officers,
    get_company_subsidiaries,
    get_company_reports,
    get_company_dividends,
    get_company_insider_deals,
    get_company_ratio_summary,
    get_company_trading_stats,
    list_all_icb_industries,
    list_all_companies_with_details
)


class TestCompanyTools:
    """Test suite for company-related tools"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_overview_json(self, mock_tcbs_class, sample_company_overview_data):
        """Test get_company_overview with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.overview.return_value = sample_company_overview_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_overview('VCB', output_format='json')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.overview.assert_called_once()
        
        # Verify JSON output
        assert isinstance(result, str)
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 1
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_overview_dataframe(self, mock_tcbs_class, sample_company_overview_data):
        """Test get_company_overview with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.overview.return_value = sample_company_overview_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_overview('VCB', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_overview_toon(self, mock_tcbs_class, sample_company_overview_data):
        """Test get_company_overview with TOON output (default)"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.overview.return_value = sample_company_overview_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test - default output_format is 'toon'
        result = get_company_overview('VCB')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.overview.assert_called_once()
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_news(self, mock_tcbs_class, sample_company_news_data):
        """Test get_company_news"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.news.return_value = sample_company_news_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_news('VCB', page_size=5, page=1, output_format='json')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.news.assert_called_once_with(page_size=5, page=1)
        
        # Verify JSON output
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['title'] == 'VCB announces Q3 results'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_events(self, mock_tcbs_class, sample_company_events_data):
        """Test get_company_events"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.events.return_value = sample_company_events_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_events('VCB', page_size=10, page=0, output_format='dataframe')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.events.assert_called_once_with(page_size=10, page=0)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['event_type'] == 'AGM'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_shareholders(self, mock_tcbs_class, sample_shareholders_data):
        """Test get_company_shareholders"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.shareholders.return_value = sample_shareholders_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_shareholders('VCB', output_format='json')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.shareholders.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['shareholder_name'] == 'State Bank of Vietnam'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_officers_working(self, mock_tcbs_class, sample_officers_data):
        """Test get_company_officers with working filter"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.officers.return_value = sample_officers_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_officers('VCB', 'working', output_format='dataframe')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.officers.assert_called_once_with(filter_by='working')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['name'] == 'John Doe'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_officers_all(self, mock_tcbs_class, sample_officers_data):
        """Test get_company_officers with all filter"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.officers.return_value = sample_officers_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_officers('VCB', 'all', output_format='json')
        
        # Assertions
        mock_instance.officers.assert_called_once_with(filter_by='all')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_subsidiaries(self, mock_tcbs_class, sample_subsidiaries_data):
        """Test get_company_subsidiaries"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.subsidiaries.return_value = sample_subsidiaries_data
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_subsidiaries('VCB', 'subsidiary', output_format='json')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.subsidiaries.assert_called_once_with(filter_by='subsidiary')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['subsidiary_name'] == 'VCB Securities'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.VCICompany')
    def test_get_company_reports(self, mock_vci_class):
        """Test get_company_reports"""
        # Setup mock
        mock_instance = Mock()
        sample_reports = pd.DataFrame([{
            'report_name': 'Annual Report 2023',
            'date': '2024-03-31',
            'type': 'Annual'
        }])
        mock_instance.reports.return_value = sample_reports
        mock_vci_class.return_value = mock_instance
        
        # Test
        result = get_company_reports('VCB', output_format='json')
        
        # Assertions
        mock_vci_class.assert_called_once_with(symbol='VCB')
        mock_instance.reports.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['report_name'] == 'Annual Report 2023'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_dividends(self, mock_tcbs_class):
        """Test get_company_dividends"""
        # Setup mock
        mock_instance = Mock()
        sample_dividends = pd.DataFrame([{
            'year': 2023,
            'dividend_per_share': 1000,
            'payment_date': '2024-05-15'
        }])
        mock_instance.dividends.return_value = sample_dividends
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_dividends('VCB', output_format='dataframe')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.dividends.assert_called_once()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['year'] == 2023

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.TCBSCompany')
    def test_get_company_insider_deals(self, mock_tcbs_class):
        """Test get_company_insider_deals"""
        # Setup mock
        mock_instance = Mock()
        sample_deals = pd.DataFrame([{
            'date': '2024-01-15',
            'insider_name': 'John Doe',
            'transaction_type': 'Buy',
            'volume': 10000
        }])
        mock_instance.insider_deals.return_value = sample_deals
        mock_tcbs_class.return_value = mock_instance
        
        # Test
        result = get_company_insider_deals('VCB', output_format='json')
        
        # Assertions
        mock_tcbs_class.assert_called_once_with(symbol='VCB')
        mock_instance.insider_deals.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['insider_name'] == 'John Doe'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.VCICompany')
    def test_get_company_ratio_summary(self, mock_vci_class):
        """Test get_company_ratio_summary"""
        # Setup mock
        mock_instance = Mock()
        sample_ratios = pd.DataFrame([{
            'pe_ratio': 12.5,
            'pb_ratio': 2.1,
            'roe': 0.18,
            'roa': 0.015
        }])
        mock_instance.ratio_summary.return_value = sample_ratios
        mock_vci_class.return_value = mock_instance
        
        # Test
        result = get_company_ratio_summary('VCB', output_format='dataframe')
        
        # Assertions
        mock_vci_class.assert_called_once_with(symbol='VCB')
        mock_instance.ratio_summary.assert_called_once()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['pe_ratio'] == 12.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.VCICompany')
    def test_get_company_trading_stats(self, mock_vci_class):
        """Test get_company_trading_stats"""
        # Setup mock
        mock_instance = Mock()
        sample_stats = pd.DataFrame([{
            'date': '2024-01-15',
            'volume': 1000000,
            'value': 100000000000,
            'avg_price': 100000
        }])
        mock_instance.trading_stats.return_value = sample_stats
        mock_vci_class.return_value = mock_instance
        
        # Test
        result = get_company_trading_stats('VCB', output_format='json')
        
        # Assertions
        mock_vci_class.assert_called_once_with(symbol='VCB')
        mock_instance.trading_stats.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['volume'] == 1000000

    @pytest.mark.unit
    def test_invalid_symbol_handling(self):
        """Test handling of invalid symbols"""
        with patch('src.vnstock_mcp.tools.company_tools.TCBSCompany') as mock_tcbs_class:
            mock_instance = Mock()
            mock_instance.overview.side_effect = Exception("Invalid symbol")
            mock_tcbs_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                get_company_overview('INVALID', output_format='json')

    @pytest.mark.unit
    def test_default_parameters(self):
        """Test tools with default parameters"""
        with patch('src.vnstock_mcp.tools.company_tools.TCBSCompany') as mock_tcbs_class:
            mock_instance = Mock()
            mock_instance.overview.return_value = pd.DataFrame([{'symbol': 'VCB'}])
            mock_tcbs_class.return_value = mock_instance
            
            # Test default output format (should be 'toon')
            result = get_company_overview('VCB')
            assert isinstance(result, str)  # TOON string
            
            # Test default filter_by for officers
            mock_instance.officers.return_value = pd.DataFrame([{'name': 'Test'}])
            result = get_company_officers('VCB')
            mock_instance.officers.assert_called_with(filter_by='working')

    @pytest.mark.unit
    def test_empty_dataframe_handling(self):
        """Test handling of empty DataFrames"""
        with patch('src.vnstock_mcp.tools.company_tools.TCBSCompany') as mock_tcbs_class:
            mock_instance = Mock()
            mock_instance.overview.return_value = pd.DataFrame()
            mock_tcbs_class.return_value = mock_instance
            
            result = get_company_overview('VCB', output_format='json')
            assert result == '[]'  # Empty JSON array
            
            result = get_company_overview('VCB', output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.VCIListing')
    def test_list_all_icb_industries(self, mock_vci_listing_class):
        """Test list_all_icb_industries"""
        # Setup mock
        mock_instance = Mock()
        sample_icb = pd.DataFrame([{
            'icb_code': '1000',
            'icb_name': 'Technology',
            'en_icb_name': 'Technology',
            'level': 1
        }])
        mock_instance.industries_icb.return_value = sample_icb
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = list_all_icb_industries(output_format='json')
        
        # Assertions
        mock_instance.industries_icb.assert_called_once()
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.company_tools.get_all_symbols_with_groups')
    @patch('src.vnstock_mcp.tools.company_tools.VCIListing')
    def test_list_all_companies_with_details(self, mock_vci_listing_class, mock_get_symbols):
        """Test list_all_companies_with_details"""
        # Setup mocks
        mock_get_symbols.return_value = pd.DataFrame([
            {'symbol': 'VCB', 'group': 'VN30'}
        ])
        
        mock_instance = Mock()
        mock_instance.symbols_by_industries.return_value = pd.DataFrame([{
            'symbol': 'VCB',
            'icb_code1': '1000',
            'icb_code2': '1100',
            'icb_code3': '1110',
            'icb_code4': '1111'
        }])
        mock_instance.symbols_by_exchange.return_value = pd.DataFrame([{
            'symbol': 'VCB',
            'organ_name': 'Vietcombank',
            'exchange': 'HOSE'
        }])
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = list_all_companies_with_details(output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert 'symbol' in result.columns
