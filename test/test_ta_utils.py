"""
Test suite for ta_utils.py - Technical Analysis indicators
This test file verifies each TA indicator function and validates the exact output columns
"""

import pytest
import pandas as pd
import numpy as np
from src.vnstock_mcp.libs.ta_utils import (
    # Momentum indicators
    add_awesome_oscillator,
    add_absolute_price_oscillator,
    add_bias,
    add_balance_of_power,
    add_br_and_ar,
    add_commodity_channel_index,
    add_chande_forecast_oscillator,
    add_center_of_gravity,
    add_chande_momentum_oscillator,
    add_coppock_curve,
    add_connors_relative_strength_index,
    add_correlation_trend_indicator,
    add_directional_movement,
    add_efficiency_ratio,
    add_elder_ray_index,
    add_fisher_transform,
    add_inertia,
    add_kdj,
    add_know_sure_thing,
    add_moving_average_convergence_divergence,
    add_momentum,
    add_pretty_good_oscillator,
    add_percentage_price_oscillator,
    add_psychological_line,
    add_quantitative_qualitative_estimation,
    add_rate_of_change,
    add_relative_strength_index,
    add_relative_strength_xtra,
    add_relative_vigor_index,
    add_slope,
    add_smart_money_concept,
    add_smi_ergodic_indicator,
    add_squeeze,
    add_schaff_trend_cycle,
    add_stochastic,
    add_fast_stochastic,
    add_stochastic_relative_strength_index,
    add_true_momentum_oscillator,
    add_trix,
    add_true_strength_index,
    add_ultimate_oscillator,
    add_williams_percent_r,
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


class TestMomentumIndicators:
    """Test suite for momentum indicators with exact output column validation"""
    
    @pytest.mark.unit
    def test_add_awesome_oscillator(self, sample_ohlcv_data):
        """
        Test Awesome Oscillator (AO)
        Output columns: AO
        """
        data = sample_ohlcv_data.copy()
        result = add_awesome_oscillator(data, fast_length=5, slow_length=34)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_ohlcv_data)
        assert 'AO' in result.columns, "Should have 'AO' column"
        
    @pytest.mark.unit
    def test_add_absolute_price_oscillator(self, sample_ohlcv_data):
        """
        Test Absolute Price Oscillator (APO)
        Output columns: APO
        """
        data = sample_ohlcv_data.copy()
        result = add_absolute_price_oscillator(data, fast_length=12, slow_length=26)
        
        assert isinstance(result, pd.DataFrame)
        assert 'APO' in result.columns, "Should have 'APO' column"
        
    @pytest.mark.unit
    def test_add_bias(self, sample_ohlcv_data):
        """
        Test Bias indicator
        Output columns: BIAS_SMA
        """
        data = sample_ohlcv_data.copy()
        result = add_bias(data, window=26)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BIAS_SMA' in result.columns, "Should have 'BIAS_SMA' column"
        
    @pytest.mark.unit
    def test_add_balance_of_power(self, sample_ohlcv_data):
        """
        Test Balance of Power (BOP)
        Output columns: BOP
        """
        data = sample_ohlcv_data.copy()
        result = add_balance_of_power(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BOP' in result.columns, "Should have 'BOP' column"
        
    @pytest.mark.unit
    def test_add_br_and_ar(self, sample_ohlcv_data):
        """
        Test BRAR (BR and AR indicators)
        Output columns: AR, BR
        """
        data = sample_ohlcv_data.copy()
        result = add_br_and_ar(data, window=26)
        
        assert isinstance(result, pd.DataFrame)
        assert 'AR' in result.columns, "Should have 'AR' column"
        assert 'BR' in result.columns, "Should have 'BR' column"
        
    @pytest.mark.unit
    def test_add_commodity_channel_index(self, sample_ohlcv_data):
        """
        Test Commodity Channel Index (CCI)
        Output columns: CCI
        """
        data = sample_ohlcv_data.copy()
        result = add_commodity_channel_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CCI' in result.columns, "Should have 'CCI' column"
        
    @pytest.mark.unit
    def test_add_chande_forecast_oscillator(self, sample_ohlcv_data):
        """
        Test Chande Forecast Oscillator (CFO)
        Output columns: CFO
        """
        data = sample_ohlcv_data.copy()
        result = add_chande_forecast_oscillator(data, window=9)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CFO' in result.columns, "Should have 'CFO' column"
        
    @pytest.mark.unit
    def test_add_center_of_gravity(self, sample_ohlcv_data):
        """
        Test Center of Gravity (CG)
        Output columns: CG
        """
        data = sample_ohlcv_data.copy()
        result = add_center_of_gravity(data, window=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CG' in result.columns, "Should have 'CG' column"
        
    @pytest.mark.unit
    def test_add_chande_momentum_oscillator(self, sample_ohlcv_data):
        """
        Test Chande Momentum Oscillator (CMO)
        Output columns: CMO
        """
        data = sample_ohlcv_data.copy()
        result = add_chande_momentum_oscillator(data, window=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CMO' in result.columns, "Should have 'CMO' column"
        
    @pytest.mark.unit
    def test_add_coppock_curve(self, sample_ohlcv_data):
        """
        Test Coppock Curve
        Output columns: COPC
        """
        data = sample_ohlcv_data.copy()
        result = add_coppock_curve(data, window=10, fast_length=11, slow_length=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'COPC' in result.columns, "Should have 'COPC' column"
        
    @pytest.mark.unit
    def test_add_connors_relative_strength_index(self, sample_ohlcv_data):
        """
        Test Connors RSI
        Output columns: CRSI
        """
        data = sample_ohlcv_data.copy()
        result = add_connors_relative_strength_index(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CRSI' in result.columns, "Should have 'CRSI' column"
        
    @pytest.mark.unit
    def test_add_correlation_trend_indicator(self, sample_ohlcv_data):
        """
        Test Correlation Trend Indicator (CTI)
        Output columns: CTI
        """
        data = sample_ohlcv_data.copy()
        result = add_correlation_trend_indicator(data, window=12)
        
        assert isinstance(result, pd.DataFrame)
        assert 'CTI' in result.columns, "Should have 'CTI' column"
        
    @pytest.mark.unit
    def test_add_directional_movement(self, sample_ohlcv_data):
        """
        Test Directional Movement (DM)
        Output columns: DMP (Plus), DMN (Minus)
        """
        data = sample_ohlcv_data.copy()
        result = add_directional_movement(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'DMP' in result.columns, "Should have 'DMP' column"
        assert 'DMN' in result.columns, "Should have 'DMN' column"
        
    @pytest.mark.unit
    def test_add_efficiency_ratio(self, sample_ohlcv_data):
        """
        Test Efficiency Ratio (ER)
        Output columns: ER
        """
        data = sample_ohlcv_data.copy()
        result = add_efficiency_ratio(data, window=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ER' in result.columns, "Should have 'ER' column"
        
    @pytest.mark.unit
    def test_add_elder_ray_index(self, sample_ohlcv_data):
        """
        Test Elder Ray Index
        Output columns: BULLP (Bull Power), BEARP (Bear Power)
        """
        data = sample_ohlcv_data.copy()
        result = add_elder_ray_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'BULLP' in result.columns, "Should have 'BULLP' column"
        assert 'BEARP' in result.columns, "Should have 'BEARP' column"
        
    @pytest.mark.unit
    def test_add_fisher_transform(self, sample_ohlcv_data):
        """
        Test Fisher Transform
        Output columns: FISHERT (Fisher), FISHERTs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_fisher_transform(data, window=9)
        
        assert isinstance(result, pd.DataFrame)
        assert 'FISHERT' in result.columns, "Should have 'FISHERT' column"
        assert 'FISHERTs' in result.columns, "Should have 'FISHERTs' column"
        
    @pytest.mark.unit
    def test_add_inertia(self, sample_ohlcv_data):
        """
        Test Inertia indicator
        Output columns: INERTIA
        """
        data = sample_ohlcv_data.copy()
        result = add_inertia(data, window=20, rvi_length=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'INERTIA' in result.columns, "Should have 'INERTIA' column"
        
    @pytest.mark.unit
    def test_add_kdj(self, sample_ohlcv_data):
        """
        Test KDJ indicator
        Output columns: K, D, J
        """
        data = sample_ohlcv_data.copy()
        result = add_kdj(data, window=9, signal_window=3)
        
        assert isinstance(result, pd.DataFrame)
        assert 'K' in result.columns, "Should have 'K' column"
        assert 'D' in result.columns, "Should have 'D' column"
        assert 'J' in result.columns, "Should have 'J' column"
        
    @pytest.mark.unit
    def test_add_know_sure_thing(self, sample_ohlcv_data):
        """
        Test Know Sure Thing (KST)
        Output columns: KST, KSTs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_know_sure_thing(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'KST' in result.columns, "Should have 'KST' column"
        assert 'KSTs' in result.columns, "Should have 'KSTs' column"
        
    @pytest.mark.unit
    def test_add_moving_average_convergence_divergence(self, sample_ohlcv_data):
        """
        Test MACD
        Output columns: MACD, MACDh (Histogram), MACDs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_moving_average_convergence_divergence(data, fast_length=12, slow_length=26, signal_length=9)
        
        assert isinstance(result, pd.DataFrame)
        assert 'MACD' in result.columns, "Should have 'MACD' column"
        assert 'MACDh' in result.columns, "Should have 'MACDh' column"
        assert 'MACDs' in result.columns, "Should have 'MACDs' column"
        
    @pytest.mark.unit
    def test_add_momentum(self, sample_ohlcv_data):
        """
        Test Momentum (MOM)
        Output columns: MOM
        """
        data = sample_ohlcv_data.copy()
        result = add_momentum(data, window=1)
        
        assert isinstance(result, pd.DataFrame)
        assert 'MOM' in result.columns, "Should have 'MOM' column"
        
    @pytest.mark.unit
    def test_add_pretty_good_oscillator(self, sample_ohlcv_data):
        """
        Test Pretty Good Oscillator (PGO)
        Output columns: PGO
        """
        data = sample_ohlcv_data.copy()
        result = add_pretty_good_oscillator(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PGO' in result.columns, "Should have 'PGO' column"
        
    @pytest.mark.unit
    def test_add_percentage_price_oscillator(self, sample_ohlcv_data):
        """
        Test Percentage Price Oscillator (PPO)
        Output columns: PPO, PPOh (Histogram), PPOs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_percentage_price_oscillator(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PPO' in result.columns, "Should have 'PPO' column"
        assert 'PPOh' in result.columns, "Should have 'PPOh' column"
        assert 'PPOs' in result.columns, "Should have 'PPOs' column"
        
    @pytest.mark.unit
    def test_add_psychological_line(self, sample_ohlcv_data):
        """
        Test Psychological Line (PSL)
        Output columns: PSL
        """
        data = sample_ohlcv_data.copy()
        result = add_psychological_line(data, window=12)
        
        assert isinstance(result, pd.DataFrame)
        assert 'PSL' in result.columns, "Should have 'PSL' column"
        
    @pytest.mark.unit
    def test_add_quantitative_qualitative_estimation(self, sample_ohlcv_data):
        """
        Test Quantitative Qualitative Estimation (QQE)
        Output columns: QQE, QQEl, QQEs (may vary)
        """
        data = sample_ohlcv_data.copy()
        result = add_quantitative_qualitative_estimation(data)
        
        assert isinstance(result, pd.DataFrame)
        # QQE indicator adds at least one column
        original_cols = set(sample_ohlcv_data.columns)
        new_cols = [col for col in result.columns if col not in original_cols]
        assert len(new_cols) >= 1, "QQE should add at least one column"
        
    @pytest.mark.unit
    def test_add_rate_of_change(self, sample_ohlcv_data):
        """
        Test Rate of Change (ROC)
        Output columns: ROC
        """
        data = sample_ohlcv_data.copy()
        result = add_rate_of_change(data, window=10)
        
        assert isinstance(result, pd.DataFrame)
        assert 'ROC' in result.columns, "Should have 'ROC' column"
        
    @pytest.mark.unit
    def test_add_relative_strength_index(self, sample_ohlcv_data):
        """
        Test Relative Strength Index (RSI)
        Output columns: RSI
        """
        data = sample_ohlcv_data.copy()
        result = add_relative_strength_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'RSI' in result.columns, "Should have 'RSI' column"
        
    @pytest.mark.unit
    def test_add_relative_strength_xtra(self, sample_ohlcv_data):
        """
        Test Relative Strength Xtra (RSX)
        Output columns: RSX
        """
        data = sample_ohlcv_data.copy()
        result = add_relative_strength_xtra(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'RSX' in result.columns, "Should have 'RSX' column"
        
    @pytest.mark.unit
    def test_add_relative_vigor_index(self, sample_ohlcv_data):
        """
        Test Relative Vigor Index (RVGI)
        Output columns: RVGI, RVGIs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_relative_vigor_index(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'RVGI' in result.columns, "Should have 'RVGI' column"
        assert 'RVGIs' in result.columns, "Should have 'RVGIs' column"
        
    @pytest.mark.unit
    def test_add_slope(self, sample_ohlcv_data):
        """
        Test Slope indicator
        Output columns: SLOPE
        """
        data = sample_ohlcv_data.copy()
        result = add_slope(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'SLOPE' in result.columns, "Should have 'SLOPE' column"
        
    @pytest.mark.unit
    def test_add_smart_money_concept(self, sample_ohlcv_data):
        """
        Test Smart Money Concept (SMC)
        Output columns: SMChv, SMCbf, SMCbi, SMCbp, SMCtf, SMCti, SMCtp
        """
        data = sample_ohlcv_data.copy()
        result = add_smart_money_concept(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'SMChv' in result.columns, "Should have 'SMChv' (High Volume) column"
        assert 'SMCbf' in result.columns, "Should have 'SMCbf' (Bullish FVG) column"
        assert 'SMCbi' in result.columns, "Should have 'SMCbi' (Bullish Imbalance) column"
        assert 'SMCbp' in result.columns, "Should have 'SMCbp' (Bullish Price) column"
        assert 'SMCtf' in result.columns, "Should have 'SMCtf' (Bearish FVG) column"
        assert 'SMCti' in result.columns, "Should have 'SMCti' (Bearish Imbalance) column"
        assert 'SMCtp' in result.columns, "Should have 'SMCtp' (Bearish Price) column"
        
    @pytest.mark.unit
    def test_add_smi_ergodic_indicator(self, sample_ohlcv_data):
        """
        Test SMI Ergodic Indicator
        Output columns: SMI, SMIs (Signal), SMIo (Oscillator)
        """
        data = sample_ohlcv_data.copy()
        result = add_smi_ergodic_indicator(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'SMI' in result.columns, "Should have 'SMI' column"
        assert 'SMIs' in result.columns, "Should have 'SMIs' column"
        assert 'SMIo' in result.columns, "Should have 'SMIo' column"
        
    @pytest.mark.unit
    def test_add_squeeze(self, sample_ohlcv_data):
        """
        Test Squeeze indicator
        Output columns: SQZ, SQZ_ON, SQZ_OFF, SQZ_NO
        """
        data = sample_ohlcv_data.copy()
        result = add_squeeze(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'SQZ' in result.columns, "Should have 'SQZ' column"
        assert 'SQZ_ON' in result.columns, "Should have 'SQZ_ON' column"
        assert 'SQZ_OFF' in result.columns, "Should have 'SQZ_OFF' column"
        assert 'SQZ_NO' in result.columns, "Should have 'SQZ_NO' column"
        
    @pytest.mark.unit
    def test_add_schaff_trend_cycle(self, sample_ohlcv_data):
        """
        Test Schaff Trend Cycle (STC)
        Output columns: STC, STCmacd, STCstoch
        """
        data = sample_ohlcv_data.copy()
        result = add_schaff_trend_cycle(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'STC' in result.columns, "Should have 'STC' column"
        assert 'STCmacd' in result.columns, "Should have 'STCmacd' column"
        assert 'STCstoch' in result.columns, "Should have 'STCstoch' column"
        
    @pytest.mark.unit
    def test_add_stochastic(self, sample_ohlcv_data):
        """
        Test Stochastic Oscillator
        Output columns: STOCHk (%K), STOCHd (%D), STOCHh (Histogram)
        """
        data = sample_ohlcv_data.copy()
        result = add_stochastic(data, k=14, d=3, smooth_k=3)
        
        assert isinstance(result, pd.DataFrame)
        assert 'STOCHk' in result.columns, "Should have 'STOCHk' column"
        assert 'STOCHd' in result.columns, "Should have 'STOCHd' column"
        assert 'STOCHh' in result.columns, "Should have 'STOCHh' column"
        
    @pytest.mark.unit
    def test_add_fast_stochastic(self, sample_ohlcv_data):
        """
        Test Fast Stochastic
        Output columns: STOCHFk (%K), STOCHFd (%D)
        """
        data = sample_ohlcv_data.copy()
        result = add_fast_stochastic(data, k=14, d=3)
        
        assert isinstance(result, pd.DataFrame)
        assert 'STOCHFk' in result.columns, "Should have 'STOCHFk' column"
        assert 'STOCHFd' in result.columns, "Should have 'STOCHFd' column"
        
    @pytest.mark.unit
    def test_add_stochastic_relative_strength_index(self, sample_ohlcv_data):
        """
        Test Stochastic RSI
        Output columns: STOCHRSIk (%K), STOCHRSId (%D)
        """
        data = sample_ohlcv_data.copy()
        result = add_stochastic_relative_strength_index(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'STOCHRSIk' in result.columns, "Should have 'STOCHRSIk' column"
        assert 'STOCHRSId' in result.columns, "Should have 'STOCHRSId' column"
        
    @pytest.mark.unit
    def test_add_true_momentum_oscillator(self, sample_ohlcv_data):
        """
        Test True Momentum Oscillator (TMO)
        Output columns: TMO, TMOs, TMOM, TMOMs
        """
        data = sample_ohlcv_data.copy()
        result = add_true_momentum_oscillator(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'TMO' in result.columns, "Should have 'TMO' column"
        assert 'TMOs' in result.columns, "Should have 'TMOs' column"
        assert 'TMOM' in result.columns, "Should have 'TMOM' column"
        assert 'TMOMs' in result.columns, "Should have 'TMOMs' column"
        
    @pytest.mark.unit
    def test_add_trix(self, sample_ohlcv_data):
        """
        Test TRIX indicator
        Output columns: TRIX, TRIXs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_trix(data, window=18, signal_window=9)
        
        assert isinstance(result, pd.DataFrame)
        assert 'TRIX' in result.columns, "Should have 'TRIX' column"
        assert 'TRIXs' in result.columns, "Should have 'TRIXs' column"
        
    @pytest.mark.unit
    def test_add_true_strength_index(self, sample_ohlcv_data):
        """
        Test True Strength Index (TSI)
        Output columns: TSI, TSIs (Signal)
        """
        data = sample_ohlcv_data.copy()
        result = add_true_strength_index(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'TSI' in result.columns, "Should have 'TSI' column"
        assert 'TSIs' in result.columns, "Should have 'TSIs' column"
        
    @pytest.mark.unit
    def test_add_ultimate_oscillator(self, sample_ohlcv_data):
        """
        Test Ultimate Oscillator (UO)
        Output columns: UO
        """
        data = sample_ohlcv_data.copy()
        result = add_ultimate_oscillator(data)
        
        assert isinstance(result, pd.DataFrame)
        assert 'UO' in result.columns, "Should have 'UO' column"
        
    @pytest.mark.unit
    def test_add_williams_percent_r(self, sample_ohlcv_data):
        """
        Test Williams %R
        Output columns: WILLR
        """
        data = sample_ohlcv_data.copy()
        result = add_williams_percent_r(data, window=14)
        
        assert isinstance(result, pd.DataFrame)
        assert 'WILLR' in result.columns, "Should have 'WILLR' column"


class TestIndicatorDataIntegrity:
    """Test data integrity for all indicators"""
    
    @pytest.mark.unit
    def test_original_data_preserved(self, sample_ohlcv_data):
        """Test that original OHLCV columns are preserved after adding indicators"""
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        # Add multiple indicators
        data = add_relative_strength_index(data)
        data = add_moving_average_convergence_divergence(data)
        data = add_stochastic(data)
        
        # Check original columns are preserved
        for col in original_cols:
            assert col in data.columns, f"Original column '{col}' should be preserved"
            
    @pytest.mark.unit
    def test_indicator_values_are_numeric(self, sample_ohlcv_data):
        """Test that indicator values are numeric"""
        data = sample_ohlcv_data.copy()
        
        data = add_relative_strength_index(data)
        assert pd.api.types.is_numeric_dtype(data['RSI']), "RSI values should be numeric"
        
        data = add_moving_average_convergence_divergence(data)
        assert pd.api.types.is_numeric_dtype(data['MACD']), "MACD values should be numeric"
        
    @pytest.mark.unit
    def test_chaining_multiple_indicators(self, sample_ohlcv_data):
        """Test chaining multiple indicators"""
        data = sample_ohlcv_data.copy()
        
        # Chain multiple indicators
        data = add_relative_strength_index(data)
        data = add_moving_average_convergence_divergence(data)
        data = add_stochastic(data)
        data = add_williams_percent_r(data)
        data = add_momentum(data)
        
        # All indicators should be present
        assert 'RSI' in data.columns
        assert 'MACD' in data.columns
        assert 'MACDh' in data.columns
        assert 'MACDs' in data.columns
        assert 'STOCHk' in data.columns
        assert 'STOCHd' in data.columns
        assert 'WILLR' in data.columns
        assert 'MOM' in data.columns


class TestIndicatorOutputColumnsSummary:
    """Summary test to document all indicator output columns"""
    
    @pytest.mark.unit
    def test_all_indicators_output_columns(self, sample_ohlcv_data):
        """
        Summary test for all indicators and their output columns.
        
        Expected output columns:
        - AO: AO
        - APO: APO
        - BIAS: BIAS_SMA
        - BOP: BOP
        - BRAR: AR, BR
        - CCI: CCI
        - CFO: CFO
        - CG: CG
        - CMO: CMO
        - Coppock: COPC
        - CRSI: CRSI
        - CTI: CTI
        - DM: DMP, DMN
        - ER: ER
        - Elder Ray: BULLP, BEARP
        - Fisher: FISHERT, FISHERTs
        - Inertia: INERTIA
        - KDJ: K, D, J
        - KST: KST, KSTs
        - MACD: MACD, MACDh, MACDs
        - MOM: MOM
        - PGO: PGO
        - PPO: PPO, PPOh, PPOs
        - PSL: PSL
        - QQE: (varies)
        - ROC: ROC
        - RSI: RSI
        - RSX: RSX
        - RVGI: RVGI, RVGIs
        - SLOPE: SLOPE
        - SMI: SMI, SMIs, SMIo
        - Squeeze: SQZ, SQZ_ON, SQZ_OFF, SQZ_NO
        - STC: STC, STCmacd, STCstoch
        - Stochastic: STOCHk, STOCHd, STOCHh
        - Fast Stochastic: STOCHFk, STOCHFd
        - Stochastic RSI: STOCHRSIk, STOCHRSId
        - TMO: TMO, TMOs, TMOM, TMOMs
        - TRIX: TRIX, TRIXs
        - TSI: TSI, TSIs
        - UO: UO
        - WILLR: WILLR
        """
        # Single column indicators
        single_col_indicators = {
            'AO': (add_awesome_oscillator, ['AO']),
            'APO': (add_absolute_price_oscillator, ['APO']),
            'BIAS': (add_bias, ['BIAS_SMA']),
            'BOP': (add_balance_of_power, ['BOP']),
            'CCI': (add_commodity_channel_index, ['CCI']),
            'CFO': (add_chande_forecast_oscillator, ['CFO']),
            'CG': (add_center_of_gravity, ['CG']),
            'CMO': (add_chande_momentum_oscillator, ['CMO']),
            'COPC': (add_coppock_curve, ['COPC']),
            'CRSI': (add_connors_relative_strength_index, ['CRSI']),
            'CTI': (add_correlation_trend_indicator, ['CTI']),
            'ER': (add_efficiency_ratio, ['ER']),
            'INERTIA': (add_inertia, ['INERTIA']),
            'MOM': (add_momentum, ['MOM']),
            'PGO': (add_pretty_good_oscillator, ['PGO']),
            'PSL': (add_psychological_line, ['PSL']),
            'ROC': (add_rate_of_change, ['ROC']),
            'RSI': (add_relative_strength_index, ['RSI']),
            'RSX': (add_relative_strength_xtra, ['RSX']),
            'SLOPE': (add_slope, ['SLOPE']),
            'UO': (add_ultimate_oscillator, ['UO']),
            'WILLR': (add_williams_percent_r, ['WILLR']),
        }
        
        # Multi-column indicators
        multi_col_indicators = {
            'BRAR': (add_br_and_ar, ['AR', 'BR']),
            'DM': (add_directional_movement, ['DMP', 'DMN']),
            'Elder Ray': (add_elder_ray_index, ['BULLP', 'BEARP']),
            'Fisher': (add_fisher_transform, ['FISHERT', 'FISHERTs']),
            'KDJ': (add_kdj, ['K', 'D', 'J']),
            'KST': (add_know_sure_thing, ['KST', 'KSTs']),
            'MACD': (add_moving_average_convergence_divergence, ['MACD', 'MACDh', 'MACDs']),
            'PPO': (add_percentage_price_oscillator, ['PPO', 'PPOh', 'PPOs']),
            'RVGI': (add_relative_vigor_index, ['RVGI', 'RVGIs']),
            'SMC': (add_smart_money_concept, ['SMChv', 'SMCbf', 'SMCbi', 'SMCbp', 'SMCtf', 'SMCti', 'SMCtp']),
            'SMI': (add_smi_ergodic_indicator, ['SMI', 'SMIs', 'SMIo']),
            'Squeeze': (add_squeeze, ['SQZ', 'SQZ_ON', 'SQZ_OFF', 'SQZ_NO']),
            'STC': (add_schaff_trend_cycle, ['STC', 'STCmacd', 'STCstoch']),
            'Stochastic': (add_stochastic, ['STOCHk', 'STOCHd', 'STOCHh']),
            'Fast Stochastic': (add_fast_stochastic, ['STOCHFk', 'STOCHFd']),
            'Stochastic RSI': (add_stochastic_relative_strength_index, ['STOCHRSIk', 'STOCHRSId']),
            'TMO': (add_true_momentum_oscillator, ['TMO', 'TMOs', 'TMOM', 'TMOMs']),
            'TRIX': (add_trix, ['TRIX', 'TRIXs']),
            'TSI': (add_true_strength_index, ['TSI', 'TSIs']),
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


class TestHelperFunctions:
    """Test suite for helper functions in ta_utils"""
    
    @pytest.mark.unit
    def test_strip_numeric_suffix(self):
        """Test _strip_numeric_suffix function"""
        from src.vnstock_mcp.libs.ta_utils import _strip_numeric_suffix
        
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
        from src.vnstock_mcp.libs.ta_utils import _merge_indicator_result
        
        data = sample_ohlcv_data.copy()
        original_cols = list(data.columns)
        
        result = _merge_indicator_result(data, None)
        
        assert result is data
        assert list(result.columns) == original_cols
    
    @pytest.mark.unit
    def test_merge_indicator_result_with_series(self, sample_ohlcv_data):
        """Test _merge_indicator_result with Series result"""
        from src.vnstock_mcp.libs.ta_utils import _merge_indicator_result
        
        data = sample_ohlcv_data.copy()
        series_result = pd.Series([1.0] * len(data), name='RSI_14')
        
        result = _merge_indicator_result(data, series_result)
        
        assert 'RSI' in result.columns
        assert len(result) == len(data)
    
    @pytest.mark.unit
    def test_merge_indicator_result_with_rename_map(self, sample_ohlcv_data):
        """Test _merge_indicator_result with rename_map"""
        from src.vnstock_mcp.libs.ta_utils import _merge_indicator_result
        
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
        from src.vnstock_mcp.libs.ta_utils import _merge_indicator_result
        
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
        from src.vnstock_mcp.libs.ta_utils import _get_indicator_params, add_relative_strength_index
        
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
        from src.vnstock_mcp.libs.ta_utils import _get_indicator_description, add_relative_strength_index
        
        description = _get_indicator_description(add_relative_strength_index)
        
        assert isinstance(description, str)
        assert len(description) > 0
        assert 'relative strength index' in description.lower()
    
    @pytest.mark.unit
    def test_get_indicator_description_no_docstring(self):
        """Test _get_indicator_description with function without docstring"""
        from src.vnstock_mcp.libs.ta_utils import _get_indicator_description
        
        def no_doc_func(data):
            pass
        
        description = _get_indicator_description(no_doc_func)
        assert description == ""
    
    @pytest.mark.unit
    def test_get_indicator_output_columns(self):
        """Test _get_indicator_output_columns function"""
        from src.vnstock_mcp.libs.ta_utils import _get_indicator_output_columns, add_relative_strength_index, add_moving_average_convergence_divergence
        
        # Single column indicator
        rsi_cols = _get_indicator_output_columns(add_relative_strength_index)
        assert 'RSI' in rsi_cols
        
        # Multi-column indicator
        macd_cols = _get_indicator_output_columns(add_moving_average_convergence_divergence)
        assert 'MACD' in macd_cols
    
    @pytest.mark.unit
    def test_get_indicator_output_columns_no_docstring(self):
        """Test _get_indicator_output_columns with function without docstring"""
        from src.vnstock_mcp.libs.ta_utils import _get_indicator_output_columns
        
        def no_doc_func(data):
            pass
        
        cols = _get_indicator_output_columns(no_doc_func)
        assert cols == []
    
    @pytest.mark.unit
    def test_get_indicator_info(self):
        """Test get_indicator_info function"""
        from src.vnstock_mcp.libs.ta_utils import get_indicator_info
        
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
        from src.vnstock_mcp.libs.ta_utils import get_indicator_info
        
        with pytest.raises(ValueError) as excinfo:
            get_indicator_info('unknown_indicator')
        
        assert 'Unknown indicator' in str(excinfo.value)
    
    @pytest.mark.unit
    def test_get_available_indicators_simple(self):
        """Test get_available_indicators without detailed info"""
        from src.vnstock_mcp.libs.ta_utils import get_available_indicators
        
        indicators = get_available_indicators(detailed=False)
        
        assert isinstance(indicators, list)
        assert len(indicators) > 0
        assert 'rsi' in indicators
        assert 'macd' in indicators
    
    @pytest.mark.unit
    def test_get_available_indicators_detailed(self):
        """Test get_available_indicators with detailed info"""
        from src.vnstock_mcp.libs.ta_utils import get_available_indicators
        
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
        from src.vnstock_mcp.libs.ta_utils import _parse_indicator_string
        
        name, kwargs = _parse_indicator_string('rsi')
        assert name == 'rsi'
        assert kwargs == {}
        
        name, kwargs = _parse_indicator_string('macd')
        assert name == 'macd'
        assert kwargs == {}
    
    @pytest.mark.unit
    def test_parse_indicator_with_single_param(self):
        """Test parsing indicator with single parameter"""
        from src.vnstock_mcp.libs.ta_utils import _parse_indicator_string
        
        name, kwargs = _parse_indicator_string('rsi(window=21)')
        assert name == 'rsi'
        assert kwargs == {'window': 21}
    
    @pytest.mark.unit
    def test_parse_indicator_with_multiple_params(self):
        """Test parsing indicator with multiple parameters"""
        from src.vnstock_mcp.libs.ta_utils import _parse_indicator_string
        
        name, kwargs = _parse_indicator_string('macd(fast=12, slow=26, signal=9)')
        assert name == 'macd'
        assert kwargs == {'fast': 12, 'slow': 26, 'signal': 9}
    
    @pytest.mark.unit
    def test_parse_indicator_with_float_params(self):
        """Test parsing indicator with float parameters"""
        from src.vnstock_mcp.libs.ta_utils import _parse_indicator_string
        
        name, kwargs = _parse_indicator_string('cci(window=14, scalar=0.015)')
        assert name == 'cci'
        assert kwargs['window'] == 14
        assert kwargs['scalar'] == 0.015
    
    @pytest.mark.unit
    def test_parse_indicator_with_spaces(self):
        """Test parsing indicator with extra spaces"""
        from src.vnstock_mcp.libs.ta_utils import _parse_indicator_string
        
        name, kwargs = _parse_indicator_string('  rsi( window = 14 )  ')
        assert name == 'rsi'
        assert kwargs == {'window': 14}


class TestAddIndicator:
    """Test suite for add_indicator function"""
    
    @pytest.mark.unit
    def test_add_indicator_simple(self, sample_ohlcv_data):
        """Test add_indicator with simple indicator name"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_with_kwargs(self, sample_ohlcv_data):
        """Test add_indicator with explicit kwargs"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi', window=21)
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_with_string_params(self, sample_ohlcv_data):
        """Test add_indicator with parameters in string"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'rsi(window=21)')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_kwargs_override_string_params(self, sample_ohlcv_data):
        """Test that explicit kwargs override string parameters"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        # String has window=21, but explicit kwarg has window=7
        result = add_indicator(data, 'rsi(window=21)', window=7)
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_unknown(self, sample_ohlcv_data):
        """Test add_indicator with unknown indicator"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        
        with pytest.raises(ValueError) as excinfo:
            add_indicator(data, 'unknown_indicator')
        
        assert 'Unknown indicator' in str(excinfo.value)
    
    @pytest.mark.unit
    def test_add_indicator_case_insensitive(self, sample_ohlcv_data):
        """Test add_indicator is case insensitive"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'RSI')
        
        assert 'RSI' in result.columns
    
    @pytest.mark.unit
    def test_add_indicator_macd_with_params(self, sample_ohlcv_data):
        """Test add_indicator with MACD and custom parameters"""
        from src.vnstock_mcp.libs.ta_utils import add_indicator
        
        data = sample_ohlcv_data.copy()
        result = add_indicator(data, 'macd(fast_length=12, slow_length=26, signal_length=9)')
        
        assert 'MACD' in result.columns
        assert 'MACDh' in result.columns
        assert 'MACDs' in result.columns
