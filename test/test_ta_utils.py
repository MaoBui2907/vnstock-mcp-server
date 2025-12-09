"""
Test suite for ta_utils.py - Unified Technical Analysis interface.
This test file verifies the helper functions, registry interface, and add_indicator function.
For specific indicator tests, see:
- test_ta_momentum_utils.py: Momentum indicators
- test_ta_trend_utils.py: Trend indicators
"""

import pytest
import pandas as pd
import numpy as np
from src.vnstock_mcp.libs.ta_utils import (
    # Core utilities
    _strip_numeric_suffix,
    _merge_indicator_result,
    _get_indicator_params,
    _get_indicator_description,
    _get_indicator_output_columns,
    _parse_indicator_string,
    # Public API
    get_indicator_info,
    get_available_indicators,
    add_indicator,
    INDICATOR_REGISTRY,
    # Re-exported indicator functions (for backward compatibility)
    add_relative_strength_index,
    add_moving_average_convergence_divergence,
    add_stochastic,
    add_williams_percent_r,
    add_momentum,
    add_average_directional_movement,
    add_aroon_and_aroon_oscillator,
)


@pytest.fixture
def sample_ohlcv_data():
    """
    Create sample OHLCV data for testing technical indicators.
    Needs sufficient data points for all indicators to compute.
    """
    np.random.seed(42)
    n = 200  # Enough data points for most indicators
    
    # Generate realistic-looking price data
    close = 100 + np.cumsum(np.random.randn(n) * 2)
    high = close + np.abs(np.random.randn(n) * 1.5)
    low = close - np.abs(np.random.randn(n) * 1.5)
    open_ = low + np.random.rand(n) * (high - low)
    volume = np.random.randint(100000, 1000000, n)
    
    df = pd.DataFrame({
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume.astype(float),
    })
    
    return df


class TestHelperFunctions:
    """Test suite for helper functions in ta_utils"""
    
    @pytest.mark.unit
    def test_strip_numeric_suffix(self):
        """Test _strip_numeric_suffix function"""
        # Test with numeric suffix
        assert _strip_numeric_suffix('MACD_12_26_9') == 'MACD'
        assert _strip_numeric_suffix('MACDh_12_26_9') == 'MACDh'
        assert _strip_numeric_suffix('STOCHk_14_3_3') == 'STOCHk'
        assert _strip_numeric_suffix('RSI_14') == 'RSI'
        
        # Test without numeric suffix
        assert _strip_numeric_suffix('SQZ_ON') == 'SQZ_ON'
        assert _strip_numeric_suffix('RSI') == 'RSI'
        assert _strip_numeric_suffix('MACD') == 'MACD'
    
    @pytest.mark.unit
    def test_merge_indicator_result_with_none(self, sample_ohlcv_data):
        """Test _merge_indicator_result when result is None"""
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        result = _merge_indicator_result(data, None)
        
        assert result is data
        assert list(result.columns) == original_cols
    
    @pytest.mark.unit
    def test_merge_indicator_result_with_series(self, sample_ohlcv_data):
        """Test _merge_indicator_result with Series result"""
        data = sample_ohlcv_data.copy()
        series_result = pd.Series([1.0] * len(data), name='RSI_14')
        
        result = _merge_indicator_result(data, series_result)
        
        assert 'RSI' in result.columns
        assert len(result) == len(data)
    
    @pytest.mark.unit
    def test_merge_indicator_result_with_rename_map(self, sample_ohlcv_data):
        """Test _merge_indicator_result with rename_map"""
        data = sample_ohlcv_data.copy()
        df_result = pd.DataFrame({
            'MACD_12_26_9': [1.0] * len(data),
            'MACDh_12_26_9': [0.5] * len(data),
        })
        
        rename_map = {'MACD_12_26_9': 'MY_MACD'}
        result = _merge_indicator_result(data, df_result, rename_map=rename_map)
        
        assert 'MY_MACD' in result.columns
        assert 'MACDh' in result.columns
    
    @pytest.mark.unit
    def test_merge_indicator_result_fillna(self, sample_ohlcv_data):
        """Test _merge_indicator_result fills NaN values"""
        data = sample_ohlcv_data.copy()
        series_with_nan = pd.Series([float('nan'), 1.0, 2.0] + [3.0] * (len(data) - 3), name='TEST_14')
        
        result = _merge_indicator_result(data, series_with_nan, fillna_value=0)
        
        assert 'TEST' in result.columns
        assert result['TEST'].iloc[0] == 0  # NaN should be filled with 0


