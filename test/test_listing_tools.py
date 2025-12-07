import pytest
import pandas as pd
import json
from unittest.mock import patch, Mock
from src.vnstock_mcp.tools.listing_tools import (
    get_all_symbol_groups,
    get_all_industries,
    get_all_symbols_by_group,
    get_all_symbols_by_industry,
    get_all_symbols,
    get_all_symbols_detailed
)


class TestListingTools:
    """Test suite for listing-related tools"""

    @pytest.mark.unit
    def test_get_all_symbol_groups_json(self):
        """Test get_all_symbol_groups with JSON output"""
        result = get_all_symbol_groups(output_format='json')
        
        # Should return hardcoded DataFrame converted to JSON
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) > 0
        
        # Check for expected groups
        group_names = [item['group'] for item in parsed_result]
        assert 'HOSE' in group_names
        assert 'HNX' in group_names
        assert 'VN30' in group_names
        assert 'ETF' in group_names

    @pytest.mark.unit
    def test_get_all_symbol_groups_dataframe(self):
        """Test get_all_symbol_groups with DataFrame output"""
        result = get_all_symbol_groups(output_format='dataframe')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert 'group' in result.columns
        assert 'group_name' in result.columns
        
        # Check for expected groups
        assert 'HOSE' in result['group'].values
        assert 'VN30' in result['group'].values

    @pytest.mark.unit
    def test_get_all_symbol_groups_toon(self):
        """Test get_all_symbol_groups with TOON output (default)"""
        result = get_all_symbol_groups()
        
        # TOON format returns a string
        assert isinstance(result, str)

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_industries_json(self, mock_vci_listing_class, sample_industries_data):
        """Test get_all_industries with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.industries_icb.return_value = sample_industries_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_industries(output_format='json')
        
        # Assertions
        mock_vci_listing_class.assert_called_once()
        mock_instance.industries_icb.assert_called_once()
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['icb_name1'] == 'Technology'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_industries_dataframe(self, mock_vci_listing_class, sample_industries_data):
        """Test get_all_industries with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.industries_icb.return_value = sample_industries_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_industries(output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['icb_name1'] == 'Technology'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_by_group_json(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols_by_group with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_group.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols_by_group('VN30', output_format='json')
        
        # Assertions
        mock_vci_listing_class.assert_called_once()
        mock_instance.symbols_by_group.assert_called_once_with(group='VN30')
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_by_group_dataframe(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols_by_group with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_group.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols_by_group('HOSE', output_format='dataframe')
        
        # Assertions
        mock_instance.symbols_by_group.assert_called_once_with(group='HOSE')
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_by_industry_with_filter(self, mock_vci_listing_class):
        """Test get_all_symbols_by_industry with industry filter"""
        # Setup mock with extended data for filtering
        extended_symbols_data = pd.DataFrame([
            {
                'symbol': 'VCB',
                'company_name': 'Vietcombank',
                'exchange': 'HOSE',
                'icb_code1': '2000',
                'icb_code2': '2100',
                'icb_code3': '2110',
                'icb_code4': '2111'
            },
            {
                'symbol': 'VIC',
                'company_name': 'Vingroup',
                'exchange': 'HOSE',
                'icb_code1': '1000',
                'icb_code2': '1100',
                'icb_code3': '1110',
                'icb_code4': '1111'
            }
        ])
        
        mock_instance = Mock()
        mock_instance.symbols_by_industries.return_value = extended_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols_by_industry('2000', output_format='json')
        
        # Assertions
        mock_vci_listing_class.assert_called_once()
        mock_instance.symbols_by_industries.assert_called_once()
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        # Should filter to only VCB (icb_code1 == '2000')
        assert len(parsed_result) == 1
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_by_industry_no_filter(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols_by_industry without industry filter"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_industries.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test with None industry (should return all)
        result = get_all_symbols_by_industry(None, output_format='dataframe')
        
        # Assertions
        mock_vci_listing_class.assert_called_once()
        mock_instance.symbols_by_industries.assert_called_once()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_json(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols with JSON output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_exchange.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols(output_format='json')
        
        # Assertions
        mock_vci_listing_class.assert_called_once()
        mock_instance.symbols_by_exchange.assert_called_once()
        
        parsed_result = json.loads(result)
        assert isinstance(parsed_result, list)
        assert len(parsed_result) == 2
        assert parsed_result[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_dataframe(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols with DataFrame output"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_exchange.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols(output_format='dataframe')
        
        # Assertions
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]['symbol'] == 'VCB'

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_detailed(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols_detailed"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_exchange.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test
        result = get_all_symbols_detailed(output_format='dataframe')
        
        # Assertions
        mock_instance.symbols_by_exchange.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    @pytest.mark.unit
    def test_get_all_symbol_groups_contains_all_expected_groups(self):
        """Test that get_all_symbol_groups contains all expected groups"""
        result = get_all_symbol_groups(output_format='dataframe')
        
        expected_groups = [
            'HOSE', 'HNX', 'UPCOM', 'VN30', 'VN100', 'HNX30',
            'VNMidCap', 'VNSmallCap', 'VNAllShare', 'HNXCon',
            'HNXFin', 'HNXLCap', 'HNXMSCap', 'HNXMan', 'ETF',
            'FU_INDEX', 'CW'
        ]
        
        actual_groups = result['group'].tolist()
        
        for expected_group in expected_groups:
            assert expected_group in actual_groups, f"Missing group: {expected_group}"

    @pytest.mark.unit
    def test_symbol_groups_structure(self):
        """Test the structure of symbol groups data"""
        result = get_all_symbol_groups(output_format='dataframe')
        
        # Check columns
        expected_columns = ['group', 'group_name']
        assert list(result.columns) == expected_columns
        
        # Check data types
        assert result['group'].dtype == 'object'
        assert result['group_name'].dtype == 'object'
        
        # Check that all group names contain the group name
        for _, row in result.iterrows():
            assert row['group'] in row['group_name']

    @pytest.mark.unit
    def test_listing_tools_error_handling(self):
        """Test error handling in listing tools"""
        with patch('src.vnstock_mcp.tools.listing_tools.VCIListing') as mock_vci_listing_class:
            mock_instance = Mock()
            mock_instance.industries_icb.side_effect = Exception("API Error")
            mock_vci_listing_class.return_value = mock_instance
            
            with pytest.raises(Exception):
                get_all_industries(output_format='json')

    @pytest.mark.unit
    def test_listing_tools_empty_results(self):
        """Test listing tools with empty results"""
        with patch('src.vnstock_mcp.tools.listing_tools.VCIListing') as mock_vci_listing_class:
            mock_instance = Mock()
            mock_instance.symbols_by_group.return_value = pd.DataFrame()
            mock_vci_listing_class.return_value = mock_instance
            
            result = get_all_symbols_by_group('INVALID_GROUP', output_format='json')
            assert result == '[]'
            
            result = get_all_symbols_by_group('INVALID_GROUP', output_format='dataframe')
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0

    @pytest.mark.unit
    @patch('src.vnstock_mcp.tools.listing_tools.VCIListing')
    def test_get_all_symbols_by_industry_default_parameter(self, mock_vci_listing_class, sample_symbols_data):
        """Test get_all_symbols_by_industry with default parameter"""
        # Setup mock
        mock_instance = Mock()
        mock_instance.symbols_by_industries.return_value = sample_symbols_data
        mock_vci_listing_class.return_value = mock_instance
        
        # Test with default parameter (should be None)
        result = get_all_symbols_by_industry()
        
        # Should return TOON by default
        assert isinstance(result, str)

    @pytest.mark.unit
    def test_listing_tools_default_output_format(self):
        """Test listing tools with default output format"""
        # Test get_all_symbol_groups default (should be 'toon')
        result = get_all_symbol_groups()
        assert isinstance(result, str)  # TOON string
        
        with patch('src.vnstock_mcp.tools.listing_tools.VCIListing') as mock_vci_listing_class:
            mock_instance = Mock()
            mock_instance.industries_icb.return_value = pd.DataFrame([{'test': 'data'}])
            mock_vci_listing_class.return_value = mock_instance
            
            # Test other tools default output format (should be 'toon')
            result = get_all_industries()
            assert isinstance(result, str)  # TOON string
