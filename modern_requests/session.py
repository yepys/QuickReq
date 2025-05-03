"""Session类 - 管理HTTP会话和Cookie"""

import copy
from http.cookiejar import CookieJar
from typing import Dict, List, Any, Callable, Union, Optional

import requests
import aiohttp

from .request import Request
from . import utils

class Session:
    """会话类，用于管理HTTP会话和Cookie"""
    
    def __init__(self, options=None):
        """创建一个新的会话实例
        
        Args:
            options (dict, optional): 会话选项
        """
        self.options = options or {}
        self.options.setdefault('headers', {})
        
        # 存储会话Cookie
        self.cookies = CookieJar()
        
        # 创建底层的requests会话和aiohttp会话
        self._requests_session = requests.Session()
        self._aiohttp_session = None  # 延迟初始化
        
        # 添加Cookie管理钩子
        self.hooks = {
            'before_request': [
                self._attach_cookies
            ],
            'after_response': [
                self._save_cookies
            ]
        }
        
        # 合并用户提供的钩子
        if 'hooks' in self.options:
            for hook_type, hooks in self.options['hooks'].items():
                if isinstance(hooks, list):
                    self.hooks[hook_type].extend(hooks)
    
    def _attach_cookies(self, options):
        """在请求前附加Cookie
        
        Args:
            options: 请求选项
            
        Returns:
            dict: 处理后的请求选项
        """
        # 将会话的Cookie添加到请求中
        if 'requests_options' in options:
            options['requests_options'].setdefault('cookies', {})
            # 合并会话Cookie和请求Cookie
            for cookie in self.cookies:
                if cookie.domain in options['url'] and cookie.path in options['url']:
                    options['requests_options']['cookies'][cookie.name] = cookie.value
        
        return options
    
    def _save_cookies(self, response):
        """保存响应中的Cookie
        
        Args:
            response: 响应对象
            
        Returns:
            Response: 原始响应对象
        """
        # 从响应中提取Cookie并保存到会话中
        if hasattr(response.original_response, 'cookies'):
            # requests响应
            for cookie in response.original_response.cookies:
                self.cookies.set_cookie(cookie)
        elif 'set-cookie' in response.headers:
            # aiohttp响应，手动解析Cookie
            cookie_header = response.headers.get('set-cookie')
            if cookie_header:
                self._requests_session.cookies.extract_cookies(
                    response.original_response,
                    requests.Request('GET', response.url).prepare()
                )
                # 同步Cookie到会话
                self.cookies = self._requests_session.cookies
        
        return response
    
    async def _ensure_aiohttp_session(self):
        """确保aiohttp会话已初始化
        
        Returns:
            aiohttp.ClientSession: aiohttp会话
        """
        if self._aiohttp_session is None or self._aiohttp_session.closed:
            self._aiohttp_session = aiohttp.ClientSession()
        return self._aiohttp_session
    
    def request(self, method, url, **kwargs):
        """创建一个新的请求实例
        
        Args:
            method: HTTP方法
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Request: 请求实例
        """
        # 合并会话选项和请求选项
        options = copy.deepcopy(self.options)
        options.update(kwargs)
        options['method'] = method
        
        # 合并钩子
        options.setdefault('hooks', {})
        for hook_type, hooks in self.hooks.items():
            options['hooks'].setdefault(hook_type, [])
            options['hooks'][hook_type].extend(hooks)
        
        return Request(**options)
    
    def get(self, url, **kwargs):
        """发送GET请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('GET', url, **kwargs).send(url)
    
    def post(self, url, **kwargs):
        """发送POST请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('POST', url, **kwargs).send(url)
    
    def put(self, url, **kwargs):
        """发送PUT请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('PUT', url, **kwargs).send(url)
    
    def delete(self, url, **kwargs):
        """发送DELETE请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('DELETE', url, **kwargs).send(url)
    
    def patch(self, url, **kwargs):
        """发送PATCH请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('PATCH', url, **kwargs).send(url)
    
    def head(self, url, **kwargs):
        """发送HEAD请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('HEAD', url, **kwargs).send(url)
    
    def options(self, url, **kwargs):
        """发送OPTIONS请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return self.request('OPTIONS', url, **kwargs).send(url)
    
    async def get_async(self, url, **kwargs):
        """异步发送GET请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('GET', url, **kwargs).send_async(url)
    
    async def post_async(self, url, **kwargs):
        """异步发送POST请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('POST', url, **kwargs).send_async(url)
    
    async def put_async(self, url, **kwargs):
        """异步发送PUT请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('PUT', url, **kwargs).send_async(url)
    
    async def delete_async(self, url, **kwargs):
        """异步发送DELETE请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('DELETE', url, **kwargs).send_async(url)
    
    async def patch_async(self, url, **kwargs):
        """异步发送PATCH请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('PATCH', url, **kwargs).send_async(url)
    
    async def head_async(self, url, **kwargs):
        """异步发送HEAD请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('HEAD', url, **kwargs).send_async(url)
    
    async def options_async(self, url, **kwargs):
        """异步发送OPTIONS请求
        
        Args:
            url: 请求URL
            **kwargs: 请求选项
            
        Returns:
            Response: 响应对象
        """
        return await self.request('OPTIONS', url, **kwargs).send_async(url)
    
    def get_cookies(self):
        """获取会话的Cookie
        
        Returns:
            dict: Cookie字典
        """
        cookies = {}
        for cookie in self.cookies:
            cookies[cookie.name] = cookie.value
        return cookies
    
    def set_cookie(self, name, value, **kwargs):
        """设置Cookie
        
        Args:
            name: Cookie名称
            value: Cookie值
            **kwargs: Cookie选项
            
        Returns:
            Session: 当前会话实例
        """
        self._requests_session.cookies.set(name, value, **kwargs)
        self.cookies = self._requests_session.cookies
        return self
    
    def clear_cookies(self):
        """清除所有Cookie
        
        Returns:
            Session: 当前会话实例
        """
        self._requests_session.cookies.clear()
        self.cookies = self._requests_session.cookies
        return self
    
    def close(self):
        """关闭会话"""
        self._requests_session.close()
        if self._aiohttp_session is not None and not self._aiohttp_session.closed:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self._aiohttp_session.close())
            else:
                loop.run_until_complete(self._aiohttp_session.close())
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    async def __aenter__(self):
        await self._ensure_aiohttp_session()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()