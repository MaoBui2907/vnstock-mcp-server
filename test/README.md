# VNStock MCP Server - Testing Documentation

This directory contains comprehensive unit tests for all VNStock MCP Server tools.

## Test Structure

```
test/
├── conftest.py                  # Pytest configuration and shared fixtures
├── test_cli.py                  # Tests for CLI and server startup
├── test_company_tools.py        # Tests for company-related tools (11 tools)
├── test_finance_tools.py        # Tests for finance-related tools (5 tools)
├── test_fund_tools.py           # Tests for fund-related tools (6 tools)
├── test_listing_tools.py        # Tests for listing-related tools (5 tools)
├── test_misc_tools.py           # Tests for misc tools (2 tools)
├── test_quote_tools.py          # Tests for quote-related tools (4 tools)
├── test_ta_momentum_utils.py    # Tests for TA momentum indicators (40+ indicators)
├── test_ta_trend_utils.py       # Tests for TA trend indicators (15+ indicators)
├── test_ta_volume_utils.py      # Tests for TA volume indicators (15+ indicators)
├── test_ta_utils.py             # Tests for TA utility functions and registry
├── test_trading_tools.py        # Tests for trading tools (1 tool)
├── test_utils.py                # Tests for utility functions
├── test_vnstock_utils.py        # Tests for vnstock utility functions
└── README.md                    # This file
```

## Tools Covered

### Company Tools (11 tools)
- `get_company_overview`
- `get_company_news`
- `get_company_events`
- `get_company_shareholders`
- `get_company_officers`
- `get_company_subsidiaries`
- `get_company_reports`
- `get_company_dividends`
- `get_company_insider_deals`
- `get_company_ratio_summary`
- `get_company_trading_stats`

### Listing Tools (5 tools)
- `get_all_symbol_groups`
- `get_all_symbols_by_group`
- `get_all_symbols_by_industry`
- `get_all_symbols`
- `get_all_industries`

### Finance Tools (5 tools)
- `get_income_statements`
- `get_balance_sheets`
- `get_cash_flows`
- `get_finance_ratios`
- `get_raw_report`

### Fund Tools (6 tools)
- `list_all_funds`
- `search_fund`
- `get_fund_nav_report`
- `get_fund_top_holding`
- `get_fund_industry_holding`
- `get_fund_asset_holding`

### Misc Tools (2 tools)
- `get_gold_price`
- `get_exchange_rate`

### Quote Tools (4 tools)
- `get_quote_history_price`
- `get_quote_intraday_price`
- `get_quote_price_depth`
- `get_quote_price_with_indicators`

### Trading Tools (1 tool)
- `get_price_board`

### Technical Analysis (TA) Tools

#### Momentum Indicators (40+ indicators)
- RSI, MACD, Stochastic, CCI, Williams %R, ADX
- Awesome Oscillator, APO, BIAS, BOP, BRAR
- CFO, CG, CMO, Coppock, CRSI, CTI, DM
- Efficiency Ratio, Elder Ray, Fisher Transform
- Inertia, KDJ, KST, Momentum, PGO, PPO, PSL
- QQE, ROC, RSX, RVGI, Slope, SMI, Squeeze
- STC, STOCH, STOCHF, STOCHRSI, TMO, TRIX, TSI
- Ultimate Oscillator, Williams %R

#### Trend Indicators (15+ indicators)
- ADX (Average Directional Movement)
- Aroon, Aroon Oscillator
- Choppiness Index, CKSp
- Decay, Decreasing/Increasing
- DPO (Detrended Price Oscillator)
- Ichimoku Cloud
- Linear Regression, PSAR (Parabolic SAR)
- QStick, SuperTrend, VHF, Vortex

#### Volume Indicators (15+ indicators)
- AD (Accumulation/Distribution)
- ADOSC (AD Oscillator)
- AOBV (Archer OBV)
- CMF (Chaikin Money Flow)
- EFI (Elder's Force Index)
- EOM (Ease of Movement)
- KVO (Klinger Volume Oscillator)
- MFI (Money Flow Index)
- NVI (Negative Volume Index)
- OBV (On-Balance Volume)
- PVO (Percentage Volume Oscillator)
- PVOL (Price-Volume)
- PVR (Price Volume Rank)
- PVT (Price Volume Trend)
- VWMA (Volume Weighted Moving Average)

**Total: 35+ tools + 70+ technical indicators tested**

## Test Features

### Comprehensive Coverage
- ✅ **Unit Tests**: All tools have comprehensive unit tests
- ✅ **Mock Testing**: All external API calls are mocked
- ✅ **Output Format Testing**: Both JSON and DataFrame outputs tested
- ✅ **Parameter Testing**: Default parameters and edge cases
- ✅ **Error Handling**: Exception handling and empty result scenarios
- ✅ **Data Validation**: Response structure and data integrity
- ✅ **TA Indicators**: Output columns verification and parameter variations

### Test Categories
- **Unit Tests**: Fast, isolated tests with mocked dependencies
- **Integration Tests**: (Placeholder for future real API tests)
- **Slow Tests**: Tests that make actual external API calls (marked as slow)

### Mock Strategy
- All external vnstock classes are mocked (TCBSCompany, VCICompany, etc.)
- Sample data fixtures provide realistic test data
- Mock functions return consistent, predictable data
- No real API calls during testing

## Running Tests

### Prerequisites
```bash
# Install development dependencies
pdm install --dev
# or with uv
uv sync --group dev
```

### Basic Test Commands
```bash
# Run all tests
pdm run pytest

# Run tests with verbose output
pdm run pytest -v

# Run only unit tests
pdm run pytest -m unit

# Run tests with coverage report
pdm run pytest --cov=src/vnstock_mcp --cov-report=html
```

### Specific Test Files
```bash
# Test company tools only
pdm run pytest test/test_company_tools.py

# Test listing tools only
pdm run pytest test/test_listing_tools.py

# Test finance tools only
pdm run pytest test/test_finance_tools.py

# Test fund tools only
pdm run pytest test/test_fund_tools.py

# Test misc tools only
pdm run pytest test/test_misc_tools.py

# Test quote tools only
pdm run pytest test/test_quote_tools.py

# Test trading tools only
pdm run pytest test/test_trading_tools.py

# Test TA momentum indicators
pdm run pytest test/test_ta_momentum_utils.py

# Test TA trend indicators
pdm run pytest test/test_ta_trend_utils.py

# Test TA volume indicators
pdm run pytest test/test_ta_volume_utils.py

# Test TA utilities and registry
pdm run pytest test/test_ta_utils.py

# Test CLI
pdm run pytest test/test_cli.py
```

### Advanced Test Commands
```bash
# Run specific test function
pdm run pytest test/test_company_tools.py::TestCompanyTools::test_get_company_overview_json

# Run tests matching a pattern
pdm run pytest -k "rsi or macd"

# Run tests with short output
pdm run pytest --tb=short -q

# Run tests in parallel (requires pytest-xdist)
pdm run pytest -n auto

# Generate HTML coverage report
pdm run pytest --cov=src/vnstock_mcp --cov-report=html
# Open report: ./htmlcov/index.html
```

## Test Configuration

### Pytest Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["test"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--cov=src/vnstock_mcp",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--strict-markers",
    "-v"
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow tests that make external API calls"
]
```

### Coverage Configuration
```toml
[tool.coverage.run]
source = ["src/vnstock_mcp"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:"
]
```

## Fixtures and Mock Data

### Available Fixtures (conftest.py)
- `sample_company_overview_data`: Mock company overview data
- `sample_company_news_data`: Mock company news data
- `sample_company_events_data`: Mock company events data
- `sample_shareholders_data`: Mock shareholders data
- `sample_officers_data`: Mock officers data
- `sample_subsidiaries_data`: Mock subsidiaries data
- `sample_financial_data`: Mock financial statements data
- `sample_fund_data`: Mock fund data
- `sample_quote_history_data`: Mock quote history data
- `sample_gold_price_data`: Mock gold price data
- `sample_exchange_rate_data`: Mock exchange rate data
- `sample_industries_data`: Mock industries data
- `sample_symbols_data`: Mock symbols data
- `sample_ohlcv_data`: Mock OHLCV data for TA indicators

### Mock Classes
- `mock_tcbs_company`: Mock TCBS Company class
- `mock_vci_company`: Mock VCI Company class
- `mock_vci_listing`: Mock VCI Listing class
- `mock_vci_finance`: Mock VCI Finance class
- `mock_quote`: Mock Quote class
- `mock_fund`: Mock Fund class
- `mock_trading`: Mock Trading class

## Test Examples

### Basic Test Structure
```python
@pytest.mark.unit
@patch('src.vnstock_mcp.server.TCBSCompany')
def test_get_company_overview_json(self, mock_tcbs_class, sample_company_overview_data):
    """Test get_company_overview with JSON output"""
    # Setup mock
    mock_instance = Mock()
    mock_instance.overview.return_value = sample_company_overview_data
    mock_tcbs_class.return_value = mock_instance
    
    # Test
    result = get_company_overview('VCB', 'json')
    
    # Assertions
    mock_tcbs_class.assert_called_once_with(symbol='VCB')
    mock_instance.overview.assert_called_once()
    
    # Verify JSON output
    assert isinstance(result, str)
    parsed_result = json.loads(result)
    assert isinstance(parsed_result, list)
    assert len(parsed_result) == 1
    assert parsed_result[0]['symbol'] == 'VCB'
