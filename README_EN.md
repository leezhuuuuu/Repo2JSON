 # GitHub Repo Downloader

[English](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README_EN.md) | [中文](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README.md)

[![](https://img.shields.io/github/license/leezhuuuuu/Repo2JSON.svg)](LICENSE)
![](https://img.shields.io/github/stars/leezhuuuuu/Repo2JSON.svg)
![](https://img.shields.io/github/forks/leezhuuuuu/Repo2JSON.svg)

## Overview

The GitHub Repo Downloader is a lightweight Flask-based API service designed to fetch and download files from a GitHub repository, adhering to configurable constraints such as depth, file count, and file size limits. This tool is ideal for developers who need a quick and efficient way to extract specific parts of a repository without cloning the entire repo.

## Features

- **Depth Limitation**: Control the depth of directory traversal up to a specified maximum.
- **File Count Limitation**: Skip directories that exceed a predefined number of files.
- **File Size Limitation**: Ignore files that exceed a specified character count.
- **License Exclusion**: Optionally exclude the LICENSE file from the download.
- **Rate Limit Handling**: Automatically handles GitHub API rate limits and provides feedback on when to retry.

## Tech Stack

- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
- **HTTP Requests**: [Requests](https://docs.python-requests.org/)
- **Proxying**: Utilizes HTTP/HTTPS proxies if configured via environment variables.

## Setup & Installation

### Prerequisites

- Python 3.x
- Flask
- Requests
- An environment variable `HTTP_PROXY` if you need to use a proxy for HTTP/HTTPS requests.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-repo-downloader.git
   cd github-repo-downloader
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables if using a proxy:
   ```bash
   export HTTP_PROXY="http://your-proxy-url:port"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Configuration

The application uses several configurable parameters to control its behavior:

- `EXCLUDE_LICENSE`: Set to `True` to skip the LICENSE file.
- `ENABLE_DEPTH_LIMIT`: Enable or disable depth limitation.
- `MAX_DEPTH`: Maximum depth for directory traversal.
- `ENABLE_FILE_COUNT_LIMIT`: Enable or disable file count limitation per directory.
- `MAX_FILES_PER_DIR`: Maximum number of files allowed in a directory before skipping it.
- `ENABLE_FILE_SIZE_LIMIT`: Enable or disable file size limitation.
- `MAX_FILE_SIZE`: Maximum character count for a file before skipping it.

## API Endpoints

### `POST /download`

Downloads the contents of a specified GitHub repository. Requires the `repo_url` in the request body and a Bearer token in the Authorization header.

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

Returns a JSON object containing the file tree structure and the contents of the files that meet the specified criteria.

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

The API returns appropriate HTTP status codes and error messages in case of failures such as invalid requests, rate limit exceedance, or internal server errors.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss any improvements or features you'd like to see.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

- [Your Name](https://github.com/yourusername)

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- GitHub API