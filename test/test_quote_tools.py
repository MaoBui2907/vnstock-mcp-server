import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from datetime import datetime
from src.vnstock_mcp.server import (
    get_quote_history_price,
    get_quote_intraday_price,
    get_quote_price_depth
)


class TestQuoteTools:
    """Test suite for quote-related tools"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    @patch('src.vnstock_mcp.server.datetime')
    def test_get_quote_history_price_json(self, mock_datetime, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with JSON output"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_history_price('VCB', '2024-01-01', None, '1D', 'json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.history.assert_called_once_with(
            start_date='2024-01-01',
            end_date='2024-01-31',
            interval='1D'
        )
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['time'] == '2024-01-01'
        assert parsed_result[0]['close'] == 103.0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_history_price_with_end_date(self, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with specific end date"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1H', 'dataframe')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.history.assert_called_once_with(
            start_date='2024-01-01',
            end_date='2024-01-31',
            interval='1H'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['time'] == '2024-01-01'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_history_price_different_intervals(self, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with different intervals"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        intervals = ['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M']
        
        for interval in intervals:
            result = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', interval, 'json')
            mock_instance.history.assert_called_with(
                start_date='2024-01-01',
                end_date='2024-01-31',
                interval=interval
            )

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_intraday_price_json(self, mock_quote_class):
        """Test get_quote_intraday_price with JSON output"""
        # Setup mock
        intraday_data = pd.DataFrame([
            {
                'time': '09:00:00',
                'price': 100.5,
                'volume': 10000,
                'accumulated_volume': 10000
            },
            {
                'time': '09:15:00',
                'price': 101.0,
                'volume': 15000,
                'accumulated_volume': 25000
            }
        ])
        
        mock_instance = Mock()
        mock_instance.intraday.return_value = intraday_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_intraday_price('VCB', 500, None, 'json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.intraday.assert_called_once_with(page_size=500, last_time=None)
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['time'] == '09:00:00'
        assert parsed_result[0]['price'] == 100.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_intraday_price_with_last_time(self, mock_quote_class):
        """Test get_quote_intraday_price with last_time parameter"""
        # Setup mock
        intraday_data = pd.DataFrame([{'time': '09:15:00', 'price': 101.0}])
        
        mock_instance = Mock()
        mock_instance.intraday.return_value = intraday_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_intraday_price('VCB', 100, '09:00:00', 'dataframe')
        
        # Assertions
        mock_instance.intraday.assert_called_once_with(page_size=100, last_time='09:00:00')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['time'] == '09:15:00'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_price_depth_json(self, mock_quote_class):
        """Test get_quote_price_depth with JSON output"""
        # Setup mock
        depth_data = pd.DataFrame([
            {
                'bid_price_1': 100.0,
                'bid_volume_1': 1000,
                'ask_price_1': 100.5,
                'ask_volume_1': 800,
                'bid_price_2': 99.5,
                'bid_volume_2': 1200,
                'ask_price_2': 101.0,
                'ask_volume_2': 900
            }
        ])
        
        mock_instance = Mock()
        mock_instance.price_depth.return_value = depth_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_price_depth('VCB', 'json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.price_depth.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['bid_price_1'] == 100.0
        assert parsed_result[0]['ask_price_1'] == 100.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_get_quote_price_depth_dataframe(self, mock_quote_class):
        """Test get_quote_price_depth with DataFrame output"""
        # Setup mock
        depth_data = pd.DataFrame([{
            'bid_price_1': 100.0,
            'ask_price_1': 100.5
        }])
        
        mock_instance = Mock()
        mock_instance.price_depth.return_value = depth_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_price_depth('VCB', 'dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['bid_price_1'] == 100.0

    @pytest.mark.unit
    def test_quote_tools_default_parameters(self):
        """Test quote tools with default parameters"""
        with patch('src.vnstock_mcp.server.Quote') as mock_quote_class, \
             patch('src.vnstock_mcp.server.datetime') as mock_datetime:
            
            mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
            mock_instance = Mock()
            mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01', 'close': 100}])
            mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00', 'price': 100}])
            mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
            mock_quote_class.return_value = mock_instance
            
            # Test default interval (should be '1D') and output_format (should be 'json')
            result = get_quote_history_price('VCB', '2024-01-01')
            mock_instance.history.assert_called_with(
                start_date='2024-01-01',
                end_date='2024-01-31',
                interval='1D'
            )
            assert isinstance(result, str)  # JSON string
            
            # Test default page_size (should be 100) and output_format (should be 'json')
            result = get_quote_intraday_price('VCB')
            mock_instance.intraday.assert_called_with(page_size=100, last_time=None)
            assert isinstance(result, str)  # JSON string
            
            # Test default output_format (should be 'json')
            result = get_quote_price_depth('VCB')
            assert isinstance(result, str)  # JSON string

    @pytest.mark.unit
    def test_quote_tools_error_handling(self):
        """Test error handling in quote tools"""
        with patch('src.vnstock_mcp.server.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.history.side_effect = Exception("Invalid symbol")
            mock_quote_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                get_quote_history_price('INVALID', '2024-01-01', '2024-01-31', '1D', 'json')

    @pytest.mark.unit
    def test_quote_tools_empty_results(self):
        """Test quote tools with empty results"""
        with patch('src.vnstock_mcp.server.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.intraday.return_value = pd.DataFrame()
            mock_quote_class.return_value = mock_instance
            
            result = get_quote_intraday_price('VCB', 100, None, 'json')
            assert result == '[]'
            
            result = get_quote_intraday_price('VCB', 100, None, 'dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_quote_class_initialization_consistency(self, mock_quote_class):
        """Test that all quote tools initialize Quote class consistently"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01'}])
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
        mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
        mock_quote_class.return_value = mock_instance
        
        symbol = 'VCB'
        
        # Test all quote tools
        get_quote_history_price(symbol, '2024-01-01', '2024-01-31', '1D', 'dataframe')
        get_quote_intraday_price(symbol, 100, None, 'dataframe')
        get_quote_price_depth(symbol, 'dataframe')
        
        # All should initialize Quote with same symbol and source='VCI'
        assert mock_quote_class.call_count == 3
        for call in mock_quote_class.call_args_list:
            assert call[1]['symbol'] == symbol
            assert call[1]['source'] == 'VCI'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_quote_history_price_page_size_parameter(self, mock_quote_class):
        """Test that get_quote_intraday_price handles different page sizes correctly"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
        mock_quote_class.return_value = mock_instance
        
        # Test different page sizes
        page_sizes = [50, 100, 500, 1000]
        for page_size in page_sizes:
            result = get_quote_intraday_price('VCB', page_size, None, 'json')
            mock_instance.intraday.assert_called_with(page_size=page_size, last_time=None)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    @patch('src.vnstock_mcp.server.datetime')
    def test_quote_history_end_date_handling(self, mock_datetime, mock_quote_class):
        """Test end_date handling in get_quote_history_price"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01'}])
        mock_quote_class.return_value = mock_instance
        
        # Test with None end_date (should use current date)
        result = get_quote_history_price('VCB', '2024-01-01', None, '1D', 'json')
        mock_datetime.now.assert_called_once()
        mock_instance.history.assert_called_with(
            start_date='2024-01-01',
            end_date='2024-01-31',
            interval='1D'
        )
        
        # Reset mocks
        mock_datetime.reset_mock()
        mock_instance.reset_mock()
        
        # Test with specific end_date (should not call datetime.now)
        result = get_quote_history_price('VCB', '2024-01-01', '2024-01-15', '1D', 'json')
        mock_datetime.now.assert_not_called()
        mock_instance.history.assert_called_with(
            start_date='2024-01-01',
            end_date='2024-01-15',
            interval='1D'
        )

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_quote_tools_with_different_symbols(self, mock_quote_class):
        """Test quote tools with different stock symbols"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01'}])
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
        mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
        mock_quote_class.return_value = mock_instance
        
        symbols = ['VCB', 'VIC', 'VNM', 'HPG', 'MSN']
        
        for symbol in symbols:
            # Test each tool with different symbols
            get_quote_history_price(symbol, '2024-01-01', '2024-01-31', '1D', 'json')
            get_quote_intraday_price(symbol, 100, None, 'json')
            get_quote_price_depth(symbol, 'json')
            
            # Verify Quote class was initialized with correct symbol
            calls = mock_quote_class.call_args_list[-3:]  # Last 3 calls
            for call in calls:
                assert call[1]['symbol'] == symbol

    @pytest.mark.unit
    def test_quote_intraday_last_time_parameter_handling(self):
        """Test last_time parameter handling in get_quote_intraday_price"""
        with patch('src.vnstock_mcp.server.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
            mock_quote_class.return_value = mock_instance
            
            # Test with None last_time
            result = get_quote_intraday_price('VCB', 100, None, 'json')
            mock_instance.intraday.assert_called_with(page_size=100, last_time=None)
            
            # Reset mock
            mock_instance.reset_mock()
            
            # Test with specific last_time
            result = get_quote_intraday_price('VCB', 100, '09:00:00', 'json')
            mock_instance.intraday.assert_called_with(page_size=100, last_time='09:00:00')

    @pytest.mark.unit
    @patch('src.vnstock_mcp.server.Quote')
    def test_quote_tools_output_format_consistency(self, mock_quote_class):
        """Test output format consistency across all quote tools"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01', 'close': 100}])
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00', 'price': 100}])
        mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
        mock_quote_class.return_value = mock_instance
        
        # Test JSON format
        history_json = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1D', 'json')
        intraday_json = get_quote_intraday_price('VCB', 100, None, 'json')
        depth_json = get_quote_price_depth('VCB', 'json')
        
        assert isinstance(history_json, str)
        assert isinstance(intraday_json, str)
        assert isinstance(depth_json, str)
        
        # Test DataFrame format
        history_df = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1D', 'dataframe')
        intraday_df = get_quote_intraday_price('VCB', 100, None, 'dataframe')
        depth_df = get_quote_price_depth('VCB', 'dataframe')
        
        assert isinstance(history_df, pd.DataFrame)
        assert isinstance(intraday_df, pd.DataFrame)
        assert isinstance(depth_df, pd.DataFrame)
