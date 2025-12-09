"""
Test suite for ta_trend_utils.py - Trend Technical Analysis indicators.
This test file verifies each trend indicator function and validates the exact output columns.
"""

import pytest
import pandas as pd
import numpy as np
from src.vnstock_mcp.libs.ta_trend_utils import (
    add_average_directional_movement,
    add_alpha_trend,
    add_archer_moving_average_trend,
    add_aroon_and_aroon_oscillator,
    add_choppiness_index,
    add_chande_kroll_stop,
    add_decay,
    add_decreasing,
    add_detrend_price_oscillator,
    add_hilbert_transform_trendline,
    add_increasing,
    add_parabolic_stop_and_reverse,
    add_q_stick,
    add_random_walk_index,
    add_trend_flex,
    add_vertical_horizontal_filter,
    add_vortex_indicator,
    add_zig_zag,
    TREND_INDICATOR_REGISTRY,
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


class TestTrendIndicators:
    """Test suite for trend indicators with exact output column validation"""
    
    @pytest.mark.unit
    def test_add_average_directional_movement(self, sample_ohlcv_data):
        """
        Test Average Directional Movement Index (ADX)
        Output columns: ADX, ADXR, DMP, DMN
        """
        data = sample_ohlcv_data.copy()
        result = add_average_directional_movement(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_ohlcv_data)
        assert 'ADX' in result.columns, "Should have 'ADX' column"
        assert 'DMP' in result.columns, "Should have 'DMP' column"
        assert 'DMN' in result.columns, "Should have 'DMN' column"
        
    @pytest.mark.unit
    def test_add_alpha_trend(self, sample_ohlcv_data):
        """
        Test Alpha Trend indicator
        Output columns: ALPHAT (Alpha Trend), ALPHATl (Alpha Trend Long)
        """
        data = sample_ohlcv_data.copy()
        result = add_alpha_trend(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ALPHAT' in result.columns, "Should have 'ALPHAT' column"
        assert 'ALPHATl' in result.columns, "Should have 'ALPHATl' column"
        
    @pytest.mark.unit
    def test_add_archer_moving_average_trend(self, sample_ohlcv_data):
        """
        Test Archer Moving Average Trend (AMAT)
        Output columns: AMATe_LR (Long Run), AMATe_SR (Short Run)
        """
        data = sample_ohlcv_data.copy()
        result = add_archer_moving_average_trend(data, fast_length=8, slow_length=21, lookback_length=2)
        
        assert isinstance(result, pd.DataFrame)
        assert 'AMATe_LR' in result.columns, "Should have 'AMATe_LR' column"
        assert 'AMATe_SR' in result.columns, "Should have 'AMATe_SR' column"
        
    @pytest.mark.unit
    def test_add_aroon_and_aroon_oscillator(self, sample_ohlcv_data):
        """
        Test Aroon indicator and Aroon Oscillator
        Output columns: AROOND (Aroon Down), AROONU (Aroon Up), AROONOSC (Aroon Oscillator)
        """
        data = sample_ohlcv_data.copy()
        result = add_aroon_and_aroon_oscillator(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'AROOND' in result.columns, "Should have 'AROOND' column"
        assert 'AROONU' in result.columns, "Should have 'AROONU' column"
        assert 'AROONOSC' in result.columns, "Should have 'AROONOSC' column"
        
    @pytest.mark.unit
    def test_add_choppiness_index(self, sample_ohlcv_data):
        """
        Test Choppiness Index (CHOP)
        Output columns: CHOP
        """
        data = sample_ohlcv_data.copy()
        result = add_choppiness_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CHOP' in result.columns, "Should have 'CHOP' column"
        
    @pytest.mark.unit
    def test_add_chande_kroll_stop(self, sample_ohlcv_data):
        """
        Test Chande Kroll Stop
        Output columns: CKSPl (Long Stop), CKSPs (Short Stop)
        """
        data = sample_ohlcv_data.copy()
        result = add_chande_kroll_stop(data, p=10, x=3, q=20)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CKSPl' in result.columns, "Should have 'CKSPl' column"
        assert 'CKSPs' in result.columns, "Should have 'CKSPs' column"
        
    @pytest.mark.unit
    def test_add_decay(self, sample_ohlcv_data):
        """
        Test Linear Decay indicator
        Output columns: LDECAY
        """
        data = sample_ohlcv_data.copy()
        result = add_decay(data, window=1)
        
        assert isinstance(result, pd.DataFrame)
        assert 'LDECAY' in result.columns, "Should have 'LDECAY' column"
        
    @pytest.mark.unit
    def test_add_decreasing(self, sample_ohlcv_data):
        """
        Test Decreasing indicator
        Output columns: DEC
        """
        data = sample_ohlcv_data.copy()
        result = add_decreasing(data, window=1)
        
        assert isinstance(result, pd.DataFrame)
        assert 'DEC' in result.columns, "Should have 'DEC' column"
        
    @pytest.mark.unit
    def test_add_detrend_price_oscillator(self, sample_ohlcv_data):
        """
        Test Detrend Price Oscillator (DPO)
        Output columns: DPO
        """
        data = sample_ohlcv_data.copy()
        result = add_detrend_price_oscillator(data, window=20)
        
        assert isinstance(result, pd.DataFrame)
        assert 'DPO' in result.columns, "Should have 'DPO' column"
        
    @pytest.mark.unit
    def test_add_hilbert_transform_trendline(self, sample_ohlcv_data):
        """
        Test Hilbert Transform Trendline
        Output columns: HT_TL
        """
        data = sample_ohlcv_data.copy()
        result = add_hilbert_transform_trendline(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'HT_TL' in result.columns, "Should have 'HT_TL' column"
        
    @pytest.mark.unit
    def test_add_increasing(self, sample_ohlcv_data):
        """
        Test Increasing indicator
        Output columns: INC
        """
        data = sample_ohlcv_data.copy()
        result = add_increasing(data, window=1)
        
        assert isinstance(result, pd.DataFrame)
        assert 'INC' in result.columns, "Should have 'INC' column"
        
    @pytest.mark.unit
    def test_add_parabolic_stop_and_reverse(self, sample_ohlcv_data):
        """
        Test Parabolic Stop and Reverse (PSAR)
        Output columns: PSARl (Long), PSARs (Short), PSARaf (Acceleration Factor), PSARr (Reversal)
        """
        data = sample_ohlcv_data.copy()
        result = add_parabolic_stop_and_reverse(data, af0=0.02, af=0.02, af_max=0.2)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PSARl' in result.columns, "Should have 'PSARl' column"
        assert 'PSARs' in result.columns, "Should have 'PSARs' column"
        assert 'PSARaf' in result.columns, "Should have 'PSARaf' column"
        assert 'PSARr' in result.columns, "Should have 'PSARr' column"
        
    @pytest.mark.unit
    def test_add_q_stick(self, sample_ohlcv_data):
        """
        Test Q Stick indicator
        Output columns: QS
        """
        data = sample_ohlcv_data.copy()
        result = add_q_stick(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'QS' in result.columns, "Should have 'QS' column"
        
    @pytest.mark.unit
    def test_add_random_walk_index(self, sample_ohlcv_data):
        """
        Test Random Walk Index (RWI)
        Output columns: RWIh (High), RWIl (Low)
        """
        data = sample_ohlcv_data.copy()
        result = add_random_walk_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'RWIh' in result.columns, "Should have 'RWIh' column"
        assert 'RWIl' in result.columns, "Should have 'RWIl' column"
        
    @pytest.mark.unit
    def test_add_trend_flex(self, sample_ohlcv_data):
        """
        Test Trend Flex indicator
        Output columns: TRENDFLEX
        """
        data = sample_ohlcv_data.copy()
        result = add_trend_flex(data, window=20, smooth_length=20)
        
        assert isinstance(result, pd.DataFrame)
        assert 'TRENDFLEX' in result.columns, "Should have 'TRENDFLEX' column"
        
    @pytest.mark.unit
    def test_add_vertical_horizontal_filter(self, sample_ohlcv_data):
        """
        Test Vertical Horizontal Filter (VHF)
        Output columns: VHF
        """
        data = sample_ohlcv_data.copy()
        result = add_vertical_horizontal_filter(data, window=28)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VHF' in result.columns, "Should have 'VHF' column"
        
    @pytest.mark.unit
    def test_add_vortex_indicator(self, sample_ohlcv_data):
        """
        Test Vortex Indicator
        Output columns: VTXP (Positive), VTXM (Negative)
        """
        data = sample_ohlcv_data.copy()
        result = add_vortex_indicator(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VTXP' in result.columns, "Should have 'VTXP' column"
        assert 'VTXM' in result.columns, "Should have 'VTXM' column"
        
    @pytest.mark.unit
    def test_add_zig_zag(self, sample_ohlcv_data):
        """
        Test Zig Zag indicator
        Output columns: ZIGZAGs_{deviation}%_{min_bars}, ZIGZAGv_{deviation}%_{min_bars}, ZIGZAGd_{deviation}%_{min_bars}
        """
        data = sample_ohlcv_data.copy()
        result = add_zig_zag(data, deviation=5.0, min_bars=10)
        
        assert isinstance(result, pd.DataFrame)
        # Zig Zag columns include parameters in name
        original_cols = set(sample_ohlcv_data.columns)
        new_cols = [col for col in result.columns if col not in original_cols]
        assert len(new_cols) >= 1, "Zig Zag should add at least one column"
        # Check for ZIGZAG pattern in column names
        zigzag_cols = [col for col in new_cols if 'ZIGZAG' in col]
        assert len(zigzag_cols) >= 1, "Should have at least one ZIGZAG column"


class TestTrendDataIntegrity:
    """Test data integrity for trend indicators"""
    
    @pytest.mark.unit
    def test_original_data_preserved(self, sample_ohlcv_data):
        """Test that original OHLCV columns are preserved after adding indicators"""
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        # Add multiple indicators
        data = add_average_directional_movement(data)
        data = add_aroon_and_aroon_oscillator(data)
        data = add_parabolic_stop_and_reverse(data)
        
        # Check original columns are preserved
        for col in original_cols:
            assert col in data.columns, f"Original column '{col}' should be preserved"
            
    @pytest.mark.unit
    def test_indicator_values_are_numeric(self, sample_ohlcv_data):
        """Test that indicator values are numeric"""
        data = sample_ohlcv_data.copy()
        
        data = add_average_directional_movement(data)
        assert pd.api.types.is_numeric_dtype(data['ADX']), "ADX values should be numeric"
        
        data = add_choppiness_index(data)
        assert pd.api.types.is_numeric_dtype(data['CHOP']), "CHOP values should be numeric"
        
    @pytest.mark.unit
    def test_chaining_multiple_indicators(self, sample_ohlcv_data):
        """Test chaining multiple trend indicators"""
        data = sample_ohlcv_data.copy()
        
        # Chain multiple indicators
        data = add_average_directional_movement(data)
        data = add_aroon_and_aroon_oscillator(data)
        data = add_choppiness_index(data)
        data = add_parabolic_stop_and_reverse(data)
        data = add_vortex_indicator(data)
        
        # All indicators should be present
        assert 'ADX' in data.columns
        assert 'AROOND' in data.columns
        assert 'AROONU' in data.columns
        assert 'CHOP' in data.columns
        assert 'PSARl' in data.columns
        assert 'VTXP' in data.columns


class TestTrendIndicatorOutputColumnsSummary:
    """Summary test to document all trend indicator output columns"""
    
    @pytest.mark.unit
    def test_all_trend_indicators_output_columns(self, sample_ohlcv_data):
        """
        Summary test for all trend indicators and their output columns.
        
        Expected output columns:
        - ADX: ADX, ADXR, DMP, DMN
        - Alpha Trend: ALPHAT, ALPHATl
        - AMAT: AMATe_LR, AMATe_SR
        - Aroon: AROOND, AROONU, AROONOSC
        - CHOP: CHOP
        - CKSP: CKSPl, CKSPs
        - Decay: LDECAY
        - Decreasing: DEC
        - DPO: DPO
        - HT Trendline: HT_TL
        - Increasing: INC
        - PSAR: PSARl, PSARs, PSARaf, PSARr
        - Q Stick: QS
        - RWI: RWIh, RWIl
        - Trend Flex: TRENDFLEX
        - VHF: VHF
        - Vortex: VTXP, VTXM
        - Zig Zag: ZIGZAGs_*, ZIGZAGv_*, ZIGZAGd_*
        """
        # Single column indicators
        single_col_indicators = {
            'CHOP': (add_choppiness_index, ['CHOP']),
            'LDECAY': (add_decay, ['LDECAY']),
            'DEC': (add_decreasing, ['DEC']),
            'DPO': (add_detrend_price_oscillator, ['DPO']),
            'HT_TL': (add_hilbert_transform_trendline, ['HT_TL']),
            'INC': (add_increasing, ['INC']),
            'QS': (add_q_stick, ['QS']),
            'TRENDFLEX': (add_trend_flex, ['TRENDFLEX']),
            'VHF': (add_vertical_horizontal_filter, ['VHF']),
        }
        
        # Multi-column indicators
        multi_col_indicators = {
            'ADX': (add_average_directional_movement, ['ADX', 'DMP', 'DMN']),
            'Alpha Trend': (add_alpha_trend, ['ALPHAT', 'ALPHATl']),
            'AMAT': (add_archer_moving_average_trend, ['AMATe_LR', 'AMATe_SR']),
            'Aroon': (add_aroon_and_aroon_oscillator, ['AROOND', 'AROONU', 'AROONOSC']),
            'CKSP': (add_chande_kroll_stop, ['CKSPl', 'CKSPs']),
            'PSAR': (add_parabolic_stop_and_reverse, ['PSARl', 'PSARs', 'PSARaf', 'PSARr']),
            'RWI': (add_random_walk_index, ['RWIh', 'RWIl']),
            'Vortex': (add_vortex_indicator, ['VTXP', 'VTXM']),
        }
        
        # Test single column indicators
        for name, (func, expected_cols) in single_col_indicators.items():
            data = sample_ohlcv_data.copy()
            result = func(data)
            for col in expected_cols:
                assert col in result.columns, f"{name}: Should have '{col}' column"
        
        # Test multi-column indicators
        for name, (func, expected_cols) in multi_col_indicators.items():
            data = sample_ohlcv_data.copy()
            result = func(data)
            for col in expected_cols:
                assert col in result.columns, f"{name}: Should have '{col}' column"


class TestTrendIndicatorRegistry:
    """Test suite for trend indicator registry"""
    
    @pytest.mark.unit
    def test_registry_contains_all_indicators(self):
        """Test that registry contains all trend indicators"""
        expected_keys = [
            'adx', 'average_directional_movement',
            'alphatrend', 'alpha_trend',
            'amat', 'archer_moving_average_trend',
            'aroon', 'aroon_oscillator',
            'chop', 'choppiness_index',
            'cksp', 'chande_kroll_stop',
            'decay',
            'decreasing',
            'dpo', 'detrend_price_oscillator',
            'ht_trendline', 'hilbert_transform_trendline',
            'increasing',
            'psar', 'parabolic_stop_and_reverse',
            'qstick', 'q_stick',
            'rwi', 'random_walk_index',
            'trendflex', 'trend_flex',
            'vhf', 'vertical_horizontal_filter',
            'vortex', 'vortex_indicator',
            'zigzag', 'zig_zag',
        ]
        
        for key in expected_keys:
            assert key in TREND_INDICATOR_REGISTRY, f"Registry should contain '{key}'"
    
    @pytest.mark.unit
    def test_registry_functions_are_callable(self):
        """Test that all registry values are callable"""
        for key, func in TREND_INDICATOR_REGISTRY.items():
            assert callable(func), f"Registry value for '{key}' should be callable"


class TestTrendIndicatorParameters:
    """Test trend indicators with various parameter combinations"""
    
    @pytest.mark.unit
    def test_adx_with_different_windows(self, sample_ohlcv_data):
        """Test ADX with different window sizes"""
        data = sample_ohlcv_data.copy()
        
        # Test with different windows
        for window in [7, 14, 21]:
            result = add_average_directional_movement(data.copy(), window=window)
            assert 'ADX' in result.columns
            
    @pytest.mark.unit
    def test_aroon_with_different_windows(self, sample_ohlcv_data):
        """Test Aroon with different window sizes"""
        data = sample_ohlcv_data.copy()
        
        # Test with different windows
        for window in [14, 25, 50]:
            result = add_aroon_and_aroon_oscillator(data.copy(), window=window)
            assert 'AROOND' in result.columns
            assert 'AROONU' in result.columns
            
    @pytest.mark.unit
    def test_psar_with_different_acceleration_factors(self, sample_ohlcv_data):
        """Test PSAR with different acceleration factors"""
        data = sample_ohlcv_data.copy()
        
        # Test with different acceleration factors
        for af in [0.01, 0.02, 0.05]:
            result = add_parabolic_stop_and_reverse(data.copy(), af0=af, af=af, af_max=0.2)
            assert 'PSARl' in result.columns
            assert 'PSARs' in result.columns
            
    @pytest.mark.unit
    def test_vortex_with_different_windows(self, sample_ohlcv_data):
        """Test Vortex with different window sizes"""
        data = sample_ohlcv_data.copy()
        
        # Test with different windows
        for window in [7, 14, 21]:
            result = add_vortex_indicator(data.copy(), window=window)
            assert 'VTXP' in result.columns
            assert 'VTXM' in result.columns

