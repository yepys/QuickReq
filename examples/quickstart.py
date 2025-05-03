#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modern Requests Library 快速入门示例
"""

import asyncio

# 导入库
from modern_requests import get, post, get_async, create_session


def sync_examples():
    """同步请求示例"""
    print("\n=== 同步请求示例 ===")
    
    # 基本GET请求
    response = get("https://httpbin.org/get")
    print(f"状态码: {response.status_code}")
    print(f"响应类型: {response.headers.get('content-type')}")
    print("响应数据:", response.json())
    
    # 带参数的GET请求
    response = get("https://httpbin.org/get", params={"name": "张三", "age": 25})
    print("\n带参数的GET请求:")
    print(f"URL: {response.url}")
    print("参数回显:", response.json().get("args"))
    
    # POST请求发送JSON数据
    response = post("https://httpbin.org/post", json={"name": "李四", "age": 30})
    print("\nPOST请求发送JSON:")
    print(f"状态码: {response.status_code}")
    print("发送的数据:", response.json().get("json"))
    
    # 使用会话保持Cookie
    print("\n使用会话:")
    with create_session() as session:
        # 设置会话级别的请求头
        session.options['headers'] = {
            'User-Agent': 'Modern-Requests/1.0',
            'Accept-Language': 'zh-CN'
        }
        
        # 发送请求
        response = session.get("https://httpbin.org/cookies/set?name=value")
        print(f"设置Cookie状态码: {response.status_code}")
        
        # 查看Cookie
        response = session.get("https://httpbin.org/cookies")
        print("会话Cookie:", response.json())


async def async_examples():
    """异步请求示例"""
    print("\n=== 异步请求示例 ===")
    
    # 基本异步GET请求
    response = await get_async("https://httpbin.org/get")
    data = await response.json_async()
    print(f"状态码: {response.status_code}")
    print("响应数据:", data)
    
    # 并发请求
    print("\n并发请求:")
    urls = [
        "https://httpbin.org/get?id=1",
        "https://httpbin.org/get?id=2",
        "https://httpbin.org/get?id=3"
    ]
    
    tasks = [get_async(url) for url in urls]
    responses = await asyncio.gather(*tasks)
    
    for i, response in enumerate(responses, 1):
        print(f"请求 {i} 状态码: {response.status_code}")
        data = await response.json_async()
        print(f"请求 {i} 参数: {data.get('args')}")


def main():
    """主函数"""
    print("Modern Requests Library 快速入门")
    print("================================")
    
    # 运行同步示例
    sync_examples()
    
    # 运行异步示例
    asyncio.run(async_examples())
    
    print("\n快速入门示例完成！")


if __name__ == "__main__":
    main()