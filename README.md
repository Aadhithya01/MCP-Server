# FastMCP Web Automation and Data Processing Toolkit

A powerful toolkit built on FastMCP for web scraping, API data fetching, local file operations, and command-line automation.

## Overview

This toolkit provides a collection of tools for automating common web and data processing tasks using FastMCP. It includes capabilities for extracting data from websites (both static and dynamic), interacting with APIs, reading local files, and executing terminal commands.

## Features

- **Web Data Extraction**: Automatically handle both static and dynamic web content
- **API Integration**: Fetch data from public APIs using various HTTP methods
- **Local File Operations**: Read and process text and CSV files
- **Terminal Command Execution**: Run system commands and capture their output

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fastmcp-toolkit.git
cd fastmcp-toolkit

# Install dependencies using uv
uv pip install -r requirements.txt
```

## Dependencies

- mcp.server.fastmcp
- BeautifulSoup4
- requests
- selenium
- python-dotenv
- and others listed in requirements.txt

## Configuration

1. Create a `.env` file in the project root with any required environment variables:

```
USERNAME=your_email@example.com
PASSWORD=your_password
```

2. Ensure you have Chrome and ChromeDriver installed for Selenium-based scraping

## Usage

### Basic Usage

```python
from toolkit import mcp

# Start the MCP server
if __name__ == "__main__":
    mcp.start()
```

### Available Tools

#### 1. Web Data Extraction

```python
# Extract text from a website
result = extract_web_data_auto("https://example.com", "div.content")
```

#### 2. API Data Fetching

```python
# Get data from a REST API
data = fetch_api_data(
    api_url="https://api.example.com",
    endpoint="/users",
    method="GET",
    params={"limit": 10}
)
```

#### 3. Reading Local Files

```python
# Read a text file
lines = read_local_file("data/example.txt", "text")

# Read a CSV file
rows = read_local_file("data/data.csv", "csv")
```

#### 4. Running Terminal Commands

```python
# Run a command safely (recommended approach)
output = run_terminal_command(["ls", "-la"])

# Run a command with shell=True (use with caution)
output = run_terminal_command("ls -la | grep .py")
```

## Tool Reference

### `add(a: int, b: int) -> int`

A simple utility to add two numbers.

### `extract_web_data_auto(url: str, css_selector: Optional[str] = None) -> List[str]`

Extract text content from websites, automatically handling both static and dynamic content.

- **Parameters:**
  - `url`: The website URL to scrape
  - `css_selector`: Optional CSS selector to target specific elements

- **Returns:** List of extracted text content

### `fetch_api_data(api_url: str, endpoint: str, method: str = "GET", params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = None, timeout: int = 10) -> Dict`

Fetch data from a public API.

- **Parameters:**
  - `api_url`: Base URL of the API
  - `endpoint`: Specific endpoint path
  - `method`: HTTP method (GET, POST, PUT, DELETE)
  - `params`: Query parameters
  - `body`: Request body (for POST/PUT)
  - `headers`: HTTP headers
  - `timeout`: Request timeout in seconds

- **Returns:** Dictionary containing the API response

### `read_local_file(file_path: str, file_type: str = "text") -> List[str]`

Read content from a local text or CSV file.

- **Parameters:**
  - `file_path`: Path to the file
  - `file_type`: Type of file ('text' or 'csv')

- **Returns:** List of file content

### `run_terminal_command(command: Union[str, List[str]]) -> List[str]`

Run a command in the terminal and return the output.

- **Parameters:**
  - `command`: Command to run (string or list of strings)

- **Returns:** List of output lines or error message

## Security Notes

- When using `run_terminal_command`, prefer passing commands as lists (`shell=False`) rather than strings (`shell=True`) to minimize security risks
- Store sensitive information in environment variables, not directly in code
- Be mindful of website terms of service when using the web scraping tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.