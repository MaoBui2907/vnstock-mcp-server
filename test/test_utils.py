"""
Test suite for utils.py - Output format utilities
"""

import pytest
import pandas as pd
from typing import Literal
from unittest.mock import Mock
from src.vnstock_mcp.libs.utils import convert_output, with_output_format, tool_with_format


class TestConvertOutput:
    """Test suite for convert_output function"""
    
    @pytest.mark.unit
    def test_convert_dataframe_to_json(self):
        """Test converting DataFrame to JSON"""
        df = pd.DataFrame([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}])
        result = convert_output(df, 'json')
        
        assert isinstance(result, str)
        assert '"a":1' in result or '"a": 1' in result
    
    @pytest.mark.unit
    def test_convert_series_to_json(self):
        """Test converting Series to JSON"""
        series = pd.Series([1, 2, 3], name='test')
        result = convert_output(series, 'json')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_dict_to_json(self):
        """Test converting dict to JSON"""
        data = {'key1': 'value1', 'key2': 'value2'}
        result = convert_output(data, 'json')
        
        assert isinstance(result, str)
        assert 'key1' in result
    
    @pytest.mark.unit
    def test_convert_list_to_json(self):
        """Test converting list to JSON"""
        data = [{'a': 1}, {'a': 2}]
        result = convert_output(data, 'json')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_primitive_to_json(self):
        """Test converting primitive to JSON"""
        result = convert_output("test string", 'json')
        assert result == "test string"
        
        result = convert_output(123, 'json')
        assert result == 123
    
    @pytest.mark.unit
    def test_convert_dataframe_to_toon(self):
        """Test converting DataFrame to TOON format"""
        df = pd.DataFrame([{'a': 1, 'b': 2}])
        result = convert_output(df, 'toon')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_series_to_toon(self):
        """Test converting Series to TOON format"""
        series = pd.Series([1, 2, 3], name='test')
        result = convert_output(series, 'toon')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_dict_to_toon(self):
        """Test converting dict to TOON format"""
        data = {'key1': 'value1', 'key2': 'value2'}
        result = convert_output(data, 'toon')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_list_to_toon(self):
        """Test converting list to TOON format"""
        data = [{'a': 1}, {'a': 2}]
        result = convert_output(data, 'toon')
        
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_primitive_to_toon(self):
        """Test converting primitive to TOON format"""
        result = convert_output("test", 'toon')
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_convert_dataframe_output_unchanged(self):
        """Test that dataframe format returns DataFrame unchanged"""
        df = pd.DataFrame([{'a': 1}])
        result = convert_output(df, 'dataframe')
        
        assert isinstance(result, pd.DataFrame)
        assert result.equals(df)


class TestWithOutputFormat:
    """Test suite for with_output_format decorator"""
    
    @pytest.mark.unit
    def test_decorator_adds_output_format_param(self):
        """Test that decorator adds output_format parameter"""
        @with_output_format
        def my_func(x: int) -> pd.DataFrame:
            """Test function."""
            return pd.DataFrame([{'x': x}])
        
        # Check signature includes output_format
        import inspect
        sig = inspect.signature(my_func)
        assert 'output_format' in sig.parameters
    
    @pytest.mark.unit
    def test_decorator_default_format_is_toon(self):
        """Test that default output_format is 'toon'"""
        @with_output_format
        def my_func() -> pd.DataFrame:
            """Test function."""
            return pd.DataFrame([{'a': 1}])
        
        import inspect
        sig = inspect.signature(my_func)
        assert sig.parameters['output_format'].default == 'toon'
    
    @pytest.mark.unit
    def test_decorator_respects_output_format(self):
        """Test that decorator converts output based on format"""
        @with_output_format
        def my_func() -> pd.DataFrame:
            """Test function."""
            return pd.DataFrame([{'a': 1}])
        
        # Test JSON
        result = my_func(output_format='json')
        assert isinstance(result, str)
        
        # Test DataFrame
        result = my_func(output_format='dataframe')
        assert isinstance(result, pd.DataFrame)
        
        # Test TOON
        result = my_func(output_format='toon')
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_decorator_preserves_function_name(self):
        """Test that decorator preserves function name"""
        @with_output_format
        def my_test_func():
            """My docstring."""
            return pd.DataFrame()
        
        assert my_test_func.__name__ == 'my_test_func'
    
    @pytest.mark.unit
    def test_decorator_with_function_already_has_output_format(self):
        """Test decorator when function already has output_format parameter"""
        @with_output_format
        def my_func(output_format: Literal['json', 'dataframe'] = 'json'):
            """Test function."""
            return pd.DataFrame([{'a': 1}])
        
        # Should still work
        result = my_func(output_format='dataframe')
        assert isinstance(result, pd.DataFrame)
    
    @pytest.mark.unit
    def test_decorator_with_function_without_annotations(self):
        """Test decorator with function that has no annotations"""
        def no_annotations_func():
            """Test function."""
            return pd.DataFrame([{'a': 1}])
        
        # Remove annotations if any
        if hasattr(no_annotations_func, '__annotations__'):
            delattr(no_annotations_func, '__annotations__')
        
        decorated = with_output_format(no_annotations_func)
        result = decorated(output_format='json')
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_decorator_updates_docstring_with_args(self):
        """Test that decorator updates docstring when Args section exists"""
        @with_output_format
        def my_func(x: int):
            """
            My function description.
            
            Args:
                x: int value
            Returns:
                DataFrame
            """
            return pd.DataFrame([{'x': x}])
        
        assert 'output_format' in my_func.__doc__
    
    @pytest.mark.unit
    def test_decorator_updates_docstring_args_no_returns(self):
        """Test decorator updates docstring when Args exists but no Returns"""
        @with_output_format
        def my_func(x: int):
            """
            My function description.
            
            Args:
                x: int value
            """
            return pd.DataFrame([{'x': x}])
        
        assert 'output_format' in my_func.__doc__
    
    @pytest.mark.unit
    def test_decorator_updates_docstring_no_args_no_returns(self):
        """Test decorator updates docstring when neither Args nor Returns exist"""
        @with_output_format
        def my_func():
            """My function description."""
            return pd.DataFrame([{'a': 1}])
        
        assert 'output_format' in my_func.__doc__
    
    @pytest.mark.unit
    def test_decorator_no_docstring(self):
        """Test decorator with function without docstring"""
        @with_output_format
        def my_func():
            return pd.DataFrame([{'a': 1}])
        
        result = my_func(output_format='json')
        assert isinstance(result, str)
    
    @pytest.mark.unit
    def test_decorator_with_args_and_kwargs(self):
        """Test decorator with function that has args and kwargs"""
        @with_output_format
        def my_func(a: int, b: str = 'default'):
            """Test function.
            
            Args:
                a: first arg
                b: second arg
            Returns:
                DataFrame
            """
            return pd.DataFrame([{'a': a, 'b': b}])
        
        result = my_func(1, 'test', output_format='dataframe')
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[0]['a'] == 1
        assert result.iloc[0]['b'] == 'test'


class TestToolWithFormat:
    """Test suite for tool_with_format decorator"""
    
    @pytest.mark.unit
    def test_tool_with_format_basic(self):
        """Test basic tool_with_format functionality"""
        # Mock MCP instance
        mock_mcp = Mock()
        mock_mcp.tool = lambda func: func  # Simple pass-through
        
        @tool_with_format(mock_mcp)
        def my_tool(symbol: str):
            """Get data for symbol."""
            return pd.DataFrame([{'symbol': symbol}])
        
        # Test that it works
        result = my_tool('VCB', output_format='dataframe')
        assert isinstance(result, pd.DataFrame)
        assert result.iloc[0]['symbol'] == 'VCB'
    
    @pytest.mark.unit
    def test_tool_with_format_output_formats(self):
        """Test tool_with_format with different output formats"""
        # Mock MCP instance
        mock_mcp = Mock()
        mock_mcp.tool = lambda func: func
        
        @tool_with_format(mock_mcp)
        def my_tool():
            """Get data."""
            return pd.DataFrame([{'a': 1}])
        
        # JSON
        result = my_tool(output_format='json')
        assert isinstance(result, str)
        
        # DataFrame
        result = my_tool(output_format='dataframe')
        assert isinstance(result, pd.DataFrame)
        
        # TOON
        result = my_tool(output_format='toon')
        assert isinstance(result, str)

