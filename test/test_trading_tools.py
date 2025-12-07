import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from src.vnstock_mcp.tools.trading_tools import get_price_board


class TestTradingTools:
    """Test suite for trading-related tools"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_json(self, mock_trading_class):
        """Test get_price_board with JSON output"""
        # Setup mock
        price_board_data = pd.DataFrame([
            {
                'symbol': 'VCB',
                'price': 100000,
                'change': 1000,
                'change_percent': 1.01,
                'volume': 1000000,
                'value': 100000000000,
                'open': 99000,
                'high': 101000,
                'low': 98500,
                'avg_price': 99750
            },
            {
                'symbol': 'VIC',
                'price': 85000,
                'change': -500,
                'change_percent': -0.58,
                'volume': 800000,
                'value': 68000000000,
                'open': 85500,
                'high': 86000,
                'low': 84000,
                'avg_price': 85250
            }
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        symbols = ['VCB', 'VIC']
        result = get_price_board(symbols, output_format='json')
        
        # Assertions
        mock_trading_class.assert_called_once()
        mock_instance.price_board.assert_called_once_with(symbols_list=symbols)
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['symbol'] == 'VCB'
        assert parsed_result[0]['price'] == 100000
        assert parsed_result[1]['symbol'] == 'VIC'
        assert parsed_result[1]['price'] == 85000

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_dataframe(self, mock_trading_class):
        """Test get_price_board with DataFrame output"""
        # Setup mock
        price_board_data = pd.DataFrame([
            {
                'symbol': 'VCB',
                'price': 100000,
                'volume': 1000000,
                'change_percent': 1.01
            },
            {
                'symbol': 'HPG',
                'price': 45000,
                'volume': 2000000,
                'change_percent': -0.5
            }
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        symbols = ['VCB', 'HPG']
        result = get_price_board(symbols, output_format='dataframe')
        
        # Assertions
        mock_trading_class.assert_called_once()
        mock_instance.price_board.assert_called_once_with(symbols_list=symbols)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['symbol'] == 'VCB'
        assert result.iloc[0]['price'] == 100000
        assert result.iloc[1]['symbol'] == 'HPG'
        assert result.iloc[1]['price'] == 45000

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_toon(self, mock_trading_class):
        """Test get_price_board with TOON output (default)"""
        # Setup mock
        price_board_data = pd.DataFrame([{'symbol': 'VCB', 'price': 100000}])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test - default output_format is 'toon'
        result = get_price_board(['VCB'])
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_single_symbol(self, mock_trading_class):
        """Test get_price_board with single symbol"""
        # Setup mock
        price_board_data = pd.DataFrame([{
            'symbol': 'VNM',
            'price': 75000,
            'change': 500,
            'volume': 500000
        }])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        symbols = ['VNM']
        result = get_price_board(symbols, output_format='json')
        
        # Assertions
        mock_instance.price_board.assert_called_once_with(symbols_list=symbols)
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['symbol'] == 'VNM'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_multiple_symbols(self, mock_trading_class):
        """Test get_price_board with multiple symbols"""
        # Setup mock
        price_board_data = pd.DataFrame([
            {'symbol': 'VCB', 'price': 100000},
            {'symbol': 'VIC', 'price': 85000},
            {'symbol': 'VNM', 'price': 75000},
            {'symbol': 'HPG', 'price': 45000},
            {'symbol': 'MSN', 'price': 120000}
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        symbols = ['VCB', 'VIC', 'VNM', 'HPG', 'MSN']
        result = get_price_board(symbols, output_format='dataframe')
        
        # Assertions
        mock_instance.price_board.assert_called_once_with(symbols_list=symbols)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 5
        
        # Verify all symbols are present
        result_symbols = result['symbol'].tolist()
        for symbol in symbols:
            assert symbol in result_symbols

    @pytest.mark.unit
    def test_get_price_board_default_parameters(self):
        """Test get_price_board with default parameters"""
        with patch('src.vnstock_mcp.tools.trading_tools.VCITrading') as mock_trading_class:
            mock_instance = Mock()
            mock_instance.price_board.return_value = pd.DataFrame([{'symbol': 'VCB', 'price': 100000}])
            mock_trading_class.return_value = mock_instance
            
            # Test default output_format (should be 'toon')
            result = get_price_board(['VCB'])
            assert isinstance(result, str)  # TOON string

    @pytest.mark.unit
    def test_get_price_board_error_handling(self):
        """Test error handling in get_price_board"""
        with patch('src.vnstock_mcp.tools.trading_tools.VCITrading') as mock_trading_class:
            mock_instance = Mock()
            mock_instance.price_board.side_effect = Exception("API Error")
            mock_trading_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                get_price_board(['VCB'], output_format='json')

    @pytest.mark.unit
    def test_get_price_board_empty_symbols_list(self):
        """Test get_price_board with empty symbols list"""
        with patch('src.vnstock_mcp.tools.trading_tools.VCITrading') as mock_trading_class:
            mock_instance = Mock()
            mock_instance.price_board.return_value = pd.DataFrame()
            mock_trading_class.return_value = mock_instance
            
            result = get_price_board([], output_format='json')
            mock_instance.price_board.assert_called_once_with(symbols_list=[])
            assert result == '[]'
            
            result = get_price_board([], output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    def test_get_price_board_invalid_symbols(self):
        """Test get_price_board with invalid symbols"""
        with patch('src.vnstock_mcp.tools.trading_tools.VCITrading') as mock_trading_class:
            mock_instance = Mock()
            # Return empty DataFrame for invalid symbols
            mock_instance.price_board.return_value = pd.DataFrame()
            mock_trading_class.return_value = mock_instance
            
            result = get_price_board(['INVALID1', 'INVALID2'], output_format='json')
            assert result == '[]'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_mixed_valid_invalid_symbols(self, mock_trading_class):
        """Test get_price_board with mix of valid and invalid symbols"""
        # Setup mock to return data only for valid symbols
        price_board_data = pd.DataFrame([{
            'symbol': 'VCB',
            'price': 100000,
            'error': None
        }])
        # Invalid symbols might not appear in result or have error field
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_board_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        symbols = ['VCB', 'INVALID']
        result = get_price_board(symbols, output_format='json')
        
        # Assertions
        mock_instance.price_board.assert_called_once_with(symbols_list=symbols)
        
        parsed_result = json.loads(result)
        # Only valid symbols should be in result
        assert len(parsed_result) == 1
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_vci_trading_initialization(self, mock_trading_class):
        """Test VCITrading class initialization"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.price_board.return_value = pd.DataFrame([{'symbol': 'VCB'}])
        mock_trading_class.return_value = mock_instance
        
        # Test
        result = get_price_board(['VCB'], output_format='json')
        
        # Assertions
        mock_trading_class.assert_called_once_with()  # No parameters expected

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_comprehensive_data_structure(self, mock_trading_class):
        """Test get_price_board with comprehensive price board data structure"""
        # Setup mock with realistic price board data
        comprehensive_data = pd.DataFrame([
            {
                'symbol': 'VCB',
                'price': 100000,
                'change': 1000,
                'change_percent': 1.01,
                'volume': 1000000,
                'value': 100000000000,
                'open': 99000,
                'high': 101000,
                'low': 98500,
                'avg_price': 99750,
                'ceiling_price': 108900,
                'floor_price': 89100,
                'total_room': 1000000000,
                'current_room': 500000000,
                'bid_price': 99500,
                'bid_volume': 10000,
                'ask_price': 100500,
                'ask_volume': 8000
            }
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = comprehensive_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        result = get_price_board(['VCB'], output_format='json')
        
        # Assertions
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        
        data = parsed_result[0]
        assert data['symbol'] == 'VCB'
        assert data['price'] == 100000
        assert data['change'] == 1000
        assert data['change_percent'] == 1.01
        assert data['volume'] == 1000000
        assert data['ceiling_price'] == 108900
        assert data['floor_price'] == 89100

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_output_format_consistency(self, mock_trading_class):
        """Test output format consistency in get_price_board"""
        # Setup mock
        price_data = pd.DataFrame([
            {'symbol': 'VCB', 'price': 100000},
            {'symbol': 'VIC', 'price': 85000}
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = price_data
        mock_trading_class.return_value = mock_instance
        
        symbols = ['VCB', 'VIC']
        
        # Test JSON format
        json_result = get_price_board(symbols, output_format='json')
        assert isinstance(json_result, str)
        parsed_json = json.loads(json_result)
        assert len(parsed_json) == 2
        
        # Test DataFrame format
        df_result = get_price_board(symbols, output_format='dataframe')
        assert isinstance(df_result, pd.DataFrame)
        assert len(df_result) == 2
        
        # Verify data consistency between formats
        assert parsed_json[0]['symbol'] == df_result.iloc[0]['symbol']
        assert parsed_json[1]['symbol'] == df_result.iloc[1]['symbol']

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_large_symbols_list(self, mock_trading_class):
        """Test get_price_board with large list of symbols"""
        # Setup mock
        large_symbol_list = [f'SYM{i:03d}' for i in range(100)]  # 100 symbols
        large_data = pd.DataFrame([
            {'symbol': symbol, 'price': 50000 + i * 100}
            for i, symbol in enumerate(large_symbol_list)
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = large_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        result = get_price_board(large_symbol_list, output_format='dataframe')
        
        # Assertions
        mock_instance.price_board.assert_called_once_with(symbols_list=large_symbol_list)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 100
        
        # Verify first and last symbols
        assert result.iloc[0]['symbol'] == 'SYM000'
        assert result.iloc[-1]['symbol'] == 'SYM099'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.trading_tools.VCITrading')
    def test_get_price_board_common_vn_symbols(self, mock_trading_class):
        """Test get_price_board with common Vietnamese stock symbols"""
        # Setup mock
        vn_symbols = ['VCB', 'VIC', 'VNM', 'HPG', 'MSN', 'VRE', 'GAS', 'CTG', 'BID', 'TCB']
        vn_data = pd.DataFrame([
            {'symbol': symbol, 'price': 50000 + hash(symbol) % 100000, 'volume': 1000000}
            for symbol in vn_symbols
        ])
        
        mock_instance = Mock()
        mock_instance.price_board.return_value = vn_data
        mock_trading_class.return_value = mock_instance
        
        # Test
        result = get_price_board(vn_symbols, output_format='json')
        
        # Assertions
        parsed_result = json.loads(result)
        assert len(parsed_result) == len(vn_symbols)
        
        result_symbols = [item['symbol'] for item in parsed_result]
        for symbol in vn_symbols:
            assert symbol in result_symbols
