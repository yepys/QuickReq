#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modern Requests Library 基本功能测试
"""

import unittest
import asyncio
from unittest import mock

# 导入库
from modern_requests import (
    get, post, create_session,
    get_async, post_async
)
from modern_requests.response import Response


class MockResponse:
    """模拟响应对象"""
    
    def __init__(self, status_code=200, json_data=None, text_data="", headers=None):
        self.status = status_code
        self.status_code = status_code
        self.reason = "OK" if status_code == 200 else "Error"
        self.headers = headers or {"content-type": "application/json"}
        self._json_data = json_data
        self._text_data = text_data
        self.url = "https://example.com"
        self.history = []
        self.request = mock.MagicMock()
        self.request.method = "GET"
    
    async def json(self):
        return self._json_data
    
    async def text(self):
        return self._text_data
    
    async def read(self):
        return self._text_data.encode("utf-8")


class TestBasicFunctionality(unittest.TestCase):
    """测试基本功能"""
    
    @mock.patch("aiohttp.ClientSession.get")
    def test_get_request(self, mock_get):
        """测试GET请求"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=200,
            json_data={"id": 1, "name": "测试"}
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # 执行请求
        response = get("https://example.com/api")
        
        # 验证结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "测试"})
    
    @mock.patch("aiohttp.ClientSession.post")
    def test_post_request(self, mock_post):
        """测试POST请求"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=201,
            json_data={"success": True}
        )
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # 执行请求
        response = post(
            "https://example.com/api",
            json={"name": "新用户", "email": "user@example.com"}
        )
        
        # 验证结果
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"success": True})
    
    @mock.patch("aiohttp.ClientSession.get")
    def test_session(self, mock_get):
        """测试会话"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=200,
            json_data={"id": 1, "name": "测试"}
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # 创建会话并发送请求
        session = create_session()
        response = session.get("https://example.com/api")
        
        # 验证结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 1, "name": "测试"})
    
    @mock.patch("aiohttp.ClientSession.get")
    def test_request_with_params(self, mock_get):
        """测试带参数的请求"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=200,
            json_data=[{"id": 1}, {"id": 2}]
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # 执行请求
        response = get(
            "https://example.com/api",
            params={"page": 1, "limit": 10}
        )
        
        # 验证结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{"id": 1}, {"id": 2}])


class TestAsyncFunctionality(unittest.TestCase):
    """测试异步功能"""
    
    @mock.patch("aiohttp.ClientSession.get")
    def test_async_get(self, mock_get):
        """测试异步GET请求"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=200,
            json_data={"id": 1, "name": "测试"}
        )
        mock_get.return_value.__aenter__.return_value = mock_response
        
        # 执行异步请求
        async def run_test():
            response = await get_async("https://example.com/api")
            self.assertEqual(response.status_code, 200)
            data = await response.json_async()
            self.assertEqual(data, {"id": 1, "name": "测试"})
        
        # 运行异步测试
        asyncio.run(run_test())
    
    @mock.patch("aiohttp.ClientSession.post")
    def test_async_post(self, mock_post):
        """测试异步POST请求"""
        # 设置模拟响应
        mock_response = MockResponse(
            status_code=201,
            json_data={"success": True}
        )
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # 执行异步请求
        async def run_test():
            response = await post_async(
                "https://example.com/api",
                json={"name": "新用户", "email": "user@example.com"}
            )
            self.assertEqual(response.status_code, 201)
            data = await response.json_async()
            self.assertEqual(data, {"success": True})
        
        # 运行异步测试
        asyncio.run(run_test())


class TestResponseMethods(unittest.TestCase):
    """测试响应方法"""
    
    def test_response_methods(self):
        """测试响应对象的方法"""
        # 创建模拟响应
        mock_resp = MockResponse(
            status_code=200,
            json_data={"id": 1, "name": "测试"},
            text_data="{\"id\": 1, \"name\": \"测试\"}",
            headers={"content-type": "application/json"}
        )
        
        # 创建响应对象
        response = Response(mock_resp)
        
        # 测试属性
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.reason, "OK")
        self.assertEqual(response.url, "https://example.com")
        self.assertTrue(response.ok)
        
        # 测试内容类型检查
        self.assertTrue(response.is_json())
        self.assertFalse(response.is_html())
        
        # 测试异步方法
        async def test_async_methods():
            text = await response.text_async()
            self.assertEqual(text, "{\"id\": 1, \"name\": \"测试\"}")
            
            json_data = await response.json_async()
            self.assertEqual(json_data, {"id": 1, "name": "测试"})
        
        # 运行异步测试
        asyncio.run(test_async_methods())


if __name__ == "__main__":
    unittest.main()