class TestIndicatorRegistry:
    """Test suite for indicator registry functions"""
    
    @pytest.mark.unit
    def test_get_indicator_params(self):
        """Test _get_indicator_params function"""
        params = _get_indicator_params(add_relative_strength_index)
        
        assert isinstance(params, list)
        assert len(params) == 2  # window and scalar
        
        param_names = [p['name'] for p in params]
        assert 'window' in param_names
        assert 'scalar' in param_names
        
        # Check default values exist
        for param in params:
            assert 'default' in param
    
    @pytest.mark.unit
    def test_get_indicator_description(self):
        """Test _get_indicator_description function"""
        description = _get_indicator_description(add_relative_strength_index)
        
        assert isinstance(description, str)
        assert len(description) > 0
        assert 'relative strength index' in description.lower()
    
    @pytest.mark.unit
    def test_get_indicator_description_no_docstring(self):
        """Test _get_indicator_description with function without docstring"""
        def no_doc_func(data):
            pass
        
        description = _get_indicator_description(no_doc_func)
        assert description == ""
    
    @pytest.mark.unit
    def test_get_indicator_output_columns(self):
        """Test _get_indicator_output_columns function"""
        # Single column indicator
        rsi_cols = _get_indicator_output_columns(add_relative_strength_index)
        assert 'RSI' in rsi_cols
        
        # Multi-column indicator
        macd_cols = _get_indicator_output_columns(add_moving_average_convergence_divergence)
        assert 'MACD' in macd_cols
    
    @pytest.mark.unit
    def test_get_indicator_output_columns_no_docstring(self):
        """Test _get_indicator_output_columns with function without docstring"""
        def no_doc_func(data):
            pass
        
        cols = _get_indicator_output_columns(no_doc_func)
        assert cols == []
    
    @pytest.mark.unit
    def test_get_indicator_info(self):
        """Test get_indicator_info function"""
        info = get_indicator_info('rsi')
        
        assert isinstance(info, dict)
        assert 'name' in info
        assert 'description' in info
        assert 'parameters' in info
        assert 'output_columns' in info
        assert 'usage' in info
        
        assert info['name'] == 'rsi'
        assert len(info['parameters']) > 0
    
    @pytest.mark.unit
    def test_get_indicator_info_unknown_indicator(self):
        """Test get_indicator_info with unknown indicator"""
        with pytest.raises(ValueError) as excinfo:
            get_indicator_info('unknown_indicator')
        
        assert 'Unknown indicator' in str(excinfo.value)
    
    @pytest.mark.unit
    def test_get_available_indicators_simple(self):
        """Test get_available_indicators without detailed info"""
        indicators = get_available_indicators(detailed=False)
        
        assert isinstance(indicators, list)
        assert len(indicators) > 0
        assert 'rsi' in indicators
        assert 'macd' in indicators
        # Also check trend indicators are included
        assert 'adx' in indicators
        assert 'aroon' in indicators
    
    @pytest.mark.unit
    def test_get_available_indicators_detailed(self):
        """Test get_available_indicators with detailed info"""
        indicators = get_available_indicators(detailed=True)
        
        assert isinstance(indicators, list)
        assert len(indicators) > 0
        
        # Each indicator should have detailed info
        for ind in indicators:
            assert isinstance(ind, dict)
            assert 'name' in ind
            assert 'description' in ind
            assert 'parameters' in ind
            assert 'output_columns' in ind
            assert 'usage' in ind


class TestParseIndicatorString:
    """Test suite for _parse_indicator_string function"""
    
    @pytest.mark.unit
    def test_parse_simple_indicator(self):
        """Test parsing simple indicator without parameters"""
        name, kwargs = _parse_indicator_string('rsi')
        assert name == 'rsi'
        assert kwargs == {}
        
        name, kwargs = _parse_indicator_string('macd')
        assert name == 'macd'
        assert kwargs == {}
    
    @pytest.mark.unit
    def test_parse_indicator_with_single_param(self):
        """Test parsing indicator with single parameter"""
        name, kwargs = _parse_indicator_string('rsi(window=21)')
        assert name == 'rsi'
        assert kwargs == {'window': 21}
    
    @pytest.mark.unit
    def test_parse_indicator_with_multiple_params(self):
        """Test parsing indicator with multiple parameters"""
        name, kwargs = _parse_indicator_string('macd(fast=12, slow=26, signal=9)')
        assert name == 'macd'
        assert kwargs == {'fast': 12, 'slow': 26, 'signal': 9}
    
    @pytest.mark.unit
    def test_parse_indicator_with_float_params(self):
        """Test parsing indicator with float parameters"""
        name, kwargs = _parse_indicator_string('cci(window=14, scalar=0.015)')
        assert name == 'cci'
        assert kwargs['window'] == 14
        assert kwargs['scalar'] == 0.015
    
    @pytest.mark.unit
    def test_parse_indicator_with_spaces(self):
        """Test parsing indicator with extra spaces"""
        name, kwargs = _parse_indicator_string('  rsi( window = 14 )  ')
        assert name == 'rsi'
        assert kwargs == {'window': 14}


class TestAddIndicator:
    """Test suite for add_indicator function"""
    
    @pytest.mark.unit
    def test_add_indicator_simple(self, sample_ohlcv_data):
        """Test add_indicator with simple indicator name"""
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_with_kwargs(self, sample_ohlcv_data):
        """Test add_indicator with explicit kwargs"""
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi', window=21)
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_with_string_params(self, sample_ohlcv_data):
        """Test add_indicator with parameters in string"""
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi(window=21)')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_kwargs_override_string_params(self, sample_ohlcv_data):
        """Test that explicit kwargs override string parameters"""
        data = sample_ohlcv_data.copy()
        # String has window=21, but explicit kwarg has window=7
        result = add_indicator(data, 'rsi(window=21)', window=7)
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_unknown(self, sample_ohlcv_data):
        """Test add_indicator with unknown indicator"""
        data = sample_ohlcv_data.copy()
        
        with pytest.raises(ValueError) as excinfo:
            add_indicator(data, 'unknown_indicator')
        
        assert 'Unknown indicator' in str(excinfo.value)
    
    @pytest.mark.unit
    def test_add_indicator_case_insensitive(self, sample_ohlcv_data):
        """Test add_indicator is case insensitive"""
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'RSI')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_macd_with_params(self, sample_ohlcv_data):
        """Test add_indicator with MACD and custom parameters"""
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'macd(fast_length=12, slow_length=26, signal_length=9)')
        
        assert 'MACD' in result.columns
        assert 'MACDh' in result.columns
        assert 'MACDs' in result.columns
        
    @pytest.mark.unit
    def test_add_trend_indicator_via_add_indicator(self, sample_ohlcv_data):
        """Test add_indicator with trend indicators"""
        data = sample_ohlcv_data.copy()
        
        # Test ADX
        result = add_indicator(data.copy(), 'adx')
        assert 'ADX' in result.columns
        
        # Test Aroon
        result = add_indicator(data.copy(), 'aroon')
        assert 'AROOND' in result.columns
        assert 'AROONU' in result.columns


class TestCombinedRegistry:
    """Test suite for combined indicator registry"""
    
    @pytest.mark.unit
    def test_registry_contains_momentum_indicators(self):
        """Test that combined registry contains momentum indicators"""
        momentum_indicators = ['rsi', 'macd', 'stochastic', 'cci', 'williams_percent_r']
        for indicator in momentum_indicators:
            assert indicator in INDICATOR_REGISTRY, f"Registry should contain '{indicator}'"
    
    @pytest.mark.unit
    def test_registry_contains_trend_indicators(self):
        """Test that combined registry contains trend indicators"""
        trend_indicators = ['adx', 'aroon', 'psar', 'chop', 'vortex']
        for indicator in trend_indicators:
            assert indicator in INDICATOR_REGISTRY, f"Registry should contain '{indicator}'"
    
    @pytest.mark.unit
    def test_registry_functions_are_callable(self):
        """Test that all registry values are callable"""
        for key, func in INDICATOR_REGISTRY.items():
            assert callable(func), f"Registry value for '{key}' should be callable"


class TestBackwardCompatibility:
    """Test backward compatibility with direct imports"""
    
    @pytest.mark.unit
    def test_momentum_indicators_importable(self, sample_ohlcv_data):
        """Test that momentum indicators can be imported and used directly"""
        data = sample_ohlcv_data.copy()
        
        # Test direct function calls
        result = add_relative_strength_index(data.copy())
        assert 'RSI' in result.columns
        
        result = add_moving_average_convergence_divergence(data.copy())
        assert 'MACD' in result.columns
        
        result = add_stochastic(data.copy())
        assert 'STOCHk' in result.columns
    
    @pytest.mark.unit
    def test_trend_indicators_importable(self, sample_ohlcv_data):
        """Test that trend indicators can be imported and used directly"""
        data = sample_ohlcv_data.copy()
        
        # Test direct function calls
        result = add_average_directional_movement(data.copy())
        assert 'ADX' in result.columns
        
        result = add_aroon_and_aroon_oscillator(data.copy())
        assert 'AROOND' in result.columns


class TestIndicatorDataIntegrity:
    """Test data integrity for indicators via unified interface"""
    
    @pytest.mark.unit
    def test_original_data_preserved(self, sample_ohlcv_data):
        """Test that original OHLCV columns are preserved after adding indicators"""
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        # Add momentum and trend indicators via unified interface
        data = add_indicator(data, 'rsi')
        data = add_indicator(data, 'macd')
        data = add_indicator(data, 'adx')
        
        # Check original columns are preserved
        for col in original_cols:
            assert col in data.columns, f"Original column '{col}' should be preserved"
            
    @pytest.mark.unit
    def test_chaining_multiple_indicators(self, sample_ohlcv_data):
        """Test chaining multiple indicators from different categories"""
        data = sample_ohlcv_data.copy()
        
        # Chain momentum indicators
        data = add_indicator(data, 'rsi')
        data = add_indicator(data, 'macd')
        
        # Chain trend indicators
        data = add_indicator(data, 'adx')
        data = add_indicator(data, 'aroon')
        
        # All indicators should be present
        assert 'RSI' in data.columns
        assert 'MACD' in data.columns
        assert 'ADX' in data.columns
        assert 'AROOND' in data.columns
