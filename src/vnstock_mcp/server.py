import argparse
import sys
from fastmcp import FastMCP
from vnstock_mcp.tools import company_tools, listing_tools, finance_tools, fund_tools, misc_tools, quote_tools, trading_tools
server = FastMCP('VNStock MCP Server')

server.mount(company_tools.company_mcp)
server.mount(listing_tools.listing_mcp)
server.mount(finance_tools.finance_mcp)
server.mount(fund_tools.fund_mcp)
server.mount(misc_tools.misc_mcp)
server.mount(quote_tools.quote_mcp)
server.mount(trading_tools.trading_mcp)


def main():
    """Main entry point for the vnstock-mcp-server CLI."""
    parser = argparse.ArgumentParser(
        description='VNStock MCP Server - Vietnam Stock Market Data Access via MCP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            %(prog)s                              # Run with default stdio transport
            %(prog)s --transport stdio            # Explicitly use stdio transport
            %(prog)s --transport sse              # Use Server-Sent Events transport
            %(prog)s --transport sse --path /mcp  # SSE with custom endpoint path
            %(prog)s --transport streamable-http  # Use HTTP streaming transport
            
            Transport Modes:
            stdio          : Standard input/output (default, for MCP clients like Claude Desktop)
            sse            : Server-Sent Events (for web applications)
            streamable-http: HTTP streaming (for HTTP-based integrations)
        """
    )
    
    parser.add_argument(
        '--transport', '-t',
        choices=['stdio', 'sse', 'streamable-http'],
        default='stdio',
        help='Transport protocol to use (default: stdio)'
    )
    
    parser.add_argument(
        '--path',
        type=str,
        default=None,
        help='Endpoint path for HTTP transports (optional, e.g. /mcp)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host address to bind to (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='%(prog)s 1.0.2'
    )

    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Port to run the server on (default: 8000)'
    )
    
    try:
        args = parser.parse_args()
        
        # Run server with specified transport
        print(f"Starting VNStock MCP Server with {args.transport} transport...", file=sys.stderr)
        
        if args.transport == 'stdio':
            server.run(transport=args.transport)
        else:
            # HTTP-based transports (sse, streamable-http)
            print(f"Server running on http://{args.host}:{args.port}", file=sys.stderr)
            if args.path:
                print(f"Endpoint path: {args.path}", file=sys.stderr)
            server.run(
                transport=args.transport,
                host=args.host,
                port=args.port,
                path=args.path
            )
        
    except KeyboardInterrupt:
        print("\nServer stopped by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
