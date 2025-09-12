# VNStock MCP Server - Testing Documentation

This directory contains comprehensive unit tests for all VNStock MCP Server tools.

## Test Structure

```
test/
├── conftest.py              # Pytest configuration and shared fixtures
├── test_company_tools.py    # Tests for company-related tools (11 tools)
├── test_listing_tools.py    # Tests for listing-related tools (5 tools)
├── test_finance_tools.py    # Tests for finance-related tools (5 tools)
├── test_fund_tools.py       # Tests for fund-related tools (5 tools)
├── test_misc_tools.py       # Tests for misc tools (2 tools)
├── test_quote_tools.py      # Tests for quote-related tools (3 tools)
├── test_trading_tools.py    # Tests for trading tools (1 tool)
└── README.md               # This file
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
- `get_all_industries`
- `get_all_symbols_by_group`
- `get_all_symbols_by_industry`
- `get_all_symbols`

### Finance Tools (5 tools)
- `get_income_statements`
- `get_balance_sheets`
- `get_cash_flows`
- `get_finance_ratios`
- `get_raw_report`

### Fund Tools (5 tools)
- `list_all_funds`
- `search_fund`
- `get_fund_nav_report`
- `get_fund_top_holding`
- `get_fund_industry_holding`
- `get_fund_asset_holding`

### Misc Tools (2 tools)
- `get_gold_price`
- `get_exchange_rate`

### Quote Tools (3 tools)
- `get_quote_history_price`
- `get_quote_intraday_price`
- `get_quote_price_depth`

### Trading Tools (1 tool)
- `get_price_board`

**Total: 32 tools tested**

## Test Features

### Comprehensive Coverage
- ✅ **Unit Tests**: All 32 tools have comprehensive unit tests
- ✅ **Mock Testing**: All external API calls are mocked
- ✅ **Output Format Testing**: Both JSON and DataFrame outputs tested
- ✅ **Parameter Testing**: Default parameters and edge cases
- ✅ **Error Handling**: Exception handling and empty result scenarios
- ✅ **Data Validation**: Response structure and data integrity

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
make install-dev
# or
pdm install --dev
```

### Basic Test Commands
```bash
# Run all tests
make test

# Run tests with verbose output
make test-verbose

# Run only unit tests
make test-unit

# Run tests with coverage report
make test-coverage
```

### Specific Test Files
```bash
# Test company tools only
make test-company

# Test listing tools only
make test-listing

# Test finance tools only
make test-finance

# Test fund tools only
make test-fund

# Test misc tools only
make test-misc

# Test quote tools only
make test-quote

# Test trading tools only
make test-trading
```

### Advanced Test Commands
```bash
# Run specific test function
make test-function FUNC=test_get_company_overview_json

# Run tests in parallel
make test-parallel

# Run tests with file watching
make test-watch

# Generate coverage report
make coverage
```

### Direct pytest Commands
```bash
# Run all tests
pdm run pytest

# Run specific test file
pdm run pytest test/test_company_tools.py

# Run specific test class
pdm run pytest test/test_company_tools.py::TestCompanyTools

# Run specific test method
pdm run pytest test/test_company_tools.py::TestCompanyTools::test_get_company_overview_json

# Run tests with specific marker
pdm run pytest -m unit

# Run tests with coverage
pdm run pytest --cov=src/vnstock_mcp --cov-report=html
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

## Known Issues and Bugs

### Documented Bugs in Code
1. **get_cash_flows function**: Does not respect `output_format` parameter
   - Always returns DataFrame regardless of output_format
   - Test documents this behavior for future fixing

### Test Coverage
- **Current Coverage**: ~95%+ (target)
- **Missing Coverage**: Error handling in some edge cases
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
make coverage

# Clean up test artifacts
make clean

# Lint test code (if linting tools are installed)
make lint-tests
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
