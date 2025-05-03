"""Response类 - 处理HTTP响应"""

import json
from typing import Dict, Any, Optional, Union

class Response:
    """响应类，用于处理HTTP响应"""
    
    def __init__(self, response):
        """创建一个新的响应实例
        
        Args:
            response: 原始响应对象（requests.Response或aiohttp.ClientResponse）
        """
        self.original_response = response
        
        # 根据响应类型设置属性
        if hasattr(response, 'status'):
            # aiohttp响应
            self.status_code = response.status
            self.reason = response.reason
            self.headers = dict(response.headers)
            self.url = str(response.url)
            self.ok = 200 <= response.status < 300
            self.is_redirect = response.history is not None and len(response.history) > 0
        else:
            # requests响应
            self.status_code = response.status_code
            self.reason = response.reason
            self.headers = dict(response.headers)
            self.url = response.url
            self.ok = response.ok
            self.is_redirect = response.is_redirect
        
        # 缓存响应体，避免多次解析
        self._body_cache = {
            'text': None,
            'json': None,
            'bytes': None
        }
    
    def text(self) -> str:
        """获取响应体文本
        
        Returns:
            str: 响应体文本
        """
        if self._body_cache['text'] is not None:
            return self._body_cache['text']
        
        # 根据响应类型获取文本
        if hasattr(self.original_response, 'text'):
            # requests响应
            self._body_cache['text'] = self.original_response.text
        else:
            # 同步API，但内部使用异步实现的包装
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                self._body_cache['text'] = loop.run_until_complete(self.text_async())
            finally:
                loop.close()
        
        return self._body_cache['text']
    
    def json(self) -> Any:
        """获取响应体JSON
        
        Returns:
            Any: 解析后的JSON对象
        
        Raises:
            json.JSONDecodeError: 解析JSON失败
        """
        if self._body_cache['json'] is not None:
            return self._body_cache['json']
        
        try:
            text = self.text()
            self._body_cache['json'] = json.loads(text)
            return self._body_cache['json']
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"解析JSON失败: {str(e)}", e.doc, e.pos)
    
    def bytes(self) -> bytes:
        """获取响应体字节
        
        Returns:
            bytes: 响应体字节
        """
        if self._body_cache['bytes'] is not None:
            return self._body_cache['bytes']
        
        # 根据响应类型获取字节
        if hasattr(self.original_response, 'content'):
            # requests响应
            self._body_cache['bytes'] = self.original_response.content
        else:
            # 同步API，但内部使用异步实现的包装
            import asyncio
            loop = asyncio.new_event_loop()
            try:
                self._body_cache['bytes'] = loop.run_until_complete(self.bytes_async())
            finally:
                loop.close()
        
        return self._body_cache['bytes']
    
    async def text_async(self) -> str:
        """异步获取响应体文本
        
        Returns:
            str: 响应体文本
        """
        if self._body_cache['text'] is not None:
            return self._body_cache['text']
        
        # 根据响应类型获取文本
        if hasattr(self.original_response, 'text'):
            # requests响应
            self._body_cache['text'] = self.original_response.text
        else:
            # aiohttp响应
            self._body_cache['text'] = await self.original_response.text()
        
        return self._body_cache['text']
    
    async def json_async(self) -> Any:
        """异步获取响应体JSON
        
        Returns:
            Any: 解析后的JSON对象
        
        Raises:
            json.JSONDecodeError: 解析JSON失败
        """
        if self._body_cache['json'] is not None:
            return self._body_cache['json']
        
        try:
            text = await self.text_async()
            self._body_cache['json'] = json.loads(text)
            return self._body_cache['json']
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"解析JSON失败: {str(e)}", e.doc, e.pos)
    
    async def bytes_async(self) -> bytes:
        """异步获取响应体字节
        
        Returns:
            bytes: 响应体字节
        """
        if self._body_cache['bytes'] is not None:
            return self._body_cache['bytes']
        
        # 根据响应类型获取字节
        if hasattr(self.original_response, 'content'):
            # requests响应
            self._body_cache['bytes'] = self.original_response.content
        else:
            # aiohttp响应
            self._body_cache['bytes'] = await self.original_response.read()
        
        return self._body_cache['bytes']
    
    def is_content_type(self, content_type: str) -> bool:
        """检查响应是否包含指定的内容类型
        
        Args:
            content_type: 内容类型
            
        Returns:
            bool: 是否包含指定的内容类型
        """
        response_content_type = self.headers.get('content-type', '')
        return content_type.lower() in response_content_type.lower()
    
    def is_json(self) -> bool:
        """检查响应是否为JSON
        
        Returns:
            bool: 是否为JSON
        """
        return self.is_content_type('application/json')
    
    def is_text(self) -> bool:
        """检查响应是否为文本
        
        Returns:
            bool: 是否为文本
        """
        return self.is_content_type('text/')
    
    def is_html(self) -> bool:
        """检查响应是否为HTML
        
        Returns:
            bool: 是否为HTML
        """
        return self.is_content_type('text/html')
    
    def is_xml(self) -> bool:
        """检查响应是否为XML
        
        Returns:
            bool: 是否为XML
        """
        return self.is_content_type('application/xml') or self.is_content_type('text/xml')
    
    def raise_for_status(self):
        """如果响应状态码表示HTTP错误，则抛出异常
        
        Raises:
            HTTPError: HTTP错误
        """
        if not self.ok:
            import requests
            raise requests.exceptions.HTTPError(
                f"HTTP错误: {self.status_code} {self.reason}",
                response=self
            )
        
        return self