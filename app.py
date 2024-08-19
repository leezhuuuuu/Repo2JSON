from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents"
EXCLUDE_LICENSE = True  # 默认不读取LICENSE文件
ENABLE_DEPTH_LIMIT = True  # 是否启用深度限制
MAX_DEPTH = 2  # 读取文件夹的最大深度
ENABLE_FILE_COUNT_LIMIT = True  # 是否启用文件数量限制
MAX_FILES_PER_DIR = 20  # 当任何一个文件夹中超过数量时，不读取这个文件夹
ENABLE_FILE_SIZE_LIMIT = True  # 是否启用文件字符数量限制
MAX_FILE_SIZE = 20000  # 当某个文件的字符数量时，不进行输出
HARDCODED_TOKEN = "your_hardcoded_token"  # 硬编码的token

def get_proxy():
    proxy = os.getenv('HTTP_PROXY')
    if proxy:
        return {
            'http': proxy,
            'https': proxy
        }
    return None

def get_repo_contents(owner, repo, path='', token=None):
    url = GITHUB_API_URL.format(owner=owner, repo=repo) + path
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    response = requests.get(url, proxies=get_proxy(), headers=headers)
    
    # Check for rate limit
    if response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
        if int(response.headers['X-RateLimit-Remaining']) == 0:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            return {"error": f"Rate limit exceeded. Try again after {reset_time}."}, 403
    
    response.raise_for_status()
    return response.json()

def build_file_tree(owner, repo, path='', token=None, depth=0):
    if ENABLE_DEPTH_LIMIT and depth > MAX_DEPTH:
        return {}

    contents = get_repo_contents(owner, repo, path, token)
    if isinstance(contents, dict) and 'error' in contents:
        return contents
    
    tree = {}
    for item in contents:
        if item['type'] == 'file':
            if EXCLUDE_LICENSE and item['name'].lower() == 'license':
                continue  # 跳过LICENSE文件
            tree[item['name']] = None
        elif item['type'] == 'dir':
            if ENABLE_FILE_COUNT_LIMIT and len(contents) > MAX_FILES_PER_DIR:
                continue  # 跳过文件数量超过阈值的文件夹
            tree[item['name']] = build_file_tree(owner, repo, item['path'], token, depth + 1)
    return tree

def download_files(owner, repo, path='', token=None, depth=0):
    if ENABLE_DEPTH_LIMIT and depth > MAX_DEPTH:
        return {}

    contents = get_repo_contents(owner, repo, path, token)
    if isinstance(contents, dict) and 'error' in contents:
        return contents
    
    result = {}
    for item in contents:
        if item['type'] == 'file':
            if EXCLUDE_LICENSE and item['name'].lower() == 'license':
                continue  # 跳过LICENSE文件
            file_content = requests.get(item['download_url'], proxies=get_proxy()).content
            try:
                file_content = file_content.decode('utf-8')
            except UnicodeDecodeError:
                continue  # 跳过无法解码为字符串的文件（二进制文件）
            if ENABLE_FILE_SIZE_LIMIT and len(file_content) > MAX_FILE_SIZE:
                continue  # 跳过字符数量超过阈值的文件
            result[item['path']] = file_content
        elif item['type'] == 'dir':
            if ENABLE_FILE_COUNT_LIMIT and len(contents) > MAX_FILES_PER_DIR:
                continue  # 跳过文件数量超过阈值的文件夹
            result[item['path']] = download_files(owner, repo, item['path'], token, depth + 1)
    return result

@app.route('/repo2json', methods=['POST'])
def repo2json():
    data = request.json
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({"error": "Missing repo_url"}), 400

    # Extract owner and repo from the URL
    parts = repo_url.strip('/').split('/')
    owner = parts[-2]
    repo = parts[-1]

    # Get token from Authorization header or use hardcoded token
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split('Bearer ')[1]
    elif HARDCODED_TOKEN:
        token = HARDCODED_TOKEN
    else:
        return jsonify({"error": "Missing or invalid Authorization header and no hardcoded token"}), 400

    try:
        file_tree = build_file_tree(owner, repo, token=token)
        file_contents = download_files(owner, repo, token=token)
        result = {
            "file_tree": file_tree,
            "file_contents": file_contents
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)