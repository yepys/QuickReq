"""Modern Requests Library
一个现代化高效的Python HTTP请求库
"""

from .request import Request
from .response import Response
from .session import Session
from . import utils

__version__ = "1.0.0"

# 创建请求实例
def create_request(options=None):
    """创建一个新的请求实例
    
    Args:
        options (dict, optional): 请求选项
        
    Returns:
        Request: 请求实例
    """
    return Request(options or {})

# 创建会话实例
def create_session(options=None):
    """创建一个新的会话实例
    
    Args:
        options (dict, optional): 会话选项
        
    Returns:
        Session: 会话实例
    """
    return Session(options or {})

# 同步请求方法
def get(url, **kwargs):
    """发送GET请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="GET", **kwargs).send(url)

def post(url, **kwargs):
    """发送POST请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="POST", **kwargs).send(url)

def put(url, **kwargs):
    """发送PUT请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="PUT", **kwargs).send(url)

def delete(url, **kwargs):
    """发送DELETE请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="DELETE", **kwargs).send(url)

def patch(url, **kwargs):
    """发送PATCH请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="PATCH", **kwargs).send(url)

def head(url, **kwargs):
    """发送HEAD请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="HEAD", **kwargs).send(url)

def options(url, **kwargs):
    """发送OPTIONS请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return Request(method="OPTIONS", **kwargs).send(url)

# 异步请求方法
async def get_async(url, **kwargs):
    """异步发送GET请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="GET", **kwargs).send_async(url)

async def post_async(url, **kwargs):
    """异步发送POST请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="POST", **kwargs).send_async(url)

async def put_async(url, **kwargs):
    """异步发送PUT请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="PUT", **kwargs).send_async(url)

async def delete_async(url, **kwargs):
    """异步发送DELETE请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="DELETE", **kwargs).send_async(url)

async def patch_async(url, **kwargs):
    """异步发送PATCH请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="PATCH", **kwargs).send_async(url)

async def head_async(url, **kwargs):
    """异步发送HEAD请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="HEAD", **kwargs).send_async(url)

async def options_async(url, **kwargs):
    """异步发送OPTIONS请求
    
    Args:
        url (str): 请求URL
        **kwargs: 请求选项
        
    Returns:
        Response: 响应对象
    """
    return await Request(method="OPTIONS", **kwargs).send_async(url)