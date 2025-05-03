"""Request类 - 处理HTTP请求"""

import asyncio
import json
from urllib.parse import urlparse, urlencode
from typing import Dict, List, Any, Callable, Union, Optional

import requests
import aiohttp

from .response import Response
from . import utils

class Request:
    """请求类，用于处理HTTP请求"""
    
    def __init__(self, **options):
        """创建一个新的请求实例
        
        Args:
            **options: 请求选项
        """
        self.options = {
            'method': 'GET',
            'headers': {},
            'timeout': 30,  # 默认30秒超时
            'max_retries': 3,  # 默认最多重试3次
            'retry_delay': 1,  # 重试间隔1秒
            'validate_status': lambda status: 200 <= status < 300,
            'follow_redirects': True,
            'max_redirects': 5,
            'verify': True,  # SSL验证
            'cert': None,  # 客户端证书
            'proxies': None,  # 代理设置
        }
        
        # 更新选项
        self.options.update(options)
        
        # 请求和响应钩子
        self.hooks = {
            'before_request': [],
            'after_response': []
        }
        
        # 合并用户提供的钩子
        if 'hooks' in options:
            for hook_type, hooks in options['hooks'].items():
                if isinstance(hooks, list):
                    self.hooks[hook_type].extend(hooks)
    
    def before_request(self, hook: Callable):
        """添加请求前钩子
        
        Args:
            hook: 钩子函数
            
        Returns:
            Request: 当前请求实例
        """
        self.hooks['before_request'].append(hook)
        return self
    
    def after_response(self, hook: Callable):
        """添加响应后钩子
        
        Args:
            hook: 钩子函数
            
        Returns:
            Request: 当前请求实例
        """
        self.hooks['after_response'].append(hook)
        return self
    
    def prepare_options(self, url: str) -> Dict[str, Any]:
        """准备请求选项
        
        Args:
            url: 请求URL
            
        Returns:
            Dict[str, Any]: 处理后的请求选项
        """
        options = self.options.copy()
        parsed_url = urlparse(url)
        
        # 处理查询参数
        if 'params' in options:
            # 构建查询字符串
            query_params = options.pop('params')
            url = utils.build_url(url, query_params)
        
        # 处理请求体
        if 'json' in options:
            options['data'] = json.dumps(options.pop('json'))
            if 'headers' not in options:
                options['headers'] = {}
            options['headers']['Content-Type'] = 'application/json'
        
        # 处理表单数据
        if 'form' in options:
            options['data'] = urlencode(options.pop('form'))
            if 'headers' not in options:
                options['headers'] = {}
            options['headers']['Content-Type'] = 'application/x-www-form-urlencoded'
        
        # 移除不是requests库的选项
        requests_options = options.copy()
        for key in ['max_retries', 'retry_delay', 'validate_status', 'hooks']:
            if key in requests_options:
                requests_options.pop(key)
        
        # 重命名一些选项以匹配requests库
        if 'follow_redirects' in requests_options:
            requests_options['allow_redirects'] = requests_options.pop('follow_redirects')
        
        return {
            'url': url,
            'requests_options': requests_options,
            'max_retries': options.get('max_retries', 3),
            'retry_delay': options.get('retry_delay', 1),
            'validate_status': options.get('validate_status', lambda status: 200 <= status < 300)
        }
    
    async def run_before_request_hooks(self, options: Dict[str, Any]) -> Dict[str, Any]:
        """执行请求前钩子
        
        Args:
            options: 请求选项
            
        Returns:
            Dict[str, Any]: 处理后的请求选项
        """
        current_options = options
        
        for hook in self.hooks['before_request']:
            # 支持同步和异步钩子
            if asyncio.iscoroutinefunction(hook):
                result = await hook(current_options)
            else:
                result = hook(current_options)
            
            if result is not None:
                current_options = result
        
        return current_options
    
    async def run_after_response_hooks(self, response: 'Response') -> 'Response':
        """执行响应后钩子
        
        Args:
            response: 响应对象
            
        Returns:
            Response: 处理后的响应对象
        """
        current_response = response
        
        for hook in self.hooks['after_response']:
            # 支持同步和异步钩子
            if asyncio.iscoroutinefunction(hook):
                result = await hook(current_response)
            else:
                result = hook(current_response)
            
            if result is not None:
                current_response = result
        
        return current_response
    
    def send(self, url: str) -> Response:
        """发送同步请求
        
        Args:
            url: 请求URL
            
        Returns:
            Response: 响应对象
        """
        # 同步API，但内部使用异步实现的包装
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(self.send_async(url))
        finally:
            loop.close()
    
    async def send_async(self, url: str) -> Response:
        """发送异步请求
        
        Args:
            url: 请求URL
            
        Returns:
            Response: 响应对象
        """
        prepared_options = self.prepare_options(url)
        prepared_options = await self.run_before_request_hooks(prepared_options)
        
        url = prepared_options['url']
        requests_options = prepared_options['requests_options']
        max_retries = prepared_options['max_retries']
        retry_delay = prepared_options['retry_delay']
        validate_status = prepared_options['validate_status']
        
        retries = 0
        last_error = None
        
        while retries <= max_retries:
            try:
                # 使用aiohttp发送异步请求
                async with aiohttp.ClientSession() as session:
                    method = requests_options.pop('method')
                    timeout = aiohttp.ClientTimeout(total=requests_options.pop('timeout', 30))
                    
                    # 转换请求选项为aiohttp格式
                    aiohttp_options = {
                        'headers': requests_options.pop('headers', {}),
                        'timeout': timeout,
                        'ssl': None if not requests_options.pop('verify', True) else requests_options.pop('cert', None),
                        'allow_redirects': requests_options.pop('allow_redirects', True),
                        'max_redirects': requests_options.pop('max_redirects', 5),
                        'proxy': requests_options.pop('proxies', None),
                    }
                    
                    # 添加请求体
                    if 'data' in requests_options:
                        aiohttp_options['data'] = requests_options.pop('data')
                    
                    # 发送请求
                    async with getattr(session, method.lower())(url, **aiohttp_options) as aiohttp_response:
                        # 创建响应对象
                        response = Response(aiohttp_response)
                        
                        # 验证状态码
                        if not validate_status(response.status_code):
                            raise requests.exceptions.HTTPError(
                                f"HTTP错误: {response.status_code} {response.reason}",
                                response=response
                            )
                        
                        # 运行响应后钩子
                        response = await self.run_after_response_hooks(response)
                        
                        return response
            
            except Exception as e:
                last_error = e
                retries += 1
                
                # 如果达到最大重试次数，抛出最后一个错误
                if retries > max_retries:
                    break
                
                # 等待重试
                await asyncio.sleep(retry_delay)
        
        # 如果所有重试都失败，抛出最后一个错误
        raise last_error