import pytest
import sys
from unittest.mock import patch, MagicMock
from vnstock_mcp.server import main


class TestCLI:
    """Test cases for command line interface functionality."""
    
    @patch('vnstock_mcp.server.server')
    def test_main_default_arguments(self, mock_server):
        """Test main function with default arguments (stdio)."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(transport='stdio')
    
    @patch('vnstock_mcp.server.server')
    def test_main_stdio_transport(self, mock_server):
        """Test main function with explicit stdio transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'stdio']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(transport='stdio')
    
    @patch('vnstock_mcp.server.server')
    def test_main_sse_transport(self, mock_server):
        """Test main function with SSE transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='0.0.0.0',
            port=8000,
            path=None
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_sse_transport_with_path(self, mock_server):
        """Test main function with SSE transport and path."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse', '--path', '/vnstock']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='0.0.0.0',
            port=8000,
            path='/vnstock'
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_streamable_http_transport(self, mock_server):
        """Test main function with streamable-http transport."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'streamable-http']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='streamable-http',
            host='0.0.0.0',
            port=8000,
            path=None
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_custom_host_and_port(self, mock_server):
        """Test main function with custom host and port."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse', '--host', '127.0.0.1', '--port', '9000']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='127.0.0.1',
            port=9000,
            path=None
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_short_transport_argument(self, mock_server):
        """Test main function with short transport argument."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '-t', 'sse']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='0.0.0.0',
            port=8000,
            path=None
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_short_port_argument(self, mock_server):
        """Test main function with short port argument."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '-t', 'sse', '-p', '3000']):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='0.0.0.0',
            port=3000,
            path=None
        )
    
    def test_main_help_argument(self):
        """Test help argument exits with code 0."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    def test_main_version_argument(self):
        """Test version argument exits with code 0."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--version']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    def test_main_invalid_transport(self):
        """Test invalid transport argument exits with code 2."""
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
    
    @patch('vnstock_mcp.server.server')
    def test_main_keyboard_interrupt(self, mock_server):
        """Test KeyboardInterrupt handling."""
        mock_server.run = MagicMock(side_effect=KeyboardInterrupt())
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    main()
        
        assert exc_info.value.code == 0
        mock_print.assert_any_call("\nServer stopped by user.", file=sys.stderr)
    
    @patch('vnstock_mcp.server.server')
    def test_main_general_exception(self, mock_server):
        """Test general exception handling."""
        mock_server.run = MagicMock(side_effect=Exception("Test error"))
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print') as mock_print:
                with pytest.raises(SystemExit) as exc_info:
                    main()
        
        assert exc_info.value.code == 1
        mock_print.assert_any_call("Error starting server: Test error", file=sys.stderr)
    
    @patch('vnstock_mcp.server.server')  
    def test_main_prints_startup_messages_stdio(self, mock_server):
        """Test that startup messages are printed to stderr for stdio."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server']):
            with patch('builtins.print') as mock_print:
                main()
        
        # Check startup messages
        mock_print.assert_any_call(
            "Starting VNStock MCP Server with stdio transport...",
            file=sys.stderr
        )
    
    @patch('vnstock_mcp.server.server')  
    def test_main_prints_startup_messages_sse(self, mock_server):
        """Test that startup messages are printed to stderr for SSE."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', ['vnstock-mcp-server', '--transport', 'sse', '--path', '/vnstock']):
            with patch('builtins.print') as mock_print:
                main()
        
        # Check startup messages
        mock_print.assert_any_call(
            "Starting VNStock MCP Server with sse transport...",
            file=sys.stderr
        )
        mock_print.assert_any_call(
            "Server running on http://0.0.0.0:8000",
            file=sys.stderr
        )
        mock_print.assert_any_call(
            "Endpoint path: /vnstock",
            file=sys.stderr
        )
    
    @patch('vnstock_mcp.server.server')
    def test_main_all_parameters(self, mock_server):
        """Test main function with all parameters."""
        mock_server.run = MagicMock()
        
        with patch.object(sys, 'argv', [
            'vnstock-mcp-server',
            '--transport', 'sse',
            '--host', '192.168.1.1',
            '--port', '5000',
            '--path', '/api/mcp'
        ]):
            with patch('builtins.print'):
                main()
        
        mock_server.run.assert_called_once_with(
            transport='sse',
            host='192.168.1.1',
            port=5000,
            path='/api/mcp'
        )
