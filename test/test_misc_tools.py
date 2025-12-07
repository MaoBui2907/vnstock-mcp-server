import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from datetime import datetime
from src.vnstock_mcp.tools.misc_tools import (
    get_gold_price,
    get_exchange_rate
)


class TestMiscTools:
    """Test suite for miscellaneous tools (gold price and exchange rate)"""

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price')
    def test_get_gold_price_sjc_no_date_json(self, mock_sjc_gold_price, sample_gold_price_data):
        """Test get_gold_price with SJC source, no date, JSON output"""
        # Setup mock
        mock_sjc_gold_price.return_value = sample_gold_price_data
        
        # Test
        result = get_gold_price(None, 'SJC', output_format='json')
        
        # Assertions
        mock_sjc_gold_price.assert_called_once_with()  # No date parameter
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 1
        assert parsed_result[0]['buy_price'] == 75000000

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price')
    def test_get_gold_price_sjc_with_date_json(self, mock_sjc_gold_price, sample_gold_price_data):
        """Test get_gold_price with SJC source, specific date, JSON output"""
        # Setup mock
        mock_sjc_gold_price.return_value = sample_gold_price_data
        
        # Test
        result = get_gold_price('2024-01-01', 'SJC', output_format='json')
        
        # Assertions
        mock_sjc_gold_price.assert_called_once_with(date='2024-01-01')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['date'] == '2024-01-01'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.btmc_goldprice')
    def test_get_gold_price_btmc_no_date_json(self, mock_btmc_goldprice, sample_gold_price_data):
        """Test get_gold_price with BTMC source, no date, JSON output"""
        # Setup mock
        mock_btmc_goldprice.return_value = sample_gold_price_data
        
        # Test
        result = get_gold_price(None, 'BTMC', output_format='json')
        
        # Assertions
        mock_btmc_goldprice.assert_called_once_with()  # No parameters for BTMC
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1
        assert parsed_result[0]['buy_price'] == 75000000

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price')
    def test_get_gold_price_sjc_dataframe(self, mock_sjc_gold_price, sample_gold_price_data):
        """Test get_gold_price with DataFrame output"""
        # Setup mock
        mock_sjc_gold_price.return_value = sample_gold_price_data
        
        # Test
        result = get_gold_price('2024-01-01', 'SJC', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]['buy_price'] == 75000000

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price')
    def test_get_gold_price_toon(self, mock_sjc_gold_price, sample_gold_price_data):
        """Test get_gold_price with TOON output (default)"""
        # Setup mock
        mock_sjc_gold_price.return_value = sample_gold_price_data
        
        # Test - default output_format is 'toon'
        result = get_gold_price(None, 'SJC')
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price')
    def test_get_gold_price_with_date_parameter(self, mock_sjc_gold_price, sample_gold_price_data):
        """Test get_gold_price when date parameter is provided"""
        # Setup mock
        mock_sjc_gold_price.return_value = sample_gold_price_data
        
        # Test
        test_date = '2024-01-15'
        result = get_gold_price(test_date, 'SJC', output_format='json')
        
        # Assertions
        mock_sjc_gold_price.assert_called_once_with(date=test_date)
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 1

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate')
    @patch('src.vnstock_mcp.tools.misc_tools.datetime')
    def test_get_exchange_rate_no_date_json(self, mock_datetime, mock_vcb_exchange_rate, sample_exchange_rate_data):
        """Test get_exchange_rate with no date (uses current date), JSON output"""
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '2024-01-01'
        mock_vcb_exchange_rate.return_value = sample_exchange_rate_data
        
        # Test
        result = get_exchange_rate(None, output_format='json')
        
        # Assertions
        mock_datetime.now.assert_called_once()
        mock_vcb_exchange_rate.assert_called_once_with(date='2024-01-01')
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['currency'] == 'USD'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate')
    def test_get_exchange_rate_with_date_json(self, mock_vcb_exchange_rate, sample_exchange_rate_data):
        """Test get_exchange_rate with specific date, JSON output"""
        # Setup mock
        mock_vcb_exchange_rate.return_value = sample_exchange_rate_data
        
        # Test
        result = get_exchange_rate('2024-01-15', output_format='json')
        
        # Assertions
        mock_vcb_exchange_rate.assert_called_once_with(date='2024-01-15')
        
        parsed_result = json.loads(result)
        assert len(parsed_result) == 2
        assert parsed_result[0]['currency'] == 'USD'
        assert parsed_result[1]['currency'] == 'EUR'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate')
    def test_get_exchange_rate_dataframe(self, mock_vcb_exchange_rate, sample_exchange_rate_data):
        """Test get_exchange_rate with DataFrame output"""
        # Setup mock
        mock_vcb_exchange_rate.return_value = sample_exchange_rate_data
        
        # Test
        result = get_exchange_rate('2024-01-01', output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['currency'] == 'USD'
        assert result.iloc[1]['currency'] == 'EUR'

    @pytest.mark.unit
    def test_get_gold_price_default_parameters(self):
        """Test get_gold_price with default parameters"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc_gold_price:
            mock_sjc_gold_price.return_value = pd.DataFrame([{'price': 75000000}])
            
            # Test default source (should be 'SJC') and output_format (should be 'toon')
            result = get_gold_price()
            mock_sjc_gold_price.assert_called_with()  # No date
            assert isinstance(result, str)  # TOON string

    @pytest.mark.unit
    def test_get_exchange_rate_default_parameters(self):
        """Test get_exchange_rate with default parameters"""
        with patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate') as mock_vcb_exchange_rate, \
             patch('src.vnstock_mcp.tools.misc_tools.datetime') as mock_datetime:
            
            mock_datetime.now.return_value.strftime.return_value = '2024-01-01'
            mock_vcb_exchange_rate.return_value = pd.DataFrame([{'currency': 'USD'}])
            
            # Test default date (should use current date) and output_format (should be 'toon')
            result = get_exchange_rate()
            mock_datetime.now.assert_called_once()
            mock_vcb_exchange_rate.assert_called_with(date='2024-01-01')
            assert isinstance(result, str)  # TOON string

    @pytest.mark.unit
    def test_misc_tools_error_handling(self):
        """Test error handling in misc tools"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc_gold_price:
            mock_sjc_gold_price.side_effect = Exception("API Error")
            
            with pytest.raises(Exception):
                get_gold_price('2024-01-01', 'SJC', output_format='json')

        with patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate') as mock_vcb_exchange_rate:
            mock_vcb_exchange_rate.side_effect = Exception("API Error")
            
            with pytest.raises(Exception):
                get_exchange_rate('2024-01-01', output_format='json')

    @pytest.mark.unit
    def test_misc_tools_empty_results(self):
        """Test misc tools with empty results"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc_gold_price:
            mock_sjc_gold_price.return_value = pd.DataFrame()
            
            result = get_gold_price('2024-01-01', 'SJC', output_format='json')
            assert result == '[]'
            
            result = get_gold_price('2024-01-01', 'SJC', output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    def test_gold_price_source_selection(self):
        """Test gold price source selection logic"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc, \
             patch('src.vnstock_mcp.tools.misc_tools.btmc_goldprice') as mock_btmc:
            
            sample_data = pd.DataFrame([{'price': 75000000}])
            mock_sjc.return_value = sample_data
            mock_btmc.return_value = sample_data
            
            # Test SJC source
            result = get_gold_price(None, 'SJC', output_format='json')
            mock_sjc.assert_called_once()
            mock_btmc.assert_not_called()
            
            # Reset mocks
            mock_sjc.reset_mock()
            mock_btmc.reset_mock()
            
            # Test BTMC source
            result = get_gold_price(None, 'BTMC', output_format='json')
            mock_btmc.assert_called_once()
            mock_sjc.assert_not_called()

    @pytest.mark.unit
    def test_date_format_handling(self):
        """Test date format handling in misc tools"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc, \
             patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate') as mock_vcb:
            
            mock_sjc.return_value = pd.DataFrame([{'price': 75000000}])
            mock_vcb.return_value = pd.DataFrame([{'currency': 'USD'}])
            
            # Test various date formats
            date_formats = ['2024-01-01', '2024-12-31', '2023-06-15']
            
            for date_str in date_formats:
                # Test gold price
                get_gold_price(date_str, 'SJC', output_format='json')
                mock_sjc.assert_called_with(date=date_str)
                
                # Test exchange rate
                get_exchange_rate(date_str, output_format='json')
                mock_vcb.assert_called_with(date=date_str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.misc_tools.datetime')
    def test_current_date_generation(self, mock_datetime):
        """Test current date generation for exchange rate"""
        with patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate') as mock_vcb:
            # Setup mock datetime
            mock_now = Mock()
            mock_now.strftime.return_value = '2024-01-15'
            mock_datetime.now.return_value = mock_now
            
            mock_vcb.return_value = pd.DataFrame([{'currency': 'USD'}])
            
            # Test
            result = get_exchange_rate(None, output_format='json')
            
            # Assertions
            mock_datetime.now.assert_called_once()
            mock_now.strftime.assert_called_once_with('%Y-%m-%d')
            mock_vcb.assert_called_once_with(date='2024-01-15')

    @pytest.mark.unit
    def test_gold_price_with_date_vs_without_date_logic(self):
        """Test the different logic paths for gold price with/without date"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc:
            sample_data = pd.DataFrame([{'price': 75000000}])
            mock_sjc.return_value = sample_data
            
            # Test without date - should call sjc_gold_price()
            get_gold_price(None, 'SJC', output_format='json')
            mock_sjc.assert_called_with()
            
            # Reset mock
            mock_sjc.reset_mock()
            
            # Test with date - should call sjc_gold_price(date='...')
            get_gold_price('2024-01-01', 'SJC', output_format='json')
            mock_sjc.assert_called_with(date='2024-01-01')

    @pytest.mark.unit
    def test_misc_tools_consistency(self):
        """Test consistency between misc tools"""
        with patch('src.vnstock_mcp.tools.misc_tools.sjc_gold_price') as mock_sjc, \
             patch('src.vnstock_mcp.tools.misc_tools.vcb_exchange_rate') as mock_vcb, \
             patch('src.vnstock_mcp.tools.misc_tools.datetime') as mock_datetime:
            
            # Setup mocks
            mock_sjc.return_value = pd.DataFrame([{'price': 75000000}])
            mock_vcb.return_value = pd.DataFrame([{'currency': 'USD'}])
            mock_datetime.now.return_value.strftime.return_value = '2024-01-01'
            
            # Test both tools with same output format
            gold_result = get_gold_price(None, 'SJC', output_format='dataframe')
            exchange_result = get_exchange_rate(None, output_format='dataframe')
            
            # Both should return DataFrames
            assert isinstance(gold_result, pd.DataFrame)
            assert isinstance(exchange_result, pd.DataFrame)
            
            # Test both tools with JSON format
            gold_result_json = get_gold_price(None, 'SJC', output_format='json')
            exchange_result_json = get_exchange_rate(None, output_format='json')
            
            # Both should return JSON strings
            assert isinstance(gold_result_json, str)
            assert isinstance(exchange_result_json, str)
