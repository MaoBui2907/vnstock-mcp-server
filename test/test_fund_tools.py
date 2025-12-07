import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from src.vnstock_mcp.tools.fund_tools import (
    list_all_funds,
    search_fund,
    get_fund_nav_report,
    get_fund_top_holding,
    get_fund_industry_holding,
    get_fund_asset_holding
)


class TestFundTools:
    """Test suite for fund-related tools"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_list_all_funds_json(self, mock_fund_class, sample_fund_data):
        """Test list_all_funds with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.listing.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = list_all_funds('STOCK', output_format='json')
        
        # Assertions
        mock_fund_class.assert_called_once()
        mock_instance.listing.assert_called_once_with(fund_type='STOCK')
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['symbol'] == 'VFMVN30'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_list_all_funds_dataframe(self, mock_fund_class, sample_fund_data):
        """Test list_all_funds with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.listing.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = list_all_funds('BALANCED', output_format='dataframe')
        
        # Assertions
        mock_instance.listing.assert_called_once_with(fund_type='BALANCED')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['symbol'] == 'VFMVN30'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_list_all_funds_toon(self, mock_fund_class, sample_fund_data):
        """Test list_all_funds with TOON output (default)"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.listing.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test - default output_format is 'toon'
        result = list_all_funds('STOCK')
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_list_all_funds_all_types(self, mock_fund_class, sample_fund_data):
        """Test list_all_funds with None fund_type (all types)"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.listing.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = list_all_funds(None, output_format='json')
        
        # Assertions
        mock_instance.listing.assert_called_once_with(fund_type=None)
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_search_fund_json(self, mock_fund_class, sample_fund_data):
        """Test search_fund with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.filter.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = search_fund('VFM', output_format='json')
        
        # Assertions
        mock_fund_class.assert_called_once()
        mock_instance.filter.assert_called_once_with(symbol='VFM')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert 'VFM' in parsed_result[0]['symbol']

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_search_fund_dataframe(self, mock_fund_class, sample_fund_data):
        """Test search_fund with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.filter.return_value = sample_fund_data
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = search_fund('Dragon', output_format='dataframe')
        
        # Assertions
        mock_instance.filter.assert_called_once_with(symbol='Dragon')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_nav_report_json(self, mock_fund_class):
        """Test get_fund_nav_report with JSON output"""
        # Setup mock
        nav_data = pd.DataFrame([
            {
                'date': '2024-01-01',
                'nav': 25.5,
                'total_assets': 5000000000,
                'outstanding_shares': 196078431
            },
            {
                'date': '2024-01-02',
                'nav': 25.7,
                'total_assets': 5040000000,
                'outstanding_shares': 196078431
            }
        ])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.nav_report.return_value = nav_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_nav_report('VFMVN30', output_format='json')
        
        # Assertions
        mock_fund_class.assert_called_once()
        details_mock.nav_report.assert_called_once_with(symbol='VFMVN30')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['nav'] == 25.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_nav_report_dataframe(self, mock_fund_class):
        """Test get_fund_nav_report with DataFrame output"""
        # Setup mock
        nav_data = pd.DataFrame([{'date': '2024-01-01', 'nav': 25.5}])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.nav_report.return_value = nav_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_nav_report('VFMVN30', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['nav'] == 25.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_top_holding_json(self, mock_fund_class):
        """Test get_fund_top_holding with JSON output"""
        # Setup mock
        holding_data = pd.DataFrame([
            {
                'symbol': 'VCB',
                'company_name': 'Vietcombank',
                'percentage': 10.5,
                'market_value': 525000000
            },
            {
                'symbol': 'VIC',
                'company_name': 'Vingroup',
                'percentage': 8.2,
                'market_value': 410000000
            }
        ])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.top_holding.return_value = holding_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_top_holding('VFMVN30', output_format='json')
        
        # Assertions
        mock_fund_class.assert_called_once()
        details_mock.top_holding.assert_called_once_with(symbol='VFMVN30')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_top_holding_dataframe(self, mock_fund_class):
        """Test get_fund_top_holding with DataFrame output"""
        # Setup mock
        holding_data = pd.DataFrame([{'symbol': 'VCB', 'percentage': 10.5}])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.top_holding.return_value = holding_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_top_holding('VFMVN30', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_industry_holding_json(self, mock_fund_class):
        """Test get_fund_industry_holding with JSON output"""
        # Setup mock
        industry_data = pd.DataFrame([
            {
                'industry': 'Banking',
                'percentage': 25.0,
                'market_value': 1250000000
            },
            {
                'industry': 'Real Estate',
                'percentage': 15.5,
                'market_value': 775000000
            }
        ])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.industry_holding.return_value = industry_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_industry_holding('VFMVN30', output_format='json')
        
        # Assertions
        details_mock.industry_holding.assert_called_once_with(symbol='VFMVN30')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['industry'] == 'Banking'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_get_fund_asset_holding_json(self, mock_fund_class):
        """Test get_fund_asset_holding with JSON output"""
        # Setup mock
        asset_data = pd.DataFrame([
            {
                'asset_type': 'Stock',
                'percentage': 80.0,
                'market_value': 4000000000
            },
            {
                'asset_type': 'Bond',
                'percentage': 15.0,
                'market_value': 750000000
            },
            {
                'asset_type': 'Cash',
                'percentage': 5.0,
                'market_value': 250000000
            }
        ])
        
        mock_instance = Mock()
        details_mock = Mock()
        details_mock.asset_holding.return_value = asset_data
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        # Test
        result = get_fund_asset_holding('VFMVN30', output_format='json')
        
        # Assertions
        details_mock.asset_holding.assert_called_once_with(symbol='VFMVN30')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 3
        assert parsed_result[0]['asset_type'] == 'Stock'

    @pytest.mark.unit
    def test_fund_tools_default_parameters(self):
        """Test fund tools with default parameters"""
        with patch('src.vnstock_mcp.tools.fund_tools.FMarketFund') as mock_fund_class:
            mock_instance = Mock()
            mock_instance.listing.return_value = pd.DataFrame([{'symbol': 'TEST'}])
            mock_fund_class.return_value = mock_instance
            
            # Test default fund_type (should be None) and output_format (should be 'toon')
            result = list_all_funds()
            mock_instance.listing.assert_called_with(fund_type=None)
            assert isinstance(result, str)  # TOON string

    @pytest.mark.unit
    def test_fund_tools_with_different_fund_types(self):
        """Test list_all_funds with different fund types"""
        with patch('src.vnstock_mcp.tools.fund_tools.FMarketFund') as mock_fund_class:
            mock_instance = Mock()
            mock_instance.listing.return_value = pd.DataFrame([{'symbol': 'TEST'}])
            mock_fund_class.return_value = mock_instance
            
            # Test different fund types
            fund_types = ['STOCK', 'BOND', 'BALANCED']
            for fund_type in fund_types:
                result = list_all_funds(fund_type, output_format='json')
                mock_instance.listing.assert_called_with(fund_type=fund_type)

    @pytest.mark.unit
    def test_fund_tools_error_handling(self):
        """Test error handling in fund tools"""
        with patch('src.vnstock_mcp.tools.fund_tools.FMarketFund') as mock_fund_class:
            mock_instance = Mock()
            mock_instance.listing.side_effect = Exception("API Error")
            mock_fund_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                list_all_funds('STOCK', output_format='json')

    @pytest.mark.unit
    def test_fund_tools_empty_results(self):
        """Test fund tools with empty results"""
        with patch('src.vnstock_mcp.tools.fund_tools.FMarketFund') as mock_fund_class:
            mock_instance = Mock()
            mock_instance.filter.return_value = pd.DataFrame()
            mock_fund_class.return_value = mock_instance
            
            result = search_fund('NONEXISTENT', output_format='json')
            assert result == '[]'
            
            result = search_fund('NONEXISTENT', output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.fund_tools.FMarketFund')
    def test_fund_details_methods_consistency(self, mock_fund_class):
        """Test that all fund detail methods work consistently"""
        # Setup mock
        mock_instance = Mock()
        details_mock = Mock()
        
        # Mock all detail methods
        details_mock.nav_report.return_value = pd.DataFrame([{'nav': 25.5}])
        details_mock.top_holding.return_value = pd.DataFrame([{'symbol': 'VCB'}])
        details_mock.industry_holding.return_value = pd.DataFrame([{'industry': 'Banking'}])
        details_mock.asset_holding.return_value = pd.DataFrame([{'asset_type': 'Stock'}])
        
        mock_instance.details = details_mock
        mock_fund_class.return_value = mock_instance
        
        symbol = 'VFMVN30'
        
        # Test all detail methods
        nav_result = get_fund_nav_report(symbol, output_format='dataframe')
        holding_result = get_fund_top_holding(symbol, output_format='dataframe')
        industry_result = get_fund_industry_holding(symbol, output_format='dataframe')
        asset_result = get_fund_asset_holding(symbol, output_format='dataframe')
        
        # All should be DataFrames
        assert isinstance(nav_result, pd.DataFrame)
        assert isinstance(holding_result, pd.DataFrame)
        assert isinstance(industry_result, pd.DataFrame)
        assert isinstance(asset_result, pd.DataFrame)
        
        # All should have called with same symbol
        details_mock.nav_report.assert_called_with(symbol=symbol)
        details_mock.top_holding.assert_called_with(symbol=symbol)
        details_mock.industry_holding.assert_called_with(symbol=symbol)
        details_mock.asset_holding.assert_called_with(symbol=symbol)

    @pytest.mark.unit
    def test_search_fund_keyword_handling(self):
        """Test search_fund with different keyword patterns"""
        with patch('src.vnstock_mcp.tools.fund_tools.FMarketFund') as mock_fund_class:
            mock_instance = Mock()
            mock_instance.filter.return_value = pd.DataFrame([{'symbol': 'FOUND'}])
            mock_fund_class.return_value = mock_instance
            
            # Test with different keywords
            keywords = ['VFM', 'dragon', 'DCDS', 'ETF']
            for keyword in keywords:
                result = search_fund(keyword, output_format='json')
                mock_instance.filter.assert_called_with(symbol=keyword)
                
                parsed_result = json.loads(result)
                assert len(parsed_result) == 1
