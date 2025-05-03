"""工具函数模块"""

import asyncio
import time
from urllib.parse import urlparse, urlencode, parse_qsl
from typing import Dict, Any, Callable, Union, Optional


def build_url(url: str, params: Dict[str, Any] = None) -> str:
    """构建URL并合并查询参数
    
    Args:
        url: 基础URL
        params: 查询参数
        
    Returns:
        str: 合并后的URL
    """
    if not params:
        return url
    
    parsed_url = urlparse(url)
    query_dict = dict(parse_qsl(parsed_url.query))
    
    # 合并现有查询参数和新参数
    query_dict.update(params)
    
    # 重建查询字符串
    query_string = urlencode(query_dict)
    
    # 重建URL
    parts = list(parsed_url)
    parts[4] = query_string
    
    return urlparse.urlunparse(parts)


def merge_deep(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """深度合并对象
    
    Args:
        target: 目标对象
        source: 源对象
        
    Returns:
        Dict[str, Any]: 合并后的对象
    """
    result = target.copy()
    
    for key, value in source.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_deep(result[key], value)
        else:
            result[key] = value
    
    return result


def detect_content_type(data: Any) -> str:
    """检测内容类型
    
    Args:
        data: 要检测的数据
        
    Returns:
        str: 内容类型
    """
    if data is None:
        return 'text/plain'
    
    if isinstance(data, str):
        # 尝试解析JSON
        try:
            import json
            json.loads(data)
            return 'application/json'
        except ValueError:
            # 不是JSON，假设是纯文本
            return 'text/plain'
    
    if isinstance(data, dict) or isinstance(data, list):
        # 对象默认为JSON
        return 'application/json'
    
    if isinstance(data, bytes):
        # 二进制数据
        return 'application/octet-stream'
    
    return 'text/plain'


def with_retry(fn: Callable, max_retries: int = 3, retry_delay: float = 1.0,
               should_retry: Callable[[Exception], bool] = None) -> Callable:
    """创建重试函数
    
    Args:
        fn: 要重试的函数
        max_retries: 最大重试次数
        retry_delay: 重试延迟（秒）
        should_retry: 判断是否应该重试的函数
        
    Returns:
        Callable: 包装后的函数
    """
    if should_retry is None:
        # 默认重试所有异常
        should_retry = lambda e: True
    
    async def async_wrapper(*args, **kwargs):
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(fn):
                    return await fn(*args, **kwargs)
                else:
                    return fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                # 检查是否应该重试
                if attempt < max_retries and should_retry(e):
                    # 等待重试延迟
                    await asyncio.sleep(retry_delay)
                    continue
                
                break
        
        raise last_error
    
    def sync_wrapper(*args, **kwargs):
        last_error = None
        
        for attempt in range(max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(fn):
                    loop = asyncio.new_event_loop()
                    try:
                        return loop.run_until_complete(fn(*args, **kwargs))
                    finally:
                        loop.close()
                else:
                    return fn(*args, **kwargs)
            except Exception as e:
                last_error = e
                
                # 检查是否应该重试
                if attempt < max_retries and should_retry(e):
                    # 等待重试延迟
                    time.sleep(retry_delay)
                    continue
                
                break
        
        raise last_error
    
    # 根据原函数类型返回相应的包装函数
    if asyncio.iscoroutinefunction(fn):
        return async_wrapper
    else:
        return sync_wrapper


def with_timeout(fn: Callable, timeout: float) -> Callable:
    """创建超时函数
    
    Args:
        fn: 要添加超时的函数
        timeout: 超时时间（秒）
        
    Returns:
        Callable: 包装后的函数
    """
    async def async_wrapper(*args, **kwargs):
        try:
            # 创建任务
            task = asyncio.create_task(fn(*args, **kwargs))
            
            # 等待任务完成或超时
            return await asyncio.wait_for(task, timeout=timeout)
        except asyncio.TimeoutError:
            # 取消任务
            task.cancel()
            raise TimeoutError(f"操作超时（{timeout}秒）")
    
    def sync_wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(async_wrapper(*args, **kwargs))
        finally:
            loop.close()
    
    # 根据原函数类型返回相应的包装函数
    if asyncio.iscoroutinefunction(fn):
        return async_wrapper
    else:
        return sync_wrapper


async def parse_response_async(response):
    """异步解析响应内容
    
    Args:
        response: 响应对象
        
    Returns:
        Any: 解析后的响应内容
    """
    content_type = response.headers.get('content-type', '')
    
    if 'application/json' in content_type:
        return await response.json_async()
    
    if 'text/' in content_type:
        return await response.text_async()
    
    # 默认返回字节
    return await response.bytes_async()


def parse_response(response):
    """解析响应内容
    
    Args:
        response: 响应对象
        
    Returns:
        Any: 解析后的响应内容
    """
    content_type = response.headers.get('content-type', '')
    
    if 'application/json' in content_type:
        return response.json()
    
    if 'text/' in content_type:
        return response.text()
    
    # 默认返回字节
    return response.bytes()


class Cache:
    """简单的缓存实现"""
    
    def __init__(self, max_size=100, ttl=300):
        """初始化缓存
        
        Args:
            max_size: 最大缓存条目数
            ttl: 缓存生存时间（秒）
        """
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key):
        """获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            Any: 缓存值，如果不存在或过期则返回None
        """
        if key not in self.cache:
            return None
        
        # 检查是否过期
        if time.time() - self.timestamps[key] > self.ttl:
            # 删除过期缓存
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key, value):
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
        """
        # 如果缓存已满，删除最旧的条目
        if len(self.cache) >= self.max_size and key not in self.cache:
            oldest_key = min(self.timestamps, key=self.timestamps.get)
            del self.cache[oldest_key]
            del self.timestamps[oldest_key]
        
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()
        self.timestamps.clear()


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, calls_per_second=10):
        """初始化速率限制器
        
        Args:
            calls_per_second: 每秒允许的调用次数
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call_time = 0
    
    async def wait(self):
        """等待直到可以进行下一次调用"""
        current_time = time.time()
        elapsed = current_time - self.last_call_time
        
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            await asyncio.sleep(wait_time)
        
        self.last_call_time = time.time()
    
    def wait_sync(self):
        """同步等待直到可以进行下一次调用"""
        current_time = time.time()
        elapsed = current_time - self.last_call_time
        
        if elapsed < self.min_interval:
            wait_time = self.min_interval - elapsed
            time.sleep(wait_time)
        
        self.last_call_time = time.time()