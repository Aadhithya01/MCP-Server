# server.py
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
from typing import Optional, List
import requests
# Create an MCP server
mcp = FastMCP("main")

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def extract_web_data(url: str, css_selector: Optional[str] = None) -> List[str]:
    """
    Extract data from a website.
    
    Args:
        url: The URL of the website to scrape
        css_selector: Optional CSS selector to extract specific elements (e.g., 'div.content', 'p')
    
    Returns:
        List of extracted text content
    """
    try:
        # Send HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data based on selector or get all text
        if css_selector:
            elements = soup.select(css_selector)
            return [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
        else:
            # Get all text content, excluding scripts and styles
            for element in soup(['script', 'style']):
                element.decompose()
            return [soup.get_text(strip=True)]
            
    except requests.RequestException as e:
        return [f"Error fetching URL: {str(e)}"]
    except Exception as e:
        return [f"Error processing content: {str(e)}"]
