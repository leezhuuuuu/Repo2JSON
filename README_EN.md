# Repo2JSON
[English](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README_EN.md) | [中文](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README.md)

[![](https://img.shields.io/github/license/leezhuuuuu/Repo2JSON.svg)](LICENSE)
![](https://img.shields.io/github/stars/leezhuuuuu/Repo2JSON.svg)
![](https://img.shields.io/github/forks/leezhuuuuu/Repo2JSON.svg)

## Overview

Repo2JSON is a lightweight API service based on Flask, designed to convert GitHub repository source code into JSON format suitable for Large Language Models (LLM). With configurable constraints such as depth, file count, and file size limits, this tool efficiently extracts specific parts of the repository without cloning the entire repository. Repo2JSON is perfect for developers who need to quickly extract and process repository content.

## Features

- **Depth Limit**: Controls the depth of directory traversal up to a specified maximum depth.
- **File Count Limit**: Skips directories that exceed a predefined number of files.
- **File Size Limit**: Ignores files that exceed a specified number of characters.
- **License Exclusion**: Optionally excludes LICENSE files from the download.
- **Rate Limit Handling**: Automatically handles GitHub API rate limits and provides feedback on when to retry.
- **Binary File Exclusion**: Ensures only text files are downloaded, excluding all binary files.
- **Hardcoded Token Support**: Uses a hardcoded GitHub API token if no token is provided in the request.

## Tech Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
- **HTTP Requests**: [Requests](https://docs.python-requests.org/)
- **Proxy**: Uses HTTP/HTTPS proxy if configured via environment variable.

## Installation and Setup

### Prerequisites

- Python 3.x
- Flask
- Requests
- If using HTTP/HTTPS proxy, set the `HTTP_PROXY` environment variable.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/leezhuuuuu/Repo2JSON.git
   cd Repo2JSON
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. If using a proxy, set the environment variable:
   ```bash
   export HTTP_PROXY="http://your-proxy-url:port"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Configuration

The application uses multiple configurable parameters to control its behavior:

- `EXCLUDE_LICENSE`: Set to `True` to skip LICENSE files.
- `ENABLE_DEPTH_LIMIT`: Enable or disable depth limit.
- `MAX_DEPTH`: Maximum depth of directory traversal.
- `ENABLE_FILE_COUNT_LIMIT`: Enable or disable file count limit per directory.
- `MAX_FILES_PER_DIR`: Maximum number of files allowed before skipping a directory.
- `ENABLE_FILE_SIZE_LIMIT`: Enable or disable file size limit.
- `MAX_FILE_SIZE`: Maximum number of characters allowed before skipping a file.
- `HARDCODED_TOKEN`: Hardcoded GitHub API token to use if no token is provided in the request.

## Getting GitHub Token

To get a GitHub Token, visit [GitHub Tokens Settings](https://github.com/settings/tokens) and generate a new personal access token. Ensure you select `repo` permissions for the token to access private repositories and perform repository-related operations.

## API Endpoint

### `POST /repo2json`

Downloads the content of a specified GitHub repository and converts it into JSON format suitable for LLM understanding. Requires `repo_url` in the request body and a Bearer token in the Authorization header.

#### Request Body

```json
{
  "repo_url": "https://github.com/owner/repo"
}
```

#### Headers

```
Authorization: Bearer <your_github_token>
```

#### Response

Returns a JSON object containing the file tree structure and file contents that meet the specified conditions.

```json
{
  "file_tree": {
    "dir1": {
      "file1.txt": null
    }
  },
  "file_contents": {
    "dir1/file1.txt": "File content here..."
  }
}
```

## Error Handling

The API returns appropriate HTTP status codes and error messages in case of failures such as invalid requests, rate limit exceeded, or internal server errors.

## Contribution

Contributions are welcome! Please feel free to submit pull requests or open issues to discuss any improvements or new features.

## License

This project is licensed under the GNU License. See the [LICENSE](LICENSE) file for details.

## Author

- [Lee Zhu](https://github.com/leezhuuuuu)

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- GitHub API
