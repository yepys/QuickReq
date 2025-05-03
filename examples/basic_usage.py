#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modern Requests Library 基本用法示例
"""

import asyncio
import time

# 导入库
from modern_requests import (
    get, post, put, delete, head, options,
    get_async, post_async, put_async, delete_async,
    create_session
)

# 基本GET请求示例
def basic_get_example():
    print('\n=== 基本GET请求示例 ===')
    try:
        # 同步GET请求
        response = get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response.status_code}')
        print(f'响应类型: {response.headers.get("content-type")}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 带参数的GET请求示例
def get_with_params_example():
    print('\n=== 带参数的GET请求示例 ===')
    try:
        # 带查询参数的GET请求
        response = get('https://jsonplaceholder.typicode.com/posts', params={'userId': 1, '_limit': 3})
        print(f'状态码: {response.status_code}')
        print(f'获取到 {len(response.json())} 条记录')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# POST请求示例
def post_example():
    print('\n=== POST请求示例 ===')
    try:
        # 发送JSON数据
        response = post('https://jsonplaceholder.typicode.com/posts', json={
            'title': '测试标题',
            'body': '测试内容',
            'userId': 1
        })
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 自定义请求头示例
def custom_headers_example():
    print('\n=== 自定义请求头示例 ===')
    try:
        response = get('https://jsonplaceholder.typicode.com/posts/1', headers={
            'X-Custom-Header': '自定义值',
            'Accept-Language': 'zh-CN'
        })
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 会话示例
def session_example():
    print('\n=== 会话示例 ===')
    try:
        # 创建会话
        session = create_session()
        
        # 设置会话级别的请求头
        session.options['headers'] = {
            'User-Agent': 'Modern-Requests/1.0',
            'Accept-Language': 'zh-CN'
        }
        
        # 第一个请求
        response1 = session.get('https://jsonplaceholder.typicode.com/posts/1')
        print('第一个请求状态码:', response1.status_code)
        
        # 第二个请求会自动使用相同的会话设置
        response2 = session.get('https://jsonplaceholder.typicode.com/posts/2')
        print('第二个请求状态码:', response2.status_code)
        
        # 查看会话的Cookie
        print('会话Cookie:', session.get_cookies())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 超时和重试示例
def timeout_and_retry_example():
    print('\n=== 超时和重试示例 ===')
    try:
        response = get('https://jsonplaceholder.typicode.com/posts/1', 
                      timeout=5,  # 5秒超时
                      max_retries=2,  # 最多重试2次
                      retry_delay=1  # 重试间隔1秒
                     )
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 请求钩子示例
def hooks_example():
    print('\n=== 请求钩子示例 ===')
    try:
        def before_request_hook(options):
            print('请求前钩子:', options['url'])
            # 可以修改请求选项
            if 'requests_options' in options and 'headers' in options['requests_options']:
                options['requests_options']['headers']['X-Hook-Added'] = 'true'
            return options

        def after_response_hook(response):
            print('响应后钩子:', response.status_code)
            # 可以修改响应
            return response

        response = get('https://jsonplaceholder.typicode.com/posts/1', hooks={
            'before_request': [before_request_hook],
            'after_response': [after_response_hook]
        })
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 异步请求示例
async def async_example():
    print('\n=== 异步请求示例 ===')
    try:
        # 并发发送多个请求
        tasks = [
            get_async('https://jsonplaceholder.typicode.com/posts/1'),
            get_async('https://jsonplaceholder.typicode.com/posts/2'),
            get_async('https://jsonplaceholder.typicode.com/posts/3')
        ]
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f'并发请求完成时间: {end_time - start_time:.2f}秒')
        print(f'获取到 {len(responses)} 个响应')
        
        for i, response in enumerate(responses, 1):
            print(f'响应 {i} 状态码: {response.status_code}')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 缓存示例
def cache_example():
    print('\n=== 缓存示例 ===')
    try:
        from modern_requests.utils import Cache
        
        # 创建缓存
        cache = Cache(max_size=100, ttl=60)  # 最多100个条目，60秒过期
        
        # 第一次请求，未缓存
        url = 'https://jsonplaceholder.typicode.com/posts/1'
        start_time = time.time()
        
        # 检查缓存
        cached_response = cache.get(url)
        if cached_response:
            print('从缓存获取响应')
            response = cached_response
        else:
            print('发送新请求')
            response = get(url)
            # 缓存响应
            cache.set(url, response)
        
        end_time = time.time()
        print(f'第一次请求时间: {end_time - start_time:.4f}秒')
        
        # 第二次请求，应该从缓存获取
        start_time = time.time()
        
        # 检查缓存
        cached_response = cache.get(url)
        if cached_response:
            print('从缓存获取响应')
            response = cached_response
        else:
            print('发送新请求')
            response = get(url)
            # 缓存响应
            cache.set(url, response)
        
        end_time = time.time()
        print(f'第二次请求时间: {end_time - start_time:.4f}秒')
        print(f'响应状态码: {response.status_code}')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 运行所有同步示例
def run_sync_examples():
    basic_get_example()
    get_with_params_example()
    post_example()
    custom_headers_example()
    session_example()
    timeout_and_retry_example()
    hooks_example()
    cache_example()

# 运行所有异步示例
async def run_async_examples():
    await async_example()

# 主函数
def main():
    print('开始运行Modern Requests示例...')
    
    # 运行同步示例
    run_sync_examples()
    
    # 运行异步示例
    asyncio.run(run_async_examples())
    
    print('\n所有示例执行完成！')

if __name__ == '__main__':
    main()