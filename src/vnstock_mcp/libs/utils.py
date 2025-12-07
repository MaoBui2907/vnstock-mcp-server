import functools
import inspect
from typing import Literal, Callable, Any
import pandas as pd
from toon import encode as toon_encode


# Type for output format
OutputFormat = Literal['json', 'dataframe', 'toon']


def convert_output(data: Any, output_format: OutputFormat = 'toon') -> Any:
    """
    Convert output data to the specified format.
    
    Args:
        data: The data to convert (typically a DataFrame)
        output_format: The format to convert to ('json', 'dataframe', or 'toon')
    
    Returns:
        Converted data in the specified format
    """
    if output_format == 'json':
        if isinstance(data, pd.DataFrame):
            return data.to_json(orient='records', force_ascii=False)
        elif isinstance(data, pd.Series):
            return data.to_json(force_ascii=False)
        elif isinstance(data, dict):
            return pd.DataFrame([data]).to_json(orient='records', force_ascii=False)
        elif isinstance(data, list):
            return pd.DataFrame(data).to_json(orient='records', force_ascii=False)
        else:
            return data
    elif output_format == 'toon':
        # Convert to TOON format (Token-Oriented Object Notation)
        # TOON is optimized for LLMs, reducing token count
        if isinstance(data, pd.DataFrame):
            # Convert DataFrame to list of dicts, then encode to TOON
            return toon_encode(data.to_dict(orient='records'))
        elif isinstance(data, pd.Series):
            return toon_encode(data.to_dict())
        elif isinstance(data, (dict, list)):
            return toon_encode(data)
        else:
            return toon_encode(data)
    else:
        # Return dataframe as-is
        return data


def with_output_format(func: Callable) -> Callable:
    """
    Decorator that adds output_format parameter to a tool function and 
    automatically converts the output to the specified format.
    
    This decorator:
    1. Adds `output_format: Literal['json', 'dataframe', 'toon'] = 'toon'` parameter
    2. Automatically converts DataFrame output based on output_format:
       - 'json': Standard JSON format
       - 'dataframe': Raw DataFrame (for programmatic use)
       - 'toon': Token-Oriented Object Notation (optimized for LLMs)
    
    Usage:
        @mcp.tool
        @with_output_format
        def my_tool(symbol: str):
            '''My tool description'''
            return some_dataframe
    
    The decorated function will have output_format parameter available and
    the output will be automatically converted based on the format.
    """
    # Get original signature
    original_sig = inspect.signature(func)
    original_params = list(original_sig.parameters.values())
    
    # Create new output_format parameter with 'toon' as default (best for AI)
    output_format_param = inspect.Parameter(
        'output_format',
        inspect.Parameter.KEYWORD_ONLY,
        default='toon',
        annotation=Literal['json', 'dataframe', 'toon']
    )
    
    # Check if output_format already exists in the function
    has_output_format = 'output_format' in original_sig.parameters
    
    if not has_output_format:
        # Add output_format parameter at the end
        new_params = original_params + [output_format_param]
        new_sig = original_sig.replace(parameters=new_params)
    else:
        new_sig = original_sig
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Extract output_format from kwargs, default to 'toon' (best for AI)
        output_format = kwargs.pop('output_format', 'toon')
        
        # Call original function
        result = func(*args, **kwargs)
        
        # Convert output based on format
        return convert_output(result, output_format)
    
    # Update wrapper signature
    wrapper.__signature__ = new_sig  # type: ignore
    
    # Update annotations to include output_format
    if hasattr(func, '__annotations__'):
        wrapper.__annotations__ = func.__annotations__.copy()
    else:
        wrapper.__annotations__ = {}
    wrapper.__annotations__['output_format'] = Literal['json', 'dataframe', 'toon']
    
    # Update docstring to include output_format parameter
    if func.__doc__:
        doc_lines = func.__doc__.split('\n')
        new_doc_lines = []
        args_found = False
        args_indent = 4  # Default indent for section headers (Args:, Returns:)
        param_indent = 8  # Default indent for parameters
        returns_line_idx = -1
        
        # First pass: find Args section and Returns line index
        for i, line in enumerate(doc_lines):
            if 'Args:' in line:
                args_found = True
                args_indent = len(line) - len(line.lstrip())
                param_indent = args_indent + 4
            if 'Returns:' in line:
                returns_line_idx = i
        
        output_format_doc = ' ' * param_indent + "output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)"
        
        # Second pass: build new docstring
        for i, line in enumerate(doc_lines):
            if args_found:
                # Has Args section: insert output_format before Returns
                if i == returns_line_idx:
                    new_doc_lines.append(output_format_doc)
                new_doc_lines.append(line)
            else:
                # No Args section: insert Args + output_format before Returns
                if i == returns_line_idx:
                    new_doc_lines.append(' ' * args_indent + "Args:")
                    new_doc_lines.append(output_format_doc)
                new_doc_lines.append(line)
        
        # If Args exists but no Returns, append output_format at the end
        if args_found and returns_line_idx == -1:
            new_doc_lines.append(output_format_doc)
        
        # If neither Args nor Returns exist, append both at the end
        if not args_found and returns_line_idx == -1:
            new_doc_lines.append(' ' * args_indent + "Args:")
            new_doc_lines.append(output_format_doc)
        
        wrapper.__doc__ = '\n'.join(new_doc_lines)
    
    return wrapper


def tool_with_format(mcp_instance):
    """
    Creates a decorator that combines @mcp.tool with @with_output_format.
    
    Usage:
        @tool_with_format(mcp)
        def my_tool(symbol: str):
            '''My tool description'''
            return some_dataframe
    
    This is equivalent to:
        @mcp.tool
        @with_output_format
        def my_tool(symbol: str):
            '''My tool description'''
            return some_dataframe
    """
    def decorator(func: Callable) -> Callable:
        # First apply with_output_format, then mcp.tool
        formatted_func = with_output_format(func)
        return mcp_instance.tool(formatted_func)
    
    return decorator
