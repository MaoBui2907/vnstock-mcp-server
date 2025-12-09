"""
Test suite for ta_volume_utils.py - Volume Technical Analysis indicators.
This test file verifies each volume indicator function and validates the exact output columns.
"""

import pytest
import pandas as pd
import numpy as np
from src.vnstock_mcp.libs.ta_volume_utils import (
    add_accumulation_distribution,
    add_accumulation_distribution_oscillator,
    add_archer_on_balance_volume,
    add_chaikin_money_flow,
    add_elder_force_index,
    add_ease_of_movement,
    add_klinger_volume_oscillator,
    add_money_flow_index,
    add_negative_volume_index,
    add_on_balance_volume,
    add_percentage_volume_oscillator,
    add_price_volume,
    add_price_volume_rank,
    add_price_volume_trend,
    add_time_segmented_volume,
    add_volume_weighted_moving_average,
    VOLUME_INDICATOR_REGISTRY,
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


class TestVolumeIndicators:
    """Test suite for volume indicators with exact output column validation"""
    
    @pytest.mark.unit
    def test_add_accumulation_distribution(self, sample_ohlcv_data):
        """
        Test Accumulation/Distribution Line (A/D)
        Output columns: AD
        """
        data = sample_ohlcv_data.copy()
        result = add_accumulation_distribution(data)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_ohlcv_data)
        assert 'AD' in result.columns, "Should have 'AD' column"
        
    @pytest.mark.unit
    def test_add_accumulation_distribution_oscillator(self, sample_ohlcv_data):
        """
        Test Accumulation/Distribution Oscillator (ADOSC)
        Output columns: ADOSC
        """
        data = sample_ohlcv_data.copy()
        result = add_accumulation_distribution_oscillator(data, fast_length=3, slow_length=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ADOSC' in result.columns, "Should have 'ADOSC' column"
        
    @pytest.mark.unit
    def test_add_archer_on_balance_volume(self, sample_ohlcv_data):
        """
        Test Archer On Balance Volume (AOBV)
        Output columns: OBV, OBV_min, OBV_max, OBVe, AOBV_LR, AOBV_SR
        """
        data = sample_ohlcv_data.copy()
        result = add_archer_on_balance_volume(data, fast_length=4, slow_length=12)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns, "Should have 'OBV' column"
        assert 'AOBV_LR' in result.columns, "Should have 'AOBV_LR' column"
        assert 'AOBV_SR' in result.columns, "Should have 'AOBV_SR' column"
        
    @pytest.mark.unit
    def test_add_chaikin_money_flow(self, sample_ohlcv_data):
        """
        Test Chaikin Money Flow (CMF)
        Output columns: CMF
        """
        data = sample_ohlcv_data.copy()
        result = add_chaikin_money_flow(data, window=20)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CMF' in result.columns, "Should have 'CMF' column"
        
    @pytest.mark.unit
    def test_add_elder_force_index(self, sample_ohlcv_data):
        """
        Test Elder Force Index (EFI)
        Output columns: EFI
        """
        data = sample_ohlcv_data.copy()
        result = add_elder_force_index(data, window=13)
        
        assert isinstance(result, pd.DataFrame)
        assert 'EFI' in result.columns, "Should have 'EFI' column"
        
    @pytest.mark.unit
    def test_add_ease_of_movement(self, sample_ohlcv_data):
        """
        Test Ease of Movement (EOM)
        Output columns: EOM
        """
        data = sample_ohlcv_data.copy()
        result = add_ease_of_movement(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'EOM' in result.columns, "Should have 'EOM' column"
        
    @pytest.mark.unit
    def test_add_klinger_volume_oscillator(self, sample_ohlcv_data):
        """
        Test Klinger Volume Oscillator (KVO)
        Output columns: KVO, KVOs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_klinger_volume_oscillator(data, fast_length=34, slow_length=55, signal_length=13)
        
        assert isinstance(result, pd.DataFrame)
        assert 'KVO' in result.columns, "Should have 'KVO' column"
        assert 'KVOs' in result.columns, "Should have 'KVOs' column"
        
    @pytest.mark.unit
    def test_add_money_flow_index(self, sample_ohlcv_data):
        """
        Test Money Flow Index (MFI)
        Output columns: MFI
        """
        data = sample_ohlcv_data.copy()
        result = add_money_flow_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'MFI' in result.columns, "Should have 'MFI' column"
        
    @pytest.mark.unit
    def test_add_negative_volume_index(self, sample_ohlcv_data):
        """
        Test Negative Volume Index (NVI)
        Output columns: NVI
        """
        data = sample_ohlcv_data.copy()
        result = add_negative_volume_index(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'NVI' in result.columns, "Should have 'NVI' column"
        
    @pytest.mark.unit
    def test_add_on_balance_volume(self, sample_ohlcv_data):
        """
        Test On Balance Volume (OBV)
        Output columns: OBV
        """
        data = sample_ohlcv_data.copy()
        result = add_on_balance_volume(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'OBV' in result.columns, "Should have 'OBV' column"
        
    @pytest.mark.unit
    def test_add_percentage_volume_oscillator(self, sample_ohlcv_data):
        """
        Test Percentage Volume Oscillator (PVO)
        Output columns: PVO, PVOh (Histogram), PVOs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_percentage_volume_oscillator(data, fast_length=12, slow_length=26, signal_length=9)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PVO' in result.columns, "Should have 'PVO' column"
        assert 'PVOh' in result.columns, "Should have 'PVOh' column"
        assert 'PVOs' in result.columns, "Should have 'PVOs' column"
        
    @pytest.mark.unit
    def test_add_price_volume(self, sample_ohlcv_data):
        """
        Test Price Volume (PVOL)
        Output columns: PVOL
        """
        data = sample_ohlcv_data.copy()
        result = add_price_volume(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PVOL' in result.columns, "Should have 'PVOL' column"
        
    @pytest.mark.unit
    def test_add_price_volume_rank(self, sample_ohlcv_data):
        """
        Test Price Volume Rank (PVR)
        Output columns: PVR
        """
        data = sample_ohlcv_data.copy()
        result = add_price_volume_rank(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PVR' in result.columns, "Should have 'PVR' column"
        
    @pytest.mark.unit
    def test_add_price_volume_trend(self, sample_ohlcv_data):
        """
        Test Price Volume Trend (PVT)
        Output columns: PVT
        """
        data = sample_ohlcv_data.copy()
        result = add_price_volume_trend(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PVT' in result.columns, "Should have 'PVT' column"
        
    @pytest.mark.unit
    def test_add_time_segmented_volume(self, sample_ohlcv_data):
        """
        Test Time Segmented Volume (TSV)
        Output columns: TSV, TSVs (Signal), TSVr (Ratio)
        """
        data = sample_ohlcv_data.copy()
        result = add_time_segmented_volume(data, window=18, signal_length=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'TSV' in result.columns, "Should have 'TSV' column"
        assert 'TSVs' in result.columns, "Should have 'TSVs' column"
        assert 'TSVr' in result.columns, "Should have 'TSVr' column"
        
    @pytest.mark.unit
    def test_add_volume_weighted_moving_average(self, sample_ohlcv_data):
        """
        Test Volume Weighted Moving Average (VWMA)
        Output columns: VWMA
        """
        data = sample_ohlcv_data.copy()
        result = add_volume_weighted_moving_average(data, window=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'VWMA' in result.columns, "Should have 'VWMA' column"


class TestVolumeDataIntegrity:
    """Test data integrity for volume indicators"""
    
    @pytest.mark.unit
    def test_original_data_preserved(self, sample_ohlcv_data):
        """Test that original OHLCV columns are preserved after adding indicators"""
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        # Add multiple indicators
        data = add_on_balance_volume(data)
        data = add_money_flow_index(data)
        data = add_chaikin_money_flow(data)
        
        # Check original columns are preserved
        for col in original_cols:
            assert col in data.columns, f"Original column '{col}' should be preserved"
            
    @pytest.mark.unit
    def test_indicator_values_are_numeric(self, sample_ohlcv_data):
        """Test that indicator values are numeric"""
        data = sample_ohlcv_data.copy()
        
        data = add_on_balance_volume(data)
        assert pd.api.types.is_numeric_dtype(data['OBV']), "OBV values should be numeric"
        
        data = add_money_flow_index(data)
        assert pd.api.types.is_numeric_dtype(data['MFI']), "MFI values should be numeric"
        
    @pytest.mark.unit
    def test_chaining_multiple_indicators(self, sample_ohlcv_data):
        """Test chaining multiple volume indicators"""
        data = sample_ohlcv_data.copy()
        
        # Chain multiple indicators
        data = add_on_balance_volume(data)
        data = add_money_flow_index(data)
        data = add_chaikin_money_flow(data)
        data = add_accumulation_distribution(data)
        data = add_price_volume_trend(data)
        
        # All indicators should be present
        assert 'OBV' in data.columns
        assert 'MFI' in data.columns
        assert 'CMF' in data.columns
        assert 'AD' in data.columns
        assert 'PVT' in data.columns


class TestVolumeIndicatorOutputColumnsSummary:
    """Summary test to document all volume indicator output columns"""
    
    @pytest.mark.unit
    def test_all_volume_indicators_output_columns(self, sample_ohlcv_data):
        """
        Summary test for all volume indicators and their output columns.
        
        Expected output columns:
        - AD: AD
        - ADOSC: ADOSC
        - AOBV: OBV, OBV_min, OBV_max, OBVe, AOBV_LR, AOBV_SR
        - CMF: CMF
        - EFI: EFI
        - EOM: EOM
        - KVO: KVO, KVOs
        - MFI: MFI
        - NVI: NVI
        - OBV: OBV
        - PVO: PVO, PVOh, PVOs
        - PVOL: PVOL
        - PVR: PVR
        - PVT: PVT
        - TSV: TSV, TSVs, TSVr
        - VWMA: VWMA
        """
        # Single column indicators
        single_col_indicators = {
            'AD': (add_accumulation_distribution, ['AD']),
            'ADOSC': (add_accumulation_distribution_oscillator, ['ADOSC']),
            'CMF': (add_chaikin_money_flow, ['CMF']),
            'EFI': (add_elder_force_index, ['EFI']),
            'EOM': (add_ease_of_movement, ['EOM']),
            'MFI': (add_money_flow_index, ['MFI']),
            'NVI': (add_negative_volume_index, ['NVI']),
            'OBV': (add_on_balance_volume, ['OBV']),
            'PVOL': (add_price_volume, ['PVOL']),
            'PVR': (add_price_volume_rank, ['PVR']),
            'PVT': (add_price_volume_trend, ['PVT']),
            'VWMA': (add_volume_weighted_moving_average, ['VWMA']),
        }
        
        # Multi-column indicators
        multi_col_indicators = {
            'AOBV': (add_archer_on_balance_volume, ['OBV', 'AOBV_LR', 'AOBV_SR']),
            'KVO': (add_klinger_volume_oscillator, ['KVO', 'KVOs']),
            'PVO': (add_percentage_volume_oscillator, ['PVO', 'PVOh', 'PVOs']),
            'TSV': (add_time_segmented_volume, ['TSV', 'TSVs', 'TSVr']),
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


class TestVolumeIndicatorRegistry:
    """Test suite for volume indicator registry"""
    
    @pytest.mark.unit
    def test_registry_contains_all_indicators(self):
        """Test that registry contains all volume indicators"""
        expected_keys = [
            'ad', 'accumulation_distribution',
            'adosc', 'accumulation_distribution_oscillator',
            'aobv', 'archer_on_balance_volume',
            'cmf', 'chaikin_money_flow',
            'efi', 'elder_force_index',
            'eom', 'ease_of_movement',
            'kvo', 'klinger_volume_oscillator',
            'mfi', 'money_flow_index',
            'nvi', 'negative_volume_index',
            'obv', 'on_balance_volume',
            'pvo', 'percentage_volume_oscillator',
            'pvol', 'price_volume',
            'pvr', 'price_volume_rank',
            'pvt', 'price_volume_trend',
            'tsv', 'time_segmented_volume',
            'vwma', 'volume_weighted_moving_average',
        ]
        
        for key in expected_keys:
            assert key in VOLUME_INDICATOR_REGISTRY, f"Registry should contain '{key}'"
    
    @pytest.mark.unit
    def test_registry_functions_are_callable(self):
        """Test that all registry values are callable"""
        for key, func in VOLUME_INDICATOR_REGISTRY.items():
            assert callable(func), f"Registry value for '{key}' should be callable"


class TestVolumeIndicatorParameters:
    """Test volume indicators with various parameter combinations"""
    
    @pytest.mark.unit
    def test_cmf_with_different_windows(self, sample_ohlcv_data):
        """Test CMF with different window sizes"""
        data = sample_ohlcv_data.copy()
        
        # Test with different windows
        for window in [10, 20, 30]:
            result = add_chaikin_money_flow(data.copy(), window=window)
            assert 'CMF' in result.columns
            
    @pytest.mark.unit
    def test_mfi_with_different_windows(self, sample_ohlcv_data):
        """Test MFI with different window sizes"""
        data = sample_ohlcv_data.copy()
        
        # Test with different windows
        for window in [7, 14, 21]:
            result = add_money_flow_index(data.copy(), window=window)
            assert 'MFI' in result.columns
            
    @pytest.mark.unit
    def test_kvo_with_different_parameters(self, sample_ohlcv_data):
        """Test KVO with different parameters"""
        data = sample_ohlcv_data.copy()
        
        result = add_klinger_volume_oscillator(data.copy(), fast_length=20, slow_length=40, signal_length=10)
        assert 'KVO' in result.columns
        assert 'KVOs' in result.columns
        
    @pytest.mark.unit
    def test_pvo_with_different_parameters(self, sample_ohlcv_data):
        """Test PVO with different parameters"""
        data = sample_ohlcv_data.copy()
        
        result = add_percentage_volume_oscillator(data.copy(), fast_length=10, slow_length=20, signal_length=5)
        assert 'PVO' in result.columns
        assert 'PVOh' in result.columns
        assert 'PVOs' in result.columns

