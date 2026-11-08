from fastmcp import FastMCP

mcp = FastMCP("Enterprise MCP Server")

@mcp.tool()
def get_customer(customer_id: int) -> dict:
    """Retrieve customer information using customer ID."""
    return {
        "customer_id": customer_id,
        "name": "John Smith",
        "status": "Active"
    }

@mcp.tool()
def calculate_total(price: float, quantity: int) -> dict:
    """Calculate total price."""
    return {
        "total": price * quantity
    }

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001
    )