# Modern Requests Library

这是一个现代化高效的Python HTTP请求库，提供了类似于Python原生requests库的简洁API，但增加了更多高级功能。

## 特性

- 简单易用的API，保持与requests库相似的接口
- 同时支持同步和异步请求
- 智能重试机制和错误处理
- 会话管理和Cookie持久化
- 请求/响应钩子和中间件系统
- 内置缓存支持
- 速率限制控制
- 超时控制和并发请求池
- 自动JSON处理
- 代理支持和身份验证

## 安装

```bash
pip install modern-requests
```

## 基本用法

### 简单请求

```python
from modern_requests import get, post

# 发送GET请求
response = get('https://api.example.com/users')
print(response.status_code)  # 200
print(response.json())  # 解析JSON响应

# 发送带参数的GET请求
response = get('https://api.example.com/users', params={'page': 1, 'limit': 10})

# 发送POST请求
response = post('https://api.example.com/users', 
                json={'name': '张三', 'email': 'zhangsan@example.com'})
```

### 异步请求

```python
import asyncio
from modern_requests import get_async, post_async

async def fetch_data():
    # 发送异步GET请求
    response = await get_async('https://api.example.com/users')
    print(response.status_code)
    data = await response.json_async()
    print(data)
    
    # 并发请求
    tasks = [
        get_async('https://api.example.com/users/1'),
        get_async('https://api.example.com/users/2'),
        get_async('https://api.example.com/users/3')
    ]
    responses = await asyncio.gather(*tasks)
    for resp in responses:
        print(await resp.json_async())

# 运行异步函数
asyncio.run(fetch_data())
```

### 会话管理

```python
from modern_requests import create_session

# 创建会话
session = create_session()

# 设置会话级别的请求头
session.options['headers'] = {
    'User-Agent': 'Modern-Requests/1.0',
    'Accept-Language': 'zh-CN'
}

# 使用会话发送请求
response1 = session.get('https://api.example.com/users/1')
response2 = session.get('https://api.example.com/users/2')  # 自动使用相同的会话设置

# 查看会话的Cookie
print(session.get_cookies())

# 使用上下文管理器自动关闭会话
with create_session() as session:
    response = session.get('https://api.example.com/users')
```

## 高级功能

### 重试机制

```python
from modern_requests import get
from modern_requests.utils import with_retry

# 内置重试
response = get('https://api.example.com/users', 
              max_retries=3,  # 最多重试3次
              retry_delay=1)  # 重试间隔1秒

# 自定义重试条件
def should_retry(error):
    # 只在网络错误或5xx错误时重试
    if hasattr(error, 'response') and error.response:
        return 500 <= error.response.status_code < 600
    return True  # 网络错误等情况

# 使用工具函数包装
retry_get = with_retry(get, max_retries=3, retry_delay=0.5, should_retry=should_retry)
response = retry_get('https://api.example.com/users')
```

### 中间件系统

```python
from modern_requests import create_request
from datetime import datetime

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
response = request.send('https://api.example.com/users')
```

### 缓存系统

```python
from modern_requests import create_session
from modern_requests.utils import Cache

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

# 使用带缓存的会话
response1 = session.get('https://api.example.com/users')  # 未缓存
response2 = session.get('https://api.example.com/users')  # 从缓存获取
```

### 速率限制

```python
from modern_requests import get
from modern_requests.utils import RateLimiter

# 创建速率限制器，限制为每秒2个请求
limiter = RateLimiter(calls_per_second=2)

# 发送多个请求
for i in range(5):
    # 等待直到可以发送请求
    limiter.wait_sync()
    
    # 发送请求
    response = get(f'https://api.example.com/users/{i+1}')
    print(f'请求 {i+1} 状态码: {response.status_code}')
```

### 并发请求池

```python
import asyncio
from modern_requests import get_async

async def concurrent_pool_example():
    # 创建一组请求
    urls = [
        f'https://api.example.com/users/{i}'
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
    responses = await asyncio.gather(*tasks)
    print(f'获取到 {len(responses)} 个响应')

# 运行并发请求
asyncio.run(concurrent_pool_example())
```

## 与原生requests库的区别

1. **同时支持同步和异步API**：提供了与requests相似的同步API，同时增加了异步API支持。
2. **内置中间件系统**：可以轻松添加请求前和响应后的处理钩子。
3. **高级缓存支持**：内置缓存系统，可以轻松缓存请求结果。
4. **速率限制**：内置速率限制器，防止请求过于频繁。
5. **智能重试**：更灵活的重试机制，可以自定义重试条件。
6. **并发控制**：提供了并发请求池，可以控制并发请求数量。

## 贡献

欢迎贡献代码、报告问题或提出改进建议！

## 许可证

MIT