"""
Technical Analysis Utilities.

This module provides a unified interface for all technical indicators.
Indicator implementations are organized in separate modules:
- ta_core.py: Core utility functions (shared across all modules)
- ta_momentum_utils.py: Momentum indicators (RSI, MACD, Stochastic, etc.)
- ta_trend_utils.py: Trend indicators (ADX, Aroon, etc.)
- ta_volume_utils.py: Volume indicators (OBV, CMF, MFI, etc.)

Import flow (one-way, no circular imports):
    ta_core.py
        ↓
    ta_momentum_utils.py, ta_trend_utils.py, ta_volume_utils.py
        ↓
    ta_utils.py (this file - unified interface)
"""
import pandas as pd
from typing import Any

# Import core utilities (re-export for backward compatibility)
from .ta_core import (
    _strip_numeric_suffix,
    _merge_indicator_result,
    _get_indicator_params,
    _get_indicator_description,
    _get_indicator_output_columns,
    _parse_indicator_string,
)

# Import indicator registries and all indicator functions from sub-modules
from .ta_momentum_utils import (
    MOMENTUM_INDICATOR_REGISTRY,
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

from .ta_trend_utils import (
    TREND_INDICATOR_REGISTRY,
    # Trend indicators
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
)

from .ta_volume_utils import (
    VOLUME_INDICATOR_REGISTRY,
    # Volume indicators
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
)


# =============================================================================
# INDICATOR REGISTRY (combined from all modules)
# =============================================================================

INDICATOR_REGISTRY: dict = {
    **MOMENTUM_INDICATOR_REGISTRY,
    **TREND_INDICATOR_REGISTRY,
    **VOLUME_INDICATOR_REGISTRY,
}


# =============================================================================
# PUBLIC API FUNCTIONS
# =============================================================================

def get_indicator_info(indicator: str) -> dict[str, Any]:
    """
    Get detailed information about a specific indicator.
    
    Args:
        indicator: Name of the indicator (case-insensitive)
    
    Returns:
        Dict with indicator information including:
        - name: Indicator name
        - description: Short description
        - parameters: List of parameters with name, default, and type
        - output_columns: List of column names that will be added
        - usage: Example usage string
    
    Raises:
        ValueError: If indicator is not found
    """
    indicator_lower = indicator.lower().strip()
    
    if indicator_lower not in INDICATOR_REGISTRY:
        available = ", ".join(sorted(set(INDICATOR_REGISTRY.keys())))
        raise ValueError(
            f"Unknown indicator: '{indicator}'. "
            f"Available indicators: {available}"
        )
    
    func = INDICATOR_REGISTRY[indicator_lower]
    params = _get_indicator_params(func)
    
    # Build usage example
    if params:
        param_examples = ", ".join([
            f"{p['name']}={p.get('default', '...')}" for p in params
        ])
        usage = f"{indicator_lower}({param_examples})"
    else:
        usage = indicator_lower
    
    return {
        "name": indicator_lower,
        "description": _get_indicator_description(func),
        "parameters": params,
        "output_columns": _get_indicator_output_columns(func),
        "usage": usage
    }


def get_available_indicators(detailed: bool = False) -> list[str] | list[dict[str, Any]]:
    """
    Get list of available indicators with optional detailed information.
    
    Args:
        detailed: If True, returns detailed info for each indicator.
                  If False, returns just the list of names.
    
    Returns:
        If detailed=False: List of indicator names
        If detailed=True: List of dicts with indicator info including:
            - name: Indicator name (short form)
            - description: Short description
            - parameters: List of {name, default, type}
            - output_columns: Columns that will be added to DataFrame
            - usage: Example usage string
    
    Examples:
        >>> get_available_indicators()
        ['ao', 'apo', 'bias', 'bop', ...]
        
        >>> get_available_indicators(detailed=True)
        [
            {
                "name": "rsi",
                "description": "Add relative strength index to the data.",
                "parameters": [{"name": "window", "default": 14, "type": "int"}, ...],
                "output_columns": ["RSI"],
                "usage": "rsi(window=14, scalar=100)"
            },
            ...
        ]
    """
    if not detailed:
        return sorted(set(INDICATOR_REGISTRY.keys()))
    
    # Get unique functions (avoid duplicates from aliases)
    seen_funcs = set()
    indicators_info = []
    
    for name in sorted(INDICATOR_REGISTRY.keys()):
        func = INDICATOR_REGISTRY[name]
        
        # Skip if we've already processed this function (alias)
        if id(func) in seen_funcs:
            continue
        seen_funcs.add(id(func))
        
        try:
            info = get_indicator_info(name)
            indicators_info.append(info)
        except Exception:
            # Skip if there's an error getting info
            continue
    
    return indicators_info


def add_indicator(data: pd.DataFrame, indicator: str, **kwargs) -> pd.DataFrame:
    """
    Add an indicator to the data by name.
    
    Supports two ways to pass parameters:
    1. Via kwargs: add_indicator(data, "rsi", window=21)
    2. Via string: add_indicator(data, "rsi(window=21)")
    
    Args:
        data: pd.DataFrame (data to add indicator to)
        indicator: str (name of the indicator, case-insensitive, with optional params)
        **kwargs: Additional arguments to pass to the indicator function
    
    Returns:
        pd.DataFrame with indicator added
    
    Raises:
        ValueError: If indicator name is not recognized
    
    Examples:
        >>> data = add_indicator(data, "rsi")
        >>> data = add_indicator(data, "rsi(window=21)")
        >>> data = add_indicator(data, "macd(fast=12, slow=26, signal=9)")
        >>> data = add_indicator(data, "stochastic", k=14, d=3)
    """
    # Parse indicator string for embedded parameters
    indicator_name, parsed_kwargs = _parse_indicator_string(indicator)
    
    # Merge parsed kwargs with explicit kwargs (explicit takes precedence)
    merged_kwargs = {**parsed_kwargs, **kwargs}
    
    indicator_lower = indicator_name.lower().strip()
    
    if indicator_lower not in INDICATOR_REGISTRY:
        available = ", ".join(sorted(set(INDICATOR_REGISTRY.keys())))
        raise ValueError(
            f"Unknown indicator: '{indicator_name}'. "
            f"Available indicators: {available}"
        )
    
    indicator_func = INDICATOR_REGISTRY[indicator_lower]
    return indicator_func(data, **merged_kwargs)
