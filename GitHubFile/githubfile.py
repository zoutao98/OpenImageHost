'''
   Copyright 2022 zoutao

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import requests
import base64
import json


def getContent(file_path):
    """
    获取文件的 Base64 编码结果
    """
    with open(file_path,'rb') as f:
        # 将二进制文件编码后转换为字符串形式
        return base64.b64encode(f.read()).decode('utf-8')


def getFile(token, user_repo, filename):
    """
    GitHub API v3 请求文件
    GET /repos/{owner}/{repo}/contents/{path}
    """
    url = f"https://api.github.com/repos/{user_repo}/contents/{filename}"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url=url, headers=headers)


def getLargeFile(token, user_repo, file_sha):
    """
    GitHub API v3 请求二进制blob
    get /repos/{owner}/{repo}/git/blobs/{file_sha}
    """
    url = f"https://api.github.com/repos/{user_repo}/git/blobs/{file_sha}"
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}'
    }
    return requests.get(url=url, headers=headers)


def uploadFile(token, user_repo, filename, content):
    """
    GitHub API v3 上传/更新文件
    PUT /repos/{owner}/{repo}/contents/{path}
    """
    url = f"https://api.github.com/repos/{user_repo}/contents/{filename}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "message": "upload by OpenImageHost",
        "content": content,
    }
    response = requests.put(url=url, data=json.dumps(data), headers=(headers))
    return response


def updateFile(token, user_repo, filename, content, sha):
    """
    GitHub API v3 上传/更新文件
    PUT /repos/{owner}/{repo}/contents/{path}
    """
    url = f"https://api.github.com/repos/{user_repo}/contents/{filename}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "message": "upload by OpenImageHost",
        "content": content,
        "sha": sha
    }
    response = requests.put(url=url, data=json.dumps(data), headers=(headers))
    return response