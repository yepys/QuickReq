/**
 * 工具函数模块
 */

const { URL } = require('url');

/**
 * 同步执行Promise
 * 注意：这只是一个模拟同步API的辅助函数，实际应用中应该使用异步API
 * @param {Promise} promise - 要同步执行的Promise
 * @returns {any} Promise的结果
 */
function syncPromise(promise) {
  let result;
  let error;
  let completed = false;
  
  // 使用同步方式执行异步Promise
  promise.then(
    value => {
      result = value;
      completed = true;
    },
    err => {
      error = err;
      completed = true;
    }
  );
  
  // 等待Promise完成
  while (!completed) {
    // 这是一个阻塞操作，仅用于演示
    // 实际应用中应该使用异步API
  }
  
  if (error) {
    throw error;
  }
  
  return result;
}

/**
 * 解析URL并合并查询参数
 * @param {string} url - 基础URL
 * @param {Object} params - 查询参数
 * @returns {string} 合并后的URL
 */
function buildUrl(url, params = {}) {
  const parsedUrl = new URL(url);
  
  for (const [key, value] of Object.entries(params)) {
    parsedUrl.searchParams.append(key, value);
  }
  
  return parsedUrl.toString();
}

/**
 * 深度合并对象
 * @param {Object} target - 目标对象
 * @param {Object} source - 源对象
 * @returns {Object} 合并后的对象
 */
function mergeDeep(target, source) {
  const result = { ...target };
  
  for (const key in source) {
    if (source[key] instanceof Object && key in target && target[key] instanceof Object) {
      result[key] = mergeDeep(target[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  
  return result;
}

/**
 * 检测内容类型
 * @param {any} data - 要检测的数据
 * @returns {string} 内容类型
 */
function detectContentType(data) {
  if (data === null || data === undefined) {
    return 'text/plain';
  }
  
  if (typeof data === 'string') {
    // 尝试解析JSON
    try {
      JSON.parse(data);
      return 'application/json';
    } catch (e) {
      // 不是JSON，假设是纯文本
      return 'text/plain';
    }
  }
  
  if (typeof data === 'object') {
    // 对象默认为JSON
    return 'application/json';
  }
  
  return 'text/plain';
}

/**
 * 创建重试函数
 * @param {Function} fn - 要重试的函数
 * @param {Object} options - 重试选项
 * @returns {Function} 包装后的函数
 */
function withRetry(fn, options = {}) {
  const { maxRetries = 3, retryDelay = 1000, shouldRetry = () => true } = options;
  
  return async function(...args) {
    let lastError;
    
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        return await fn(...args);
      } catch (error) {
        lastError = error;
        
        // 检查是否应该重试
        if (attempt < maxRetries && shouldRetry(error)) {
          // 等待重试延迟
          await new Promise(resolve => setTimeout(resolve, retryDelay));
          continue;
        }
        
        break;
      }
    }
    
    throw lastError;
  };
}

/**
 * 创建超时函数
 * @param {Function} fn - 要添加超时的函数
 * @param {number} timeout - 超时时间（毫秒）
 * @returns {Function} 包装后的函数
 */
function withTimeout(fn, timeout) {
  return async function(...args) {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`操作超时（${timeout}ms）`));
      }, timeout);
      
      fn(...args)
        .then(result => {
          clearTimeout(timeoutId);
          resolve(result);
        })
        .catch(error => {
          clearTimeout(timeoutId);
          reject(error);
        });
    });
  };
}

/**
 * 解析响应内容
 * @param {Response} response - 响应对象
 * @returns {Promise<any>} 解析后的响应内容
 */
async function parseResponse(response) {
  const contentType = response.headers['content-type'] || '';
  
  if (contentType.includes('application/json')) {
    return response.jsonAsync();
  }
  
  if (contentType.includes('text/')) {
    return response.textAsync();
  }
  
  // 默认返回buffer
  return response.bufferAsync();
}

module.exports = {
  syncPromise,
  buildUrl,
  mergeDeep,
  detectContentType,
  withRetry,
  withTimeout,
  parseResponse
};