#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modern Requests Library 高级用法示例
"""

import asyncio
import time
import json
from datetime import datetime

# 导入库
from modern_requests import (
    get, post, create_request, create_session,
    get_async, post_async
)
from modern_requests.utils import Cache, RateLimiter, with_retry, with_timeout

# 中间件系统示例
def middleware_example():
    print('\n=== 中间件系统示例 ===')
    try:
        # 创建请求实例
        request = create_request()
        
        # 添加日志中间件
        def logging_middleware(options):
            print(f'[{datetime.now()}] 发送 {options.get("method", "GET")} 请求到 {options["url"]}')
            return options
        
        # 添加计时中间件
        def timing_middleware(options):
            options['_start_time'] = time.time()
            return options
        
        # 添加响应处理中间件
        def response_timing_middleware(response):
            if hasattr(response, '_start_time'):
                duration = time.time() - response._start_time
                print(f'请求耗时: {duration:.4f}秒')
            return response
        
        # 注册中间件
        request.before_request(logging_middleware)
        request.before_request(timing_middleware)
        request.after_response(response_timing_middleware)
        
        # 发送请求
        response = request.send('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 高级重试机制示例
def advanced_retry_example():
    print('\n=== 高级重试机制示例 ===')
    try:
        # 自定义重试条件
        def should_retry(error):
            # 只在网络错误或5xx错误时重试
            if hasattr(error, 'response') and error.response:
                return 500 <= error.response.status_code < 600
            return True  # 网络错误等情况
        
        # 创建带自定义重试的请求
        response = get(
            'https://jsonplaceholder.typicode.com/posts/1',
            max_retries=3,
            retry_delay=0.5,
            # 在实际应用中，可以传入should_retry函数
        )
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
        
        # 使用工具函数包装
        retry_get = with_retry(get, max_retries=3, retry_delay=0.5, should_retry=should_retry)
        response = retry_get('https://jsonplaceholder.typicode.com/posts/2')
        print(f'使用with_retry包装后状态码: {response.status_code}')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 速率限制示例
def rate_limit_example():
    print('\n=== 速率限制示例 ===')
    try:
        # 创建速率限制器，限制为每秒2个请求
        limiter = RateLimiter(calls_per_second=2)
        
        # 发送多个请求
        for i in range(5):
            start_time = time.time()
            
            # 等待直到可以发送请求
            limiter.wait_sync()
            
            # 发送请求
            response = get(f'https://jsonplaceholder.typicode.com/posts/{i+1}')
            end_time = time.time()
            
            print(f'请求 {i+1} 状态码: {response.status_code}, 耗时: {end_time - start_time:.4f}秒')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 高级缓存示例
def advanced_cache_example():
    print('\n=== 高级缓存示例 ===')
    try:
        # 创建缓存
        cache = Cache(max_size=100, ttl=60)  # 最多100个条目，60秒过期
        
        # 创建会话
        session = create_session()
        
        # 添加缓存中间件
        def cache_middleware(options):
            # 只缓存GET请求
            if options.get('method', 'GET') != 'GET':
                return options
            
            url = options['url']
            cached_response = cache.get(url)
            
            if cached_response:
                print(f'从缓存获取: {url}')
                # 设置标记，跳过实际请求
                options['_use_cache'] = True
                options['_cached_response'] = cached_response
            else:
                print(f'未缓存: {url}')
            
            return options
        
        # 添加响应缓存中间件
        def response_cache_middleware(response):
            # 缓存GET请求的响应
            if hasattr(response, 'original_response') and \
               hasattr(response.original_response, 'request') and \
               response.original_response.request.method == 'GET':
                url = response.url
                cache.set(url, response)
                print(f'缓存响应: {url}')
            return response
        
        # 注册中间件
        session.hooks['before_request'].append(cache_middleware)
        session.hooks['after_response'].append(response_cache_middleware)
        
        # 第一次请求，未缓存
        print('\n第一次请求:')
        response1 = session.get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response1.status_code}')
        
        # 第二次请求，应该从缓存获取
        print('\n第二次请求:')
        response2 = session.get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response2.status_code}')
        
        # 不同URL，未缓存
        print('\n不同URL请求:')
        response3 = session.get('https://jsonplaceholder.typicode.com/posts/2')
        print(f'状态码: {response3.status_code}')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 超时控制示例
def timeout_example():
    print('\n=== 超时控制示例 ===')
    try:
        # 使用超时选项
        start_time = time.time()
        response = get(
            'https://jsonplaceholder.typicode.com/posts/1',
            timeout=2  # 2秒超时
        )
        end_time = time.time()
        print(f'请求完成，耗时: {end_time - start_time:.4f}秒')
        print(f'状态码: {response.status_code}')
        
        # 使用工具函数包装
        timeout_get = with_timeout(get, timeout=1.5)
        start_time = time.time()
        response = timeout_get('https://jsonplaceholder.typicode.com/posts/2')
        end_time = time.time()
        print(f'使用with_timeout包装后，耗时: {end_time - start_time:.4f}秒')
        print(f'状态码: {response.status_code}')
        
        # 尝试一个会超时的请求（模拟）
        try:
            print('\n尝试一个会超时的请求...')
            # 这里我们使用一个通常会很慢的请求，设置很短的超时时间
            # 注意：在实际运行中，这个请求可能不会超时，这只是一个示例
            timeout_get = with_timeout(get, timeout=0.001)  # 1毫秒，几乎肯定会超时
            response = timeout_get('https://httpbin.org/delay/2')  # 这个接口会延迟2秒返回
        except TimeoutError as e:
            print(f'预期的超时错误: {str(e)}')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 并发请求池示例
async def concurrent_pool_example():
    print('\n=== 并发请求池示例 ===')
    try:
        # 创建一组请求
        urls = [
            f'https://jsonplaceholder.typicode.com/posts/{i}'
            for i in range(1, 11)
        ]
        
        # 限制并发数为3
        semaphore = asyncio.Semaphore(3)
        
        async def fetch_with_limit(url):
            async with semaphore:
                print(f'开始请求: {url}')
                response = await get_async(url)
                print(f'完成请求: {url}, 状态码: {response.status_code}')
                return response
        
        # 创建任务
        tasks = [fetch_with_limit(url) for url in urls]
        
        # 执行所有任务
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f'所有请求完成，总耗时: {end_time - start_time:.4f}秒')
        print(f'获取到 {len(responses)} 个响应')
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 代理和身份验证示例
def proxy_auth_example():
    print('\n=== 代理和身份验证示例 ===')
    try:
        # 使用代理
        # 注意：这里使用的是示例代理地址，实际使用时需要替换为真实的代理
        print('代理示例 (仅演示，不会实际连接)'):
        print('get("https://api.example.com", proxies={"http": "http://proxy.example.com:8080", "https": "https://proxy.example.com:8080"})')
        
        # 基本身份验证
        print('\n基本身份验证示例 (使用httpbin服务)'):
        response = get(
            'https://httpbin.org/basic-auth/user/pass',
            auth=('user', 'pass')  # 用户名和密码
        )
        print(f'状态码: {response.status_code}')
        if response.ok:
            print('身份验证成功')
            print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 自定义适配器示例
def custom_adapter_example():
    print('\n=== 自定义适配器示例 ===')
    try:
        # 创建会话
        session = create_session()
        
        # 添加自定义适配器（模拟）
        print('在实际应用中，您可以创建自定义适配器来处理特殊协议或需求')
        print('例如：session.mount("special://", CustomAdapter())')
        
        # 正常请求示例
        response = session.get('https://jsonplaceholder.typicode.com/posts/1')
        print(f'状态码: {response.status_code}')
        print('响应数据:', response.json())
    except Exception as e:
        print(f'请求失败: {str(e)}')

# 运行所有同步示例
def run_sync_examples():
    middleware_example()
    advanced_retry_example()
    rate_limit_example()
    advanced_cache_example()
    timeout_example()
    proxy_auth_example()
    custom_adapter_example()

# 运行所有异步示例
async def run_async_examples():
    await concurrent_pool_example()

# 主函数
def main():
    print('开始运行Modern Requests高级示例...')
    
    # 运行同步示例
    run_sync_examples()
    
    # 运行异步示例
    asyncio.run(run_async_examples())
    
    print('\n所有高级示例执行完成！')

if __name__ == '__main__':
    main()