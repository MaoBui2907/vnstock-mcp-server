"""
Test suite for vnstock_utils.py
"""

import pytest
import pandas as pd
from unittest.mock import patch, Mock, MagicMock


class TestGetAllSymbolsWithGroups:
    """Test suite for get_all_symbols_with_groups function"""
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.libs.vnstock_utils.vci')
    @patch('src.vnstock_mcp.libs.vnstock_utils._GROUP_CODE', ['VN30', 'VN100', 'HOSE'])
    def test_get_all_symbols_with_groups_success(self, mock_vci):
        """Test successful retrieval of symbols with groups"""
        from src.vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups
        
        # Setup mock
        mock_listing = Mock()
        mock_listing.symbols_by_group.side_effect = [
            ['VCB', 'VIC', 'VNM'],  # VN30
            ['VCB', 'VIC', 'VNM', 'HPG', 'MSN'],  # VN100
            ['VCB', 'VIC', 'VNM', 'HPG', 'MSN', 'FPT'],  # HOSE
        ]
        mock_vci.listing.Listing.return_value = mock_listing
        
        result = get_all_symbols_with_groups()
        
        assert isinstance(result, pd.DataFrame)
        assert 'symbol' in result.columns
        assert 'group' in result.columns
        assert len(result) > 0
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.libs.vnstock_utils.vci')
    @patch('src.vnstock_mcp.libs.vnstock_utils._GROUP_CODE', ['VN30', 'VN100'])
    def test_get_all_symbols_with_groups_handles_exceptions(self, mock_vci):
        """Test that exceptions are handled gracefully"""
        from src.vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups
        
        # Setup mock - first group succeeds, second raises exception
        mock_listing = Mock()
        mock_listing.symbols_by_group.side_effect = [
            ['VCB', 'VIC'],  # VN30 succeeds
            Exception("API Error"),  # VN100 fails
        ]
        mock_vci.listing.Listing.return_value = mock_listing
        
        # Should not raise, just skip the failed group
        result = get_all_symbols_with_groups()
        
        assert isinstance(result, pd.DataFrame)
        # Should only have data from VN30
        assert len(result) == 2
        assert all(result['group'] == 'VN30')
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.libs.vnstock_utils.vci')
    @patch('src.vnstock_mcp.libs.vnstock_utils._GROUP_CODE', ['VN30'])
    def test_get_all_symbols_with_groups_column_order(self, mock_vci):
        """Test that result has correct column order [symbol, group]"""
        from src.vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups
        
        mock_listing = Mock()
        mock_listing.symbols_by_group.return_value = ['VCB', 'VIC']
        mock_vci.listing.Listing.return_value = mock_listing
        
        result = get_all_symbols_with_groups()
        
        assert list(result.columns) == ['symbol', 'group']
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.libs.vnstock_utils.vci')
    @patch('src.vnstock_mcp.libs.vnstock_utils._GROUP_CODE', [])
    def test_get_all_symbols_with_groups_empty_groups(self, mock_vci):
        """Test with empty group list - raises KeyError due to empty DataFrame"""
        from src.vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups
        
        mock_listing = Mock()
        mock_vci.listing.Listing.return_value = mock_listing
        
        # Empty group list causes empty DataFrame which raises KeyError 
        # when trying to select columns ['symbol', 'group']
        with pytest.raises(KeyError):
            get_all_symbols_with_groups()
    
    @pytest.mark.unit
    @patch('src.vnstock_mcp.libs.vnstock_utils.vci')
    @patch('src.vnstock_mcp.libs.vnstock_utils._GROUP_CODE', ['VN30', 'VN100'])
    def test_get_all_symbols_with_groups_all_fail(self, mock_vci):
        """Test when all groups fail - raises KeyError due to empty DataFrame"""
        from src.vnstock_mcp.libs.vnstock_utils import get_all_symbols_with_groups
        
        mock_listing = Mock()
        mock_listing.symbols_by_group.side_effect = Exception("API Error")
        mock_vci.listing.Listing.return_value = mock_listing
        
        # All groups failing causes empty DataFrame which raises KeyError
        with pytest.raises(KeyError):
            get_all_symbols_with_groups()

