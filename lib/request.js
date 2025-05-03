/**
 * Request类 - 处理HTTP请求
 */

const fetch = require('node-fetch');
const AbortController = require('abort-controller');
const FormData = require('form-data');
const { URL } = require('url');
const Response = require('./response');
const utils = require('./utils');

class Request {
  /**
   * 创建一个新的请求实例
   * @param {Object} options - 请求选项
   */
  constructor(options = {}) {
    this.options = {
      method: 'GET',
      headers: {},
      timeout: 30000, // 默认30秒超时
      maxRetries: 3,  // 默认最多重试3次
      retryDelay: 1000, // 重试间隔1秒
      validateStatus: status => status >= 200 && status < 300,
      followRedirect: true,
      maxRedirects: 5,
      ...options
    };

    // 请求和响应钩子
    this.hooks = {
      beforeRequest: [],
      afterResponse: []
    };

    // 合并用户提供的钩子
    if (options.hooks) {
      for (const hookType in options.hooks) {
        if (Array.isArray(options.hooks[hookType])) {
          this.hooks[hookType] = [
            ...this.hooks[hookType],
            ...options.hooks[hookType]
          ];
        }
      }
    }
  }

  /**
   * 添加请求前钩子
   * @param {Function} hook - 钩子函数
   * @returns {Request} 当前请求实例
   */
  beforeRequest(hook) {
    this.hooks.beforeRequest.push(hook);
    return this;
  }

  /**
   * 添加响应后钩子
   * @param {Function} hook - 钩子函数
   * @returns {Request} 当前请求实例
   */
  afterResponse(hook) {
    this.hooks.afterResponse.push(hook);
    return this;
  }

  /**
   * 准备请求选项
   * @param {string} url - 请求URL
   * @returns {Object} 处理后的请求选项
   */
  prepareOptions(url) {
    const options = { ...this.options };
    const parsedUrl = new URL(url);
    
    // 处理查询参数
    if (options.params) {
      for (const [key, value] of Object.entries(options.params)) {
        parsedUrl.searchParams.append(key, value);
      }
      delete options.params;
    }
    
    // 处理请求体
    if (options.json) {
      options.body = JSON.stringify(options.json);
      options.headers = {
        'Content-Type': 'application/json',
        ...options.headers
      };
      delete options.json;
    } else if (options.form) {
      const formBody = new URLSearchParams();
      for (const [key, value] of Object.entries(options.form)) {
        formBody.append(key, value);
      }
      options.body = formBody;
      options.headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        ...options.headers
      };
      delete options.form;
    } else if (options.formData) {
      const formData = new FormData();
      for (const [key, value] of Object.entries(options.formData)) {
        formData.append(key, value);
      }
      options.body = formData;
      // FormData会自动设置Content-Type和boundary
      delete options.formData;
    }
    
    // 移除不是fetch API的选项
    const fetchOptions = { ...options };
    delete fetchOptions.timeout;
    delete fetchOptions.maxRetries;
    delete fetchOptions.retryDelay;
    delete fetchOptions.validateStatus;
    delete fetchOptions.followRedirect;
    delete fetchOptions.maxRedirects;
    delete fetchOptions.hooks;
    
    return {
      url: parsedUrl.toString(),
      fetchOptions,
      timeout: options.timeout,
      maxRetries: options.maxRetries,
      retryDelay: options.retryDelay,
      validateStatus: options.validateStatus,
      followRedirect: options.followRedirect,
      maxRedirects: options.maxRedirects
    };
  }

  /**
   * 执行请求前钩子
   * @param {Object} options - 请求选项
   * @returns {Object} 处理后的请求选项
   */
  async runBeforeRequestHooks(options) {
    let currentOptions = options;
    
    for (const hook of this.hooks.beforeRequest) {
      currentOptions = await hook(currentOptions) || currentOptions;
    }
    
    return currentOptions;
  }

  /**
   * 执行响应后钩子
   * @param {Response} response - 响应对象
   * @returns {Response} 处理后的响应对象
   */
  async runAfterResponseHooks(response) {
    let currentResponse = response;
    
    for (const hook of this.hooks.afterResponse) {
      currentResponse = await hook(currentResponse) || currentResponse;
    }
    
    return currentResponse;
  }

  /**
   * 发送同步请求
   * @param {string} url - 请求URL
   * @returns {Response} 响应对象
   */
  send(url) {
    const promise = this.sendAsync(url);
    // 同步API，但内部使用异步实现
    // 在实际应用中，应该使用异步API
    // 这里仅为了提供类似同步API的接口
    return utils.syncPromise(promise);
  }

  /**
   * 发送异步请求
   * @param {string} url - 请求URL
   * @returns {Promise<Response>} Promise响应对象
   */
  async sendAsync(url) {
    let preparedOptions = this.prepareOptions(url);
    preparedOptions = await this.runBeforeRequestHooks(preparedOptions);
    
    const { url: finalUrl, fetchOptions, timeout, maxRetries, retryDelay, validateStatus } = preparedOptions;
    
    let retries = 0;
    let lastError;
    
    while (retries <= maxRetries) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        
        fetchOptions.signal = controller.signal;
        
        const fetchResponse = await fetch(finalUrl, fetchOptions);
        clearTimeout(timeoutId);
        
        const response = new Response(fetchResponse);
        
        // 验证状态码
        if (!validateStatus(response.statusCode)) {
          throw new Error(`请求失败，状态码: ${response.statusCode}`);
        }
        
        // 运行响应后钩子
        return await this.runAfterResponseHooks(response);
      } catch (error) {
        lastError = error;
        
        // 如果是超时或网络错误，尝试重试
        if (error.name === 'AbortError' || error.type === 'system') {
          retries++;
          if (retries <= maxRetries) {
            // 等待重试延迟
            await new Promise(resolve => setTimeout(resolve, retryDelay));
            continue;
          }
        } else {
          // 其他错误直接抛出
          break;
        }
      }
    }
    
    throw lastError || new Error('请求失败');
  }
}

module.exports = Request;