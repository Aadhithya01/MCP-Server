from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import csv
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import imapclient
from email import policy
from email.parser import BytesParser
import html2text
from datetime import datetime
from dotenv import load_dotenv
import subprocess
from typing import Union

load_dotenv()  # Load environment variables from .env file

# Create an MCP server
mcp = FastMCP("main")

# Addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Combined web data extractor
@mcp.tool()
def extract_web_data_auto(url: str, css_selector: Optional[str] = None) -> List[str]:
    """
    Extract data from a website, automatically handling both static and dynamic content.
    
    Args:
        url: The URL of the website to scrape
        css_selector: Optional CSS selector to extract specific elements (e.g., 'div.content', 'p')
    
    Returns:
        List of extracted text content
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup_static = BeautifulSoup(response.text, 'html.parser')
        
        if css_selector:
            elements_static = soup_static.select(css_selector)
            if elements_static:
                return [element.get_text(strip=True) for element in elements_static if element.get_text(strip=True)]
        
        return _extract_with_selenium(url, css_selector)
    
    except requests.RequestException:
        return _extract_with_selenium(url, css_selector)
    
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]

# Helper function for Selenium-based scraping
def _extract_with_selenium(url: str, css_selector: Optional[str] = None) -> List[str]:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        if css_selector:
            elements = soup.select(css_selector)
            result = [element.get_text(strip=True) for element in elements if element.get_text(strip=True)]
        else:
            for element in soup(['script', 'style']):
                element.decompose()
            result = [soup.get_text(strip=True)]
        
        return result
    
    except Exception as e:
        return [f"Selenium error: {str(e)}"]
    
    finally:
        driver.quit()

# Fetch API data
@mcp.tool()
def fetch_api_data(api_url: str, endpoint: str, method: str = "GET", params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = None, timeout: int = 10) -> Dict:
    """
    Fetch data from a public API in real time.
    
    Args:
        api_url: The base URL of the API
        endpoint: The specific endpoint path
        method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        params: Optional dictionary of query parameters
        body: Optional dictionary for the request body (JSON-encoded)
        headers: Optional dictionary of HTTP headers
        timeout: Request timeout in seconds (default: 10)
    
    Returns:
        Dictionary containing the API response
    """
    full_url = f"{api_url.rstrip('/')}/{endpoint.lstrip('/')}"
    if method.upper() in ['GET', 'DELETE'] and body is not None:
        return {"error": "Body is not allowed for GET and DELETE methods"}
    
    try:
        response = requests.request(method, full_url, params=params, json=body, headers=headers, timeout=timeout)
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

# New tool to run terminal commands
@mcp.tool()
def run_terminal_command(command: Union[str, List[str]]) -> List[str]:
    """
    Run a command in the terminal and return the output.

    Args:
        command: The command to run. If str, it will be run with shell=True. If List[str], it will be run with shell=False.

    Note: When passing a string, shell=True is used, which can pose a security risk if the command is constructed from untrusted input. When passing a list, shell=False is used, which is safer.

    Returns:
        A list of strings representing the output lines if successful, or an error message if failed.
    """
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False)
        else:
            result = subprocess.run(command, shell=False, capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            return result.stdout.splitlines()
        else:
            return [f"Command failed with return code {result.returncode}: {result.stderr}"]
    except Exception as e:
        return [f"Error running command: {str(e)}"]

# # Email summarizer
# @mcp.tool()
# def summarize_emails(email_texts: List[str], language: str = "english", summary_length: int = 3) -> List[str]:
#     """
#     Summarize a list of email texts using the LexRank algorithm.
    
#     Args:
#         email_texts: List of email texts to summarize
#         language: Language of the emails (default: 'english')
#         summary_length: Number of sentences in each summary (default: 3)
    
#     Returns:
#         List of summaries, one for each email
#     """
#     try:
#         summaries = []
#         for email_text in email_texts:
#             if not email_text.strip():
#                 summaries.append("Error: Empty email text")
#                 continue
#             parser = PlaintextParser.from_string(email_text, Tokenizer(language))
#             summarizer = LexRankSummarizer()
#             summary = summarizer(parser.document, summary_length)
#             summaries.append(" ".join(str(sentence) for sentence in summary))
#         return summaries
#     except Exception as e:
#         return [f"Error summarizing emails: {str(e)}"]

# # Tool for fetching and summarizing daily emails
# @mcp.tool()
# def get_daily_email_summary(language: str = "english", summary_length: int = 3) -> List[str]:
#     """
#     Fetch emails from today and return their summaries.
    
#     Args:
#         language: Language of the emails (default: 'english')
#         summary_length: Number of sentences in each summary (default: 3)
    
#     Returns:
#         List of summaries for today's emails
#     """
#     # Email credentials (replace with your actual credentials)
#     username = os.getenv('USERNAME')  # Replace with your Gmail address
#     password = os.getenv('PASSWORD')     # Replace with your Gmail app password

#     if not username or not password:
#         return ["Error: Email username or password not set"]

#     # Connect to Gmail IMAP server
#     try:
#         imap_obj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
#         imap_obj.login(username, password)
#         imap_obj.select_folder('INBOX', readonly=True)
#     except Exception as e:
#         return [f"Error connecting to IMAP server: {str(e)}"]

#     # Get today's date
#     today = datetime.now().strftime('%d-%b-%Y')

#     # Search for emails from today
#     try:
#         search_criteria = f'(SINCE "{today}")'
#         messages = imap_obj.search(search_criteria)
#     except Exception as e:
#         imap_obj.logout()
#         return [f"Error searching emails: {str(e)}"]

#     # Fetch email contents
#     email_texts = []
#     for msg_id in messages:
#         try:
#             raw_message = imap_obj.fetch(msg_id, ['RFC822'])[msg_id][b'RFC822']
#             msg = BytesParser(policy=policy.default).parsebytes(raw_message)
#             text = ""
#             for part in msg.walk():
#                 if part.get_content_type() == 'text/plain':
#                     text = part.get_payload(decode=True).decode()
#                     break
#                 elif part.get_content_type() == 'text/html':
#                     html = part.get_payload(decode=True).decode()
#                     text = html2text.html2text(html)
#                     break
#             if text:
#                 email_texts.append(text)
#         except Exception as e:
#             continue  # Skip problematic emails

#     imap_obj.logout()

#     # Summarize emails
#     if not email_texts:
#         return ["No emails found for today"]
#     return summarize_emails(email_texts, language, summary_length)