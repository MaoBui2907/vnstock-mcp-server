"""
Core utility functions for Technical Analysis.

This module contains shared utility functions used by all indicator modules.
These are the foundational functions that should be imported by other ta_* modules.
"""
import pandas as pd
import re
import inspect
from typing import Any


def _strip_numeric_suffix(col_name: str) -> str:
    """
    Remove numeric suffix from column name.
    Examples:
        'MACD_12_26_9' -> 'MACD'
        'MACDh_12_26_9' -> 'MACDh'
        'STOCHk_14_3_3' -> 'STOCHk'
        'SQZ_ON' -> 'SQZ_ON' (no numeric suffix)
    """
    # Match pattern: name followed by underscore and numbers (with possible dots)
    # Keep the base name part
    match = re.match(r'^([A-Za-z_]+?)(?:_[\d._]+)?$', col_name)
    if match:
        return match.group(1).rstrip('_')
    return col_name


def _merge_indicator_result(data: pd.DataFrame, result, rename_map: dict = None, fillna_value: float = 0) -> pd.DataFrame:
    """
    Merge indicator result into data DataFrame.
    
    Args:
        data: Original DataFrame
        result: Result from pandas_ta (Series or DataFrame)
        rename_map: Optional dict to rename columns {old_name_pattern: new_name}
        fillna_value: Value to fill NaN with (default: 0)
    
    Returns:
        DataFrame with indicator columns added (NaN values filled with fillna_value)
    """
    if result is None:
        return data
    
    if isinstance(result, pd.Series):
        # Single column result
        name = _strip_numeric_suffix(result.name) if result.name else 'indicator'
        data[name] = result.fillna(fillna_value)
    elif isinstance(result, pd.DataFrame):
        # Multi-column result
        for col in result.columns:
            new_name = _strip_numeric_suffix(col)
            if rename_map and col in rename_map:
                new_name = rename_map[col]
            data[new_name] = result[col].fillna(fillna_value)
    
    return data


def _get_indicator_params(func) -> list[dict[str, Any]]:
    """
    Extract parameter information from an indicator function.
    
    Args:
        func: The indicator function
    
    Returns:
        List of parameter info dicts with name, default, and type
    """
    sig = inspect.signature(func)
    params = []
    
    for name, param in sig.parameters.items():
        # Skip 'data' parameter as it's always the DataFrame
        if name == 'data':
            continue
        
        param_info = {"name": name}
        
        # Get default value
        if param.default is not inspect.Parameter.empty:
            param_info["default"] = param.default
        
        # Get type annotation if available
        if param.annotation is not inspect.Parameter.empty:
            param_info["type"] = param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation)
        
        params.append(param_info)
    
    return params


def _get_indicator_description(func) -> str:
    """
    Extract short description from indicator function docstring.
    
    Args:
        func: The indicator function
    
    Returns:
        Short description string
    """
    if not func.__doc__:
        return ""
    
    # Get first non-empty line of docstring
    lines = func.__doc__.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('Output') and not line.startswith('Args'):
            return line
    return ""


def _get_indicator_output_columns(func) -> list[str]:
    """
    Extract output column names from indicator function docstring.
    
    Args:
        func: The indicator function
    
    Returns:
        List of output column names
    """
    if not func.__doc__:
        return []
    
    # Look for "Output columns:" line
    lines = func.__doc__.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('Output columns:'):
            # Extract column names after the colon
            cols_str = line.replace('Output columns:', '').strip()
            # Parse columns like "MACD, MACDh, MACDs" or "RSI"
            cols = [c.strip().split()[0] for c in cols_str.split(',')]
            return cols
    return []


def _parse_indicator_string(indicator_str: str) -> tuple[str, dict]:
    """
    Parse indicator string with optional parameters.
    
    Supports formats:
        - "rsi" -> ("rsi", {})
        - "rsi(14)" -> ("rsi", {"window": 14})  # positional not supported, use named
        - "rsi(window=14)" -> ("rsi", {"window": 14})
        - "macd(fast=12, slow=26)" -> ("macd", {"fast": 12, "slow": 26})
        - "stochastic(k=14, d=3, smooth_k=3)" -> ("stochastic", {"k": 14, "d": 3, "smooth_k": 3})
    
    Args:
        indicator_str: Indicator string with optional parameters
    
    Returns:
        Tuple of (indicator_name, kwargs_dict)
    """
    indicator_str = indicator_str.strip()
    
    # Check if there are parameters
    match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.+)\)\s*$', indicator_str)
    
    if not match:
        # No parameters, just indicator name
        return indicator_str, {}
    
    indicator_name = match.group(1)
    params_str = match.group(2).strip()
    
    kwargs = {}
    
    # Parse key=value pairs
    # Handle: window=14, fast=12.5, smooth_k=3
    param_pattern = re.compile(r'([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([^,]+)')
    
    for param_match in param_pattern.finditer(params_str):
        key = param_match.group(1).strip()
        value_str = param_match.group(2).strip()
        
        # Try to convert value to appropriate type
        try:
            # Try int first
            if '.' not in value_str:
                value = int(value_str)
            else:
                value = float(value_str)
        except ValueError:
            # Keep as string if not a number
            value = value_str.strip('"\'')
        
        kwargs[key] = value
    
    return indicator_name, kwargs