```

### Testing TA Indicators
```python
def test_add_rsi_default_params(self, sample_ohlcv_data):
    """Test RSI indicator with default parameters"""
    result = add_relative_strength_index(sample_ohlcv_data.copy())
    
    # Check output columns exist
    assert 'RSI_14' in result.columns
    
    # Check data integrity
    assert len(result) == len(sample_ohlcv_data)
    assert result['close'].equals(sample_ohlcv_data['close'])

def test_add_macd_custom_params(self, sample_ohlcv_data):
    """Test MACD indicator with custom parameters"""
    result = add_moving_average_convergence_divergence(
        sample_ohlcv_data.copy(),
        fast_length=8,
        slow_length=21,
        signal_length=5
    )
    
    # Check all output columns
    macd_cols = [col for col in result.columns if 'MACD' in col.upper()]
    assert len(macd_cols) >= 3  # MACD, MACDh, MACDs
```

### Testing Both Output Formats
```python
def test_tool_both_formats(self):
    """Test tool with both JSON and DataFrame outputs"""
    with patch('src.vnstock_mcp.server.SomeClass') as mock_class:
        mock_instance = Mock()
        mock_instance.method.return_value = sample_data
        mock_class.return_value = mock_instance
        
        # Test JSON format
        json_result = some_tool('param', 'json')
        assert isinstance(json_result, str)
        
        # Test DataFrame format
        df_result = some_tool('param', 'dataframe')
        assert isinstance(df_result, pd.DataFrame)
```

## Current Test Statistics

- **Total Tests**: 305
- **Coverage**: ~99%
- **Test Files**: 14

### Test Distribution
| Test File | Tests |
|-----------|-------|
| test_cli.py | 16 |
| test_company_tools.py | 19 |
| test_finance_tools.py | 16 |
| test_fund_tools.py | 18 |
| test_listing_tools.py | 15 |
| test_misc_tools.py | 18 |
| test_quote_tools.py | 23 |
| test_ta_momentum_utils.py | 48 |
| test_ta_trend_utils.py | 28 |
| test_ta_utils.py | 34 |
| test_ta_volume_utils.py | 26 |
| test_trading_tools.py | 15 |
| test_utils.py | 24 |
| test_vnstock_utils.py | 5 |

## Known Issues and Bugs

### Documented Bugs in Code
1. **get_cash_flows function**: Does not respect `output_format` parameter
   - Always returns DataFrame regardless of output_format
   - Test documents this behavior for future fixing

### Test Coverage
- **Current Coverage**: 99%
- **Missing Coverage**: Minor edge cases in error handling
- **Future Improvements**: Integration tests with real API calls

## Contributing

### Adding New Tests
1. Create test file following naming convention: `test_[category]_tools.py`
2. Use existing fixtures from `conftest.py`
3. Follow the established test patterns
4. Include both JSON and DataFrame output tests
5. Test error handling and edge cases
6. Add appropriate pytest markers

### Test Guidelines
- Use descriptive test names
- Test one thing per test function
- Use appropriate fixtures and mocks
- Include docstrings for complex tests
- Follow the AAA pattern (Arrange, Act, Assert)
- Mock all external dependencies

### Running Tests Before Commit
```bash
# Run full test suite with coverage
pdm run pytest --cov=src/vnstock_mcp --cov-report=html

# Quick test run
pdm run pytest --tb=short -q

# Lint test code (if linting tools are installed)
pdm run ruff check test/
```

## Maintenance

### Regular Tasks
- Update mock data when API responses change
- Add tests for new tools
- Review and update test coverage
- Update documentation

### Dependencies
- `pytest`: Test framework
- `pytest-mock`: Mocking utilities
- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support (future use)

## Support

For questions about testing:
1. Check this documentation
2. Review existing test examples
3. Check pytest documentation
4. Review mock data in `conftest.py`

The test suite is designed to be comprehensive, fast, and maintainable. All external API calls are mocked to ensure tests run quickly and reliably without depending on external services.
