# QuickReq

这是一个现代化高效的HTTP请求库，类似于Python的requests库，但提供了更多高级功能和优化。支持JavaScript和Python两种语言版本，专注于简洁性和高性能。

## 特性

- 简单易用的API，保持与原生requests库相似的接口
- 同时支持同步和异步请求，性能优化
- 智能重试机制和增强的错误处理
- 会话管理和Cookie持久化
- 请求/响应钩子和中间件系统
- 内置高效缓存支持
- 精确的速率限制控制
- 优化的超时控制和并发请求池
- 自动JSON处理和序列化
- 压缩支持（gzip, deflate, brotli）
- 增强的代理支持和身份验证
- 流式响应处理
- 内存使用优化

## 安装

### JavaScript版本

```bash
npm install quickreq
```

### Python版本

```bash
pip install quickreq
```

## 基本用法

### JavaScript版本

```javascript
const quickreq = require('quickreq');

// 同步请求
const response = quickreq.get('https://api.example.com/data');
console.log(response.statusCode);
console.log(response.json());

// 异步请求
quickreq.getAsync('https://api.example.com/data')
  .then(response => {
    console.log(response.statusCode);
    console.log(response.json());
  })
  .catch(error => {
    console.error('请求失败:', error);
  });

// 使用Promise和async/await
async function fetchData() {
  try {
    const response = await quickreq.getAsync('https://api.example.com/data');
    console.log(response.statusCode);
    console.log(response.json());
  } catch (error) {
    console.error('请求失败:', error);
  }
}
```

### Python版本

```python
from quickreq import get, post

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

#### 异步请求 (Python)

```python
import asyncio
from quickreq import get_async, post_async

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

## 高级用法

### JavaScript版本

```javascript
// 设置请求头和查询参数
const response = quickreq.get('https://api.example.com/search', {
  params: { q: 'javascript', limit: 10 },
  headers: { 'Accept-Language': 'zh-CN' }
});

// 发送POST请求与JSON数据
const response = quickreq.post('https://api.example.com/users', {
  json: { name: '张三', email: 'zhangsan@example.com' }
});

// 使用会话保持Cookie
const session = quickreq.createSession();
session.get('https://example.com/login');
session.post('https://example.com/login', {
  form: { username: 'user', password: 'pass' }
});

// 会话会自动保持Cookie
const profileResponse = session.get('https://example.com/profile');

// 并发请求控制
async function concurrentRequests() {
  const promises = [
    quickreq.getAsync('https://api.example.com/data/1'),
    quickreq.getAsync('https://api.example.com/data/2'),
    quickreq.getAsync('https://api.example.com/data/3'),
    quickreq.getAsync('https://api.example.com/data/4'),
    quickreq.getAsync('https://api.example.com/data/5')
  ];
  
  const responses = await Promise.all(promises);
  console.log(`获取到 ${responses.length} 个响应`);
  
  // 处理所有响应
  for (const response of responses) {
    const data = await response.jsonAsync();
    console.log(data);
  }
}

// 自定义重试逻辑
const fetchWithRetry = quickreq.utils.withRetry(
  async () => {
    return await quickreq.getAsync('https://api.example.com/data');
  },
  {
    maxRetries: 3,
    retryDelay: 500,
    shouldRetry: error => {
      // 只在网络错误或5xx错误时重试
      if (error.response) {
        return error.response.statusCode >= 500;
      }
      return true; // 网络错误等情况
    }
  }
);

// 流式处理大型响应
async function streamResponse() {
  const response = await quickreq.getAsync('https://api.example.com/large-data', {
    stream: true
  });
  
  const stream = response.body;
  let totalSize = 0;
  
  return new Promise((resolve, reject) => {
    stream.on('data', chunk => {
      totalSize += chunk.length;
      console.log(`接收数据块: ${chunk.length} 字节`);
    });
    
    stream.on('end', () => {
      console.log(`总共接收: ${totalSize} 字节`);
      resolve(totalSize);
    });
    
    stream.on('error', err => {
      reject(err);
    });
  });
}
```

### Python版本

#### 会话管理

```python
from quickreq import create_session

# 创建会话
session = create_session()

# 设置会话级别的请求头
session.options['headers'] = {
    'User-Agent': 'QuickReq/1.0',
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

#### 重试机制

```python
from quickreq import get
from quickreq.utils import with_retry

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

#### 中间件系统

```python
from quickreq import create_request
from datetime import datetime
import time

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

#### 缓存系统

```python
from quickreq import create_session
from quickreq.utils import Cache

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

#### 速率限制

```python
from quickreq import get
from quickreq.utils import RateLimiter

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

#### 并发请求池

```python
import asyncio
from quickreq import get_async

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

## Node.js 特有功能

### 流式请求和响应

```javascript
const fs = require('fs');
const quickreq = require('quickreq');

// 流式下载文件
async function downloadFile() {
  const response = await quickreq.getAsync('https://example.com/large-file.zip', {
    stream: true
  });
  
  const fileStream = fs.createWriteStream('downloaded-file.zip');
  response.body.pipe(fileStream);
  
  return new Promise((resolve, reject) => {
    fileStream.on('finish', () => {
      console.log('文件下载完成');
      resolve();
    });
    
    fileStream.on('error', err => {
      reject(err);
    });
  });
}

// 流式上传文件
async function uploadFile() {
  const fileStream = fs.createReadStream('large-file.zip');
  
  const response = await quickreq.postAsync('https://example.com/upload', {
    body: fileStream,
    headers: {
      'Content-Type': 'application/octet-stream'
    }
  });
  
  console.log(`上传状态: ${response.statusCode}`);
  return response;
}
```

### 事件驱动的请求

```javascript
const quickreq = require('quickreq');

// 创建请求实例
const request = quickreq.createRequest();

// 注册事件监听器
request.on('beforeRequest', options => {
  console.log(`准备发送请求到: ${options.url}`);
});

request.on('progress', (loaded, total) => {
  const percent = total ? Math.round((loaded / total) * 100) : 'unknown';
  console.log(`下载进度: ${percent}%`);
});

request.on('complete', response => {
  console.log(`请求完成，状态码: ${response.statusCode}`);
});

request.on('error', error => {
  console.error(`请求错误: ${error.message}`);
});

// 发送请求
request.send('https://example.com/api/data');
```

### 内存优化的大型响应处理

```javascript
const quickreq = require('quickreq');

async function processLargeResponse() {
  const response = await quickreq.getAsync('https://example.com/large-dataset', {
    stream: true,
    // 启用增量JSON解析
    incrementalJson: true
  });
  
  let count = 0;
  
  // 对于大型JSON数组，逐项处理
  for await (const item of response.jsonIterator()) {
    // 处理单个项目，避免将整个数组加载到内存
    processItem(item);
    count++;
    
    if (count % 1000 === 0) {
      console.log(`已处理 ${count} 个项目`);
    }
  }
  
  console.log(`总共处理了 ${count} 个项目`);
}

function processItem(item) {
  // 处理单个数据项
  console.log(`处理项目: ${item.id}`);
}
```

### WebSocket支持

```javascript
const quickreq = require('quickreq');

// 创建WebSocket连接
const ws = quickreq.createWebSocket('wss://echo.websocket.org');

// 连接打开时
ws.on('open', () => {
  console.log('WebSocket连接已打开');
  ws.send('Hello WebSocket!');
});

// 接收消息
ws.on('message', data => {
  console.log(`收到消息: ${data}`);
});

// 处理错误
ws.on('error', error => {
  console.error(`WebSocket错误: ${error.message}`);
});

// 连接关闭
ws.on('close', () => {
  console.log('WebSocket连接已关闭');
});

// 5秒后关闭连接
setTimeout(() => {
  ws.close();
}, 5000);
```

## 与原生requests库的区别

1. **同时支持同步和异步API**：提供了与requests相似的同步API，同时增加了异步API支持。
2. **内置中间件系统**：可以轻松添加请求前和响应后的处理钩子。
3. **高级缓存支持**：内置缓存系统，可以轻松缓存请求结果。
4. **速率限制**：内置速率限制器，防止请求过于频繁。
5. **智能重试**：更灵活的重试机制，可以自定义重试条件。
6. **并发控制**：提供了并发请求池，可以控制并发请求数量。
7. **多语言支持**：同时提供JavaScript和Python版本，API设计保持一致。
8. **流式处理**：优化的流式请求和响应处理，适合大型数据传输。
9. **内存优化**：针对大型响应的内存使用进行了优化。
10. **事件驱动**：Node.js版本提供了事件驱动的API，更符合JavaScript生态系统。
11. **WebSocket支持**：内置WebSocket客户端支持。

## 贡献

欢迎提交问题和Pull Request来帮助改进这个库。详细的贡献指南请参考[CONTRIBUTING.md](./CONTRIBUTING.md)文件。

## 许可证

MIT