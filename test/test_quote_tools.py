import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from datetime import datetime
from src.vnstock_mcp.tools.quote_tools import (
    get_quote_history_price,
    get_quote_intraday_price,
    get_quote_price_depth,
    get_quote_price_with_indicators,
    _get_available_indicators_detailed,
    _list_available_indicators
)


class TestQuoteTools:
    """Test suite for quote-related tools"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    @patch('src.vnstock_mcp.tools.quote_tools.datetime')
    def test_get_quote_history_price_json(self, mock_datetime, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with JSON output"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_history_price('VCB', '2024-01-01', None, '1D', output_format='json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.history.assert_called_once_with(
            start='2024-01-01',
            end='2024-01-31',
            interval='1D'
        )
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['time'] == '2024-01-01'
        assert parsed_result[0]['close'] == 103.0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_history_price_with_end_date(self, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with specific end date"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1H', output_format='dataframe')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.history.assert_called_once_with(
            start='2024-01-01',
            end='2024-01-31',
            interval='1H'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['time'] == '2024-01-01'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_history_price_toon(self, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with TOON output (default)"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        # Test - default output_format is 'toon'
        result = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1D')
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_history_price_different_intervals(self, mock_quote_class, sample_quote_history_data):
        """Test get_quote_history_price with different intervals"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = sample_quote_history_data
        mock_quote_class.return_value = mock_instance
        
        intervals = ['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M']
        
        for interval in intervals:
            result = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', interval, output_format='json')
            mock_instance.history.assert_called_with(
                start='2024-01-01',
                end='2024-01-31',
                interval=interval
            )

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
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
        result = get_quote_intraday_price('VCB', 500, 1, output_format='json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.intraday.assert_called_once_with(page_size=500, page=1)
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['time'] == '09:00:00'
        assert parsed_result[0]['price'] == 100.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_intraday_price_with_last_time(self, mock_quote_class):
        """Test get_quote_intraday_price with last_time parameter"""
        # Setup mock
        intraday_data = pd.DataFrame([{'time': '09:15:00', 'price': 101.0}])
        
        mock_instance = Mock()
        mock_instance.intraday.return_value = intraday_data
        mock_quote_class.return_value = mock_instance
        
        # Test
        result = get_quote_intraday_price('VCB', 100, 2, output_format='dataframe')
        
        # Assertions
        mock_instance.intraday.assert_called_once_with(page_size=100, page=2)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['time'] == '09:15:00'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
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
        result = get_quote_price_depth('VCB', output_format='json')
        
        # Assertions
        mock_quote_class.assert_called_once_with(symbol='VCB', source='VCI')
        mock_instance.price_depth.assert_called_once()
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['bid_price_1'] == 100.0
        assert parsed_result[0]['ask_price_1'] == 100.5

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
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
        result = get_quote_price_depth('VCB', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['bid_price_1'] == 100.0

    @pytest.mark.unit
    def test_quote_tools_default_parameters(self):
        """Test quote tools with default parameters"""
        with patch('src.vnstock_mcp.tools.quote_tools.Quote') as mock_quote_class, \
             patch('src.vnstock_mcp.tools.quote_tools.datetime') as mock_datetime:
            
            mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
            mock_instance = Mock()
            mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01', 'close': 100}])
            mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00', 'price': 100}])
            mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
            mock_quote_class.return_value = mock_instance
            
            # Test default interval (should be '1D') and output_format (should be 'toon')
            result = get_quote_history_price('VCB', '2024-01-01')
            mock_instance.history.assert_called_with(
                start='2024-01-01',
                end='2024-01-31',
                interval='1D'
            )
            assert isinstance(result, str)  # TOON string
            
            # Test default page_size (should be 100) and output_format (should be 'toon')
            result = get_quote_intraday_price('VCB')
            mock_instance.intraday.assert_called_with(page_size=100, page=1)
            assert isinstance(result, str)  # TOON string
            
            # Test default output_format (should be 'toon')
            result = get_quote_price_depth('VCB')
            assert isinstance(result, str)  # TOON string

    @pytest.mark.unit
    def test_quote_tools_error_handling(self):
        """Test error handling in quote tools"""
        with patch('src.vnstock_mcp.tools.quote_tools.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.history.side_effect = Exception("Invalid symbol")
            mock_quote_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                get_quote_history_price('INVALID', '2024-01-01', '2024-01-31', '1D', output_format='json')

    @pytest.mark.unit
    def test_quote_tools_empty_results(self):
        """Test quote tools with empty results"""
        with patch('src.vnstock_mcp.tools.quote_tools.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.intraday.return_value = pd.DataFrame()
            mock_quote_class.return_value = mock_instance
            
            result = get_quote_intraday_price('VCB', 100, 1, output_format='json')
            assert result == '[]'
            
            result = get_quote_intraday_price('VCB', 100, 1, output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
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
        get_quote_history_price(symbol, '2024-01-01', '2024-01-31', '1D', output_format='dataframe')
        get_quote_intraday_price(symbol, 100, None, output_format='dataframe')
        get_quote_price_depth(symbol, output_format='dataframe')
        
        # All should initialize Quote with same symbol and source='VCI'
        assert mock_quote_class.call_count == 3
        for call in mock_quote_class.call_args_list:
            assert call[1]['symbol'] == symbol
            assert call[1]['source'] == 'VCI'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_quote_history_price_page_size_parameter(self, mock_quote_class):
        """Test that get_quote_intraday_price handles different page sizes correctly"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
        mock_quote_class.return_value = mock_instance
        
        # Test different page sizes
        page_sizes = [50, 100, 500, 1000]
        for page_size in page_sizes:
            result = get_quote_intraday_price('VCB', page_size, 1, output_format='json')
            mock_instance.intraday.assert_called_with(page_size=page_size, page=1)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    @patch('src.vnstock_mcp.tools.quote_tools.datetime')
    def test_quote_history_end_date_handling(self, mock_datetime, mock_quote_class):
        """Test end_date handling in get_quote_history_price"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01'}])
        mock_quote_class.return_value = mock_instance
        
        # Test with None end_date (should use current date)
        result = get_quote_history_price('VCB', '2024-01-01', None, '1D', output_format='json')
        mock_datetime.now.assert_called_once()
        mock_instance.history.assert_called_with(
            start='2024-01-01',
            end='2024-01-31',
            interval='1D'
        )
        
        # Reset mocks
        mock_datetime.reset_mock()
        mock_instance.reset_mock()
        
        # Test with specific end_date (should not call datetime.now)
        result = get_quote_history_price('VCB', '2024-01-01', '2024-01-15', '1D', output_format='json')
        mock_datetime.now.assert_not_called()
        mock_instance.history.assert_called_with(
            start='2024-01-01',
            end='2024-01-15',
            interval='1D'
        )

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
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
            get_quote_history_price(symbol, '2024-01-01', '2024-01-31', '1D', output_format='json')
            get_quote_intraday_price(symbol, 100, 1, output_format='json')
            get_quote_price_depth(symbol, output_format='json')
            
            # Verify Quote class was initialized with correct symbol
            calls = mock_quote_class.call_args_list[-3:]  # Last 3 calls
            for call in calls:
                assert call[1]['symbol'] == symbol

    @pytest.mark.unit
    def test_quote_intraday_last_time_parameter_handling(self):
        """Test last_time parameter handling in get_quote_intraday_price"""
        with patch('src.vnstock_mcp.tools.quote_tools.Quote') as mock_quote_class:
            mock_instance = Mock()
            mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00'}])
            mock_quote_class.return_value = mock_instance
            
            # Test with None last_time
            result = get_quote_intraday_price('VCB', 100, 1, output_format='json')
            mock_instance.intraday.assert_called_with(page_size=100, page=1)
            
            # Reset mock
            mock_instance.reset_mock()
            
            # Test with specific last_time
            result = get_quote_intraday_price('VCB', 100, 2, output_format='json')
            mock_instance.intraday.assert_called_with(page_size=100, page=2)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_quote_tools_output_format_consistency(self, mock_quote_class):
        """Test output format consistency across all quote tools"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.history.return_value = pd.DataFrame([{'time': '2024-01-01', 'close': 100}])
        mock_instance.intraday.return_value = pd.DataFrame([{'time': '09:00:00', 'price': 100}])
        mock_instance.price_depth.return_value = pd.DataFrame([{'bid_price': 100}])
        mock_quote_class.return_value = mock_instance
        
        # Test JSON format
        history_json = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1D', output_format='json')
        intraday_json = get_quote_intraday_price('VCB', 100, 1, output_format='json')
        depth_json = get_quote_price_depth('VCB', output_format='json')
        
        assert isinstance(history_json, str)
        assert isinstance(intraday_json, str)
        assert isinstance(depth_json, str)
        
        # Test DataFrame format
        history_df = get_quote_history_price('VCB', '2024-01-01', '2024-01-31', '1D', output_format='dataframe')
        intraday_df = get_quote_intraday_price('VCB', 100, 1, output_format='dataframe')
        depth_df = get_quote_price_depth('VCB', output_format='dataframe')
        
        assert isinstance(history_df, pd.DataFrame)
        assert isinstance(intraday_df, pd.DataFrame)
        assert isinstance(depth_df, pd.DataFrame)


class TestQuotePriceWithIndicators:
    """Test suite for get_quote_price_with_indicators"""
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    @patch('src.vnstock_mcp.tools.quote_tools.datetime')
    def test_get_quote_price_with_indicators_single(self, mock_datetime, mock_quote_class):
        """Test get_quote_price_with_indicators with single indicator"""
        import numpy as np
        
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-31'
        
        # Create OHLCV data that works with pandas_ta
        np.random.seed(42)
        n = 50
        close = 100 + np.cumsum(np.random.randn(n) * 2)
        ohlcv_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=n),
            'open': close + np.random.randn(n),
            'high': close + np.abs(np.random.randn(n)),
            'low': close - np.abs(np.random.randn(n)),
            'close': close,
            'volume': np.random.randint(100000, 1000000, n).astype(float)
        })
        
        mock_instance = Mock()
        mock_instance.history.return_value = ohlcv_data
        mock_quote_class.return_value = mock_instance
        
        # Test with RSI
        result = get_quote_price_with_indicators(
            'VCB', ['rsi'], '2024-01-01', None, '1D', 
            output_format='dataframe'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert 'RSI' in result.columns
        mock_quote_class.assert_called_with(symbol='VCB', source='VCI')
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_price_with_indicators_multiple(self, mock_quote_class):
        """Test get_quote_price_with_indicators with multiple indicators"""
        import numpy as np
        
        # Create OHLCV data
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.randn(n) * 2)
        ohlcv_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=n),
            'open': close + np.random.randn(n),
            'high': close + np.abs(np.random.randn(n)),
            'low': close - np.abs(np.random.randn(n)),
            'close': close,
            'volume': np.random.randint(100000, 1000000, n).astype(float)
        })
        
        mock_instance = Mock()
        mock_instance.history.return_value = ohlcv_data
        mock_quote_class.return_value = mock_instance
        
        # Test with multiple indicators
        result = get_quote_price_with_indicators(
            'VCB', ['rsi', 'macd'], '2024-01-01', '2024-03-31', '1D',
            output_format='dataframe'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert 'RSI' in result.columns
        assert 'MACD' in result.columns
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_price_with_indicators_with_params(self, mock_quote_class):
        """Test get_quote_price_with_indicators with indicator parameters"""
        import numpy as np
        
        # Create OHLCV data
        np.random.seed(42)
        n = 100
        close = 100 + np.cumsum(np.random.randn(n) * 2)
        ohlcv_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=n),
            'open': close + np.random.randn(n),
            'high': close + np.abs(np.random.randn(n)),
            'low': close - np.abs(np.random.randn(n)),
            'close': close,
            'volume': np.random.randint(100000, 1000000, n).astype(float)
        })
        
        mock_instance = Mock()
        mock_instance.history.return_value = ohlcv_data
        mock_quote_class.return_value = mock_instance
        
        # Test with indicator with custom parameters
        result = get_quote_price_with_indicators(
            'VCB', ['rsi(window=21)'], '2024-01-01', '2024-03-31', '1D',
            output_format='dataframe'
        )
        
        assert isinstance(result, pd.DataFrame)
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.quote_tools.Quote')
    def test_get_quote_price_with_indicators_json_output(self, mock_quote_class):
        """Test get_quote_price_with_indicators with JSON output"""
        import numpy as np
        
        # Create OHLCV data
        np.random.seed(42)
        n = 50
        close = 100 + np.cumsum(np.random.randn(n) * 2)
        ohlcv_data = pd.DataFrame({
            'time': pd.date_range('2024-01-01', periods=n),
            'open': close + np.random.randn(n),
            'high': close + np.abs(np.random.randn(n)),
            'low': close - np.abs(np.random.randn(n)),
            'close': close,
            'volume': np.random.randint(100000, 1000000, n).astype(float)
        })
        
        mock_instance = Mock()
        mock_instance.history.return_value = ohlcv_data
        mock_quote_class.return_value = mock_instance
        
        result = get_quote_price_with_indicators(
            'VCB', ['rsi'], '2024-01-01', '2024-02-01', '1D',
            output_format='json'
        )
        
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert isinstance(parsed, list)


class TestIndicatorHelpers:
    """Test suite for indicator helper functions"""
    
    @pytest.mark.unit
    def test_get_available_indicators_detailed(self):
        """Test _get_available_indicators_detailed function"""
        result = _get_available_indicators_detailed()
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        # Each indicator should have detailed info
        for ind in result:
            assert isinstance(ind, dict)
            assert 'name' in ind
            assert 'description' in ind
            assert 'parameters' in ind
    
    @pytest.mark.unit
    def test_list_available_indicators(self):
        """Test _list_available_indicators function"""
        result = _list_available_indicators()
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert 'rsi' in result
        assert 'macd' in result
