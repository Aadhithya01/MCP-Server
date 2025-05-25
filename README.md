# FastMCP Web Automation and Data Processing Toolkit

A powerful and flexible toolkit built on FastMCP for web scraping, API data fetching, local file operations, and command-line automation.

## Overview

The FastMCP Toolkit is designed to simplify and automate common data processing tasks. It provides a robust set of tools for extracting data from websites (both static and dynamic content), interacting with public APIs, reading local text and CSV files, and executing terminal commands. Built on the `FastMCP` framework, this toolkit is ideal for developers, data analysts, and automation enthusiasts.

## Features

* *   **Web Data Extraction**: Seamlessly extract data from static and dynamic websites using a hybrid approach (BeautifulSoup and Selenium).
* *   **API Integration**: Fetch real-time data from public APIs with support for various HTTP methods (GET, POST, PUT, DELETE).
* *   **Local File Operations**: Read and process text and CSV files with ease.
* *   **Terminal Command Execution**: Execute system commands and capture their output securely.
* *   **Extensible Framework**: Built on FastMCP, allowing easy integration of additional tools.

## Installation

To get started, clone the repository and install the required dependencies using `uv`.

```bash
# Clone the repository
git clone https://github.com/yourusername/fastmcp-toolkit.git
cd fastmcp-toolkit

# Install dependencies using uv
uv pip install -r requirements.txt
```

### Prerequisites

* *   Python 3.8 or higher
* *   Chrome browser and [ChromeDriver](https://chromedriver.chromium.org/) for Selenium-based web scraping
* *   `uv` for dependency management (install via `pip install uv`)

### Dependencies

The toolkit relies on the following Python packages (listed in `requirements.txt`):

* *   `mcp.server.fastmcp`: Core framework for tool integration
* *   `beautifulsoup4`: For parsing static HTML content
* *   `requests`: For HTTP requests and API interactions
* *   `selenium`: For scraping dynamic web content
* *   `python-dotenv`: For managing environment variables
* *   Other dependencies listed in `requirements.txt`

## Configuration

1. 1.  **Create a `.env` file** in the project root to store environment variables (e.g., API credentials or other sensitive data):
1.     
1.     ```plaintext
1.     USERNAME=your_email@example.com
1.     PASSWORD=your_password
1.     ```
1.     
1. 2.  **Install Chrome and ChromeDriver**:
1.     
1.     * *   Ensure Chrome is installed on your system.
1.     * *   Download and configure [ChromeDriver](https://chromedriver.chromium.org/) compatible with your Chrome version.
1.     * *   Add ChromeDriver to your system PATH or specify its location in your environment.
1. 3.  **Verify dependencies**:  
1.     Run `uv pip install -r requirements.txt` to ensure all dependencies are installed correctly.
1.     

## Usage

### Starting the MCP Server

To use the toolkit, initialize and start the FastMCP server:

```python
from toolkit import mcp

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

* *   **Parameters**:* *   `url`: The website URL to scrape (e.g., `https://example.com`)
*     * *   `css_selector`: Optional CSS selector to target specific elements (e.g., `div.content`, `p`)
* *   **Returns**: List of extracted text strings
* *   **Example**:
*     
*     ```python
*     result = extract_web_data_auto("https://example.com", "div.content")
*     print(result)  # Prints list of text from elements matching 'div.content'
*     ```
*     

### `fetch_api_data(api_url: str, endpoint: str, method: str = "GET", params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = None, timeout: int = 10) -> Dict`

Fetch data from a public API with support for various HTTP methods.

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

Execute a terminal command and capture its output.

* *   **Parameters**:* *   `command`: Command to run (string for `shell=True`, list of strings for `shell=False`)
* *   **Returns**: List of output lines or an error message
* *   **Notes**:* *   Use lists (e.g., `["ls", "-la"]`) for safer execution with `shell=False`.
*     * *   Use strings (e.g., `"ls -la | grep .py"`) with caution, as `shell=True` can pose security risks with untrusted input.
* *   **Example**:
*     
*     ```python
*     # Safe command execution
*     output = run_terminal_command(["ls", "-la"])
*     print(output)  # Prints list of directory contents
*     
*     # Shell command (use with caution)
*     output = run_terminal_command("ls -la | grep .py")
*     print(output)  # Prints list of Python files
*     ```
*     

## Security Notes

- When using `run_terminal_command`, prefer passing commands as lists (`shell=False`) rather than strings (`shell=True`) to minimize security risks
- Store sensitive information in environment variables, not directly in code
- Be mindful of website terms of service when using the web scraping tools

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.