from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
from typing import Optional, List
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import csv

# Create an MCP server
mcp = FastMCP("main")

# Addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Web data extractor
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
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if css_selector:
            elements = soup.select(css_selector)
            return [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
        else:
            for element in soup(['script', 'style']):
                element.decompose()
            return [soup.get_text(strip=True)]
            
    except requests.RequestException as e:
        return [f"Error fetching URL: {str(e)}"]
    except Exception as e:
        return [f"Error processing content: {str(e)}"]

# Dynamic web scraper
@mcp.tool()
def extract_dynamic_web_data(url: str, css_selector: Optional[str] = None) -> List[str]:
    """
    Extract data from a website with JavaScript-rendered content using Selenium.
    
    Args:
        url: The URL of the website to scrape
        css_selector: Optional CSS selector to extract specific elements (e.g., 'div.content', 'p')
    
    Returns:
        List of extracted text content
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        
        if css_selector:
            elements = soup.select(css_selector)
            return [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
        else:
            for element in soup(['script', 'style']):
                element.decompose()
            return [soup.get_text(strip=True)]
            
    except Exception as e:
        return [f"Error processing dynamic content: {str(e)}"]

# Generic API data fetcher
@mcp.tool()
def fetch_api_data(api_url: str, endpoint: str, params: Optional[dict] = None) -> dict:
    """
    Fetch data from a public API in real time.
    
    Args:
        api_url: The base URL of the API (e.g., 'https://api.openweathermap.org')
        endpoint: The specific endpoint (e.g., '/data/2.5/weather')
        params: Optional dictionary of query parameters (e.g., {'q': 'London', 'appid': 'your_key'})
    
    Returns:
        Dictionary containing the API response
    """
    try:
        full_url = f"{api_url.rstrip('/')}/{endpoint.lstrip('/')}"
        response = requests.get(full_url, params=params)
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        return {"error": f"Error fetching API data: {str(e)}"}
    except ValueError as e:
        return {"error": f"Error parsing JSON response: {str(e)}"}

# Local file system reader
@mcp.tool()
def read_local_file(file_path: str, file_type: str = "text") -> List[str]:
    """
    Read content from a local text or CSV file.
    
    Args:
        file_path: Path to the file (relative or absolute)
        file_type: Type of file ('text' or 'csv')
    
    Returns:
        List of file content (lines for text, rows for CSV)
    """
    try:
        if not os.path.exists(file_path):
            return [f"Error: File not found at {file_path}"]
        
        if file_type == "text":
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        
        elif file_type == "csv":
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                return [','.join(row) for row in reader if any(row)]
        
        else:
            return [f"Error: Unsupported file type '{file_type}'"]
            
    except Exception as e:
        return [f"Error reading file: {str(e)}"]