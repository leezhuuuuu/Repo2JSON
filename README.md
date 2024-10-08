# Repo2JSON
[English](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README_EN.md) | [中文](https://github.com/leezhuuuuu/Repo2JSON/blob/main/README.md)

[![](https://img.shields.io/github/license/leezhuuuuu/Repo2JSON.svg)](LICENSE)
![](https://img.shields.io/github/stars/leezhuuuuu/Repo2JSON.svg)
![](https://img.shields.io/github/forks/leezhuuuuu/Repo2JSON.svg)

## 概述

Repo2JSON 是一个基于 Flask 的轻量级 API 服务，旨在将 GitHub 仓库的源代码转换为适合大型语言模型（LLM）理解的 JSON 格式。通过可配置的约束条件（如深度、文件数量和文件大小限制），该工具能够高效地提取仓库的特定部分，而无需克隆整个仓库。Repo2JSON 非常适合需要快速提取和处理代码库内容的开发者。

## 功能

- **深度限制**：控制目录遍历的深度，直至指定的最大深度。
- **文件数量限制**：跳过超过预定义文件数量的目录。
- **文件大小限制**：忽略超过指定字符数的文件。
- **许可证排除**：可选地从下载中排除 LICENSE 文件。
- **速率限制处理**：自动处理 GitHub API 的速率限制，并提供何时重试的反馈。
- **二进制文件排除**：确保只下载文本文件，排除所有二进制文件。
- **硬编码令牌支持**：如果请求中未提供令牌，可以使用硬编码的 GitHub API 令牌。

## 技术栈

- **后端框架**：[Flask](https://flask.palletsprojects.com/)
- **HTTP 请求**：[Requests](https://docs.python-requests.org/)
- **代理**：如果通过环境变量配置，则使用 HTTP/HTTPS 代理。

## 安装与设置

### 先决条件

- Python 3.x
- Flask
- Requests
- 如果需要使用 HTTP/HTTPS 代理，请设置环境变量 `HTTP_PROXY`。

### 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/leezhuuuuu/Repo2JSON.git
   cd Repo2JSON
   ```

2. 安装所需包：
   ```bash
   pip install -r requirements.txt
   ```

3. 如果使用代理，请设置环境变量：
   ```bash
   export HTTP_PROXY="http://your-proxy-url:port"
   ```

4. 运行应用程序：
   ```bash
   python app.py
   ```

## 配置

应用程序使用多个可配置参数来控制其行为：

- `EXCLUDE_LICENSE`：设置为 `True` 以跳过 LICENSE 文件。
- `ENABLE_DEPTH_LIMIT`：启用或禁用深度限制。
- `MAX_DEPTH`：目录遍历的最大深度。
- `ENABLE_FILE_COUNT_LIMIT`：启用或禁用每个目录的文件数量限制。
- `MAX_FILES_PER_DIR`：在跳过目录之前允许的最大文件数量。
- `ENABLE_FILE_SIZE_LIMIT`：启用或禁用文件大小限制。
- `MAX_FILE_SIZE`：在跳过文件之前允许的最大字符数。
- `HARDCODED_TOKEN`：硬编码的 GitHub API 令牌，用于在请求中未提供令牌时使用。

## 获取 GitHub Token

要获取 GitHub Token，请访问 [GitHub Tokens Settings](https://github.com/settings/tokens) 并生成一个新的个人访问令牌。确保为令牌选择 `repo` 权限，以便能够访问私有仓库和执行仓库相关的操作。

## API 端点

### `POST /repo2json`

下载指定 GitHub 仓库的内容，并将其转换为适合 LLM 理解的 JSON 格式。需要在请求体中提供 `repo_url`，并在 Authorization 头中提供 Bearer 令牌。

#### 请求体

```json
{
  "repo_url": "https://github.com/owner/repo"
}
```

#### 头部

```
Authorization: Bearer <your_github_token>
```

#### 响应

返回一个 JSON 对象，包含文件树结构和符合指定条件的文件内容。

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

## 错误处理

API 在失败情况下（如无效请求、速率限制超限或内部服务器错误）返回适当的 HTTP 状态码和错误信息。

## 贡献

欢迎贡献！请随时提交拉取请求或开启问题以讨论任何改进或新功能。

## 许可证

本项目基于 GNU 许可证。详见 [LICENSE](LICENSE) 文件。

## 作者

- [Lee Zhu](https://github.com/leezhuuuuu)

## 致谢

- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- GitHub API


## GitHub Star History

[![Star History Chart](https://api.star-history.com/svg?repos=leezhuuuuu/Repo2JSON&type=Date)](https://star-history.com/#leezhuuuuu/Repo2JSON&Date)