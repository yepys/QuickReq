/**
 * Session类 - 管理HTTP会话和Cookie
 */

const Request = require('./request');
const utils = require('./utils');

class Session {
  /**
   * 创建一个新的会话实例
   * @param {Object} options - 会话选项
   */
  constructor(options = {}) {
    this.options = {
      ...options,
      headers: {
        ...options.headers
      }
    };
    
    // 存储会话Cookie
    this.cookies = {};
    
    // 添加Cookie管理钩子
    this.hooks = {
      beforeRequest: [
        this._attachCookies.bind(this)
      ],
      afterResponse: [
        this._saveCookies.bind(this)
      ]
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
   * 在请求前附加Cookie
   * @param {Object} options - 请求选项
   * @returns {Object} 处理后的请求选项
   * @private
   */
  _attachCookies(options) {
    const url = new URL(options.url);
    const domain = url.hostname;
    
    // 获取适用于当前域的Cookie
    const applicableCookies = Object.entries(this.cookies)
      .filter(([key, cookie]) => {
        // 检查域匹配
        if (!domain.endsWith(cookie.domain)) {
          return false;
        }
        
        // 检查路径匹配
        if (!url.pathname.startsWith(cookie.path)) {
          return false;
        }
        
        // 检查是否过期
        if (cookie.expires && new Date() > cookie.expires) {
          // 删除过期的Cookie
          delete this.cookies[key];
          return false;
        }
        
        // 检查是否需要安全连接
        if (cookie.secure && url.protocol !== 'https:') {
          return false;
        }
        
        return true;
      })
      .map(([key, cookie]) => `${key}=${cookie.value}`);
    
    // 如果有适用的Cookie，添加到请求头
    if (applicableCookies.length > 0) {
      options.fetchOptions.headers = options.fetchOptions.headers || {};
      options.fetchOptions.headers.Cookie = applicableCookies.join('; ');
    }
    
    return options;
  }

  /**
   * 保存响应中的Cookie
   * @param {Response} response - 响应对象
   * @returns {Response} 原始响应对象
   * @private
   */
  _saveCookies(response) {
    const setCookieHeaders = response.headers['set-cookie'];
    if (!setCookieHeaders) {
      return response;
    }
    
    // 处理可能是字符串或数组的Set-Cookie头
    const cookieStrings = Array.isArray(setCookieHeaders) 
      ? setCookieHeaders 
      : [setCookieHeaders];
    
    for (const cookieString of cookieStrings) {
      const parsedCookie = this._parseCookie(cookieString, response.url);
      if (parsedCookie) {
        this.cookies[parsedCookie.name] = parsedCookie;
      }
    }
    
    return response;
  }

  /**
   * 解析Cookie字符串
   * @param {string} cookieString - Cookie字符串
   * @param {string} url - 响应URL
   * @returns {Object|null} 解析后的Cookie对象
   * @private
   */
  _parseCookie(cookieString, url) {
    const parts = cookieString.split(';').map(part => part.trim());
    const [nameValue, ...attributes] = parts;
    
    const [name, value] = nameValue.split('=').map(s => s.trim());
    if (!name) {
      return null;
    }
    
    const parsedUrl = new URL(url);
    const cookie = {
      name,
      value,
      domain: parsedUrl.hostname,
      path: '/',
      secure: false,
      httpOnly: false,
      expires: null
    };
    
    // 解析Cookie属性
    for (const attr of attributes) {
      const [attrName, attrValue] = attr.split('=').map(s => s.trim());
      const lowerAttrName = attrName.toLowerCase();
      
      if (lowerAttrName === 'domain' && attrValue) {
        cookie.domain = attrValue.startsWith('.') ? attrValue.slice(1) : attrValue;
      } else if (lowerAttrName === 'path' && attrValue) {
        cookie.path = attrValue;
      } else if (lowerAttrName === 'expires' && attrValue) {
        cookie.expires = new Date(attrValue);
      } else if (lowerAttrName === 'max-age' && attrValue) {
        const seconds = parseInt(attrValue, 10);
        if (!isNaN(seconds)) {
          cookie.expires = new Date(Date.now() + seconds * 1000);
        }
      } else if (lowerAttrName === 'secure') {
        cookie.secure = true;
      } else if (lowerAttrName === 'httponly') {
        cookie.httpOnly = true;
      }
    }
    
    return cookie;
  }

  /**
   * 创建一个新的请求实例
   * @param {Object} options - 请求选项
   * @returns {Request} 请求实例
   */
  request(options = {}) {
    return new Request({
      ...this.options,
      ...options,
      hooks: {
        beforeRequest: [
          ...(this.hooks.beforeRequest || []),
          ...(options.hooks?.beforeRequest || [])
        ],
        afterResponse: [
          ...(this.hooks.afterResponse || []),
          ...(options.hooks?.afterResponse || [])
        ]
      }
    });
  }

  /**
   * 发送GET请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Response} 响应对象
   */
  get(url, options = {}) {
    return this.request({ ...options, method: 'GET' }).send(url);
  }

  /**
   * 发送POST请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Response} 响应对象
   */
  post(url, options = {}) {
    return this.request({ ...options, method: 'POST' }).send(url);
  }

  /**
   * 发送PUT请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Response} 响应对象
   */
  put(url, options = {}) {
    return this.request({ ...options, method: 'PUT' }).send(url);
  }

  /**
   * 发送DELETE请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Response} 响应对象
   */
  delete(url, options = {}) {
    return this.request({ ...options, method: 'DELETE' }).send(url);
  }

  /**
   * 发送PATCH请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Response} 响应对象
   */
  patch(url, options = {}) {
    return this.request({ ...options, method: 'PATCH' }).send(url);
  }

  /**
   * 异步发送GET请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Promise<Response>} Promise响应对象
   */
  getAsync(url, options = {}) {
    return this.request({ ...options, method: 'GET' }).sendAsync(url);
  }

  /**
   * 异步发送POST请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Promise<Response>} Promise响应对象
   */
  postAsync(url, options = {}) {
    return this.request({ ...options, method: 'POST' }).sendAsync(url);
  }

  /**
   * 异步发送PUT请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Promise<Response>} Promise响应对象
   */
  putAsync(url, options = {}) {
    return this.request({ ...options, method: 'PUT' }).sendAsync(url);
  }

  /**
   * 异步发送DELETE请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Promise<Response>} Promise响应对象
   */
  deleteAsync(url, options = {}) {
    return this.request({ ...options, method: 'DELETE' }).sendAsync(url);
  }

  /**
   * 异步发送PATCH请求
   * @param {string} url - 请求URL
   * @param {Object} options - 请求选项
   * @returns {Promise<Response>} Promise响应对象
   */
  patchAsync(url, options = {}) {
    return this.request({ ...options, method: 'PATCH' }).sendAsync(url);
  }

  /**
   * 清除所有会话Cookie
   */
  clearCookies() {
    this.cookies = {};
  }

  /**
   * 获取当前会话的所有Cookie
   * @returns {Object} Cookie对象
   */
  getCookies() {
    return { ...this.cookies };
  }

  /**
   * 设置Cookie
   * @param {string} name - Cookie名称
   * @param {string} value - Cookie值
   * @param {Object} options - Cookie选项
   */
  setCookie(name, value, options = {}) {
    this.cookies[name] = {
      name,
      value,
      domain: options.domain || '.example.com',
      path: options.path || '/',
      secure: options.secure || false,
      httpOnly: options.httpOnly || false,
      expires: options.expires || null
    };
  }
}

module.exports = Session;