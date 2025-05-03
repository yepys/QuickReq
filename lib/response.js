/**
 * Response类 - 处理HTTP响应
 */

class Response {
  /**
   * 创建一个新的响应实例
   * @param {Object} fetchResponse - fetch API的响应对象
   */
  constructor(fetchResponse) {
    this.originalResponse = fetchResponse;
    this.statusCode = fetchResponse.status;
    this.statusText = fetchResponse.statusText;
    this.headers = this._parseHeaders(fetchResponse.headers);
    this.url = fetchResponse.url;
    this.ok = fetchResponse.ok;
    this.redirected = fetchResponse.redirected;
    this.type = fetchResponse.type;
    
    // 缓存响应体，避免多次解析
    this._bodyCache = {
      text: null,
      json: null,
      buffer: null
    };
  }

  /**
   * 解析响应头
   * @param {Headers} headers - fetch API的Headers对象
   * @returns {Object} 解析后的响应头对象
   * @private
   */
  _parseHeaders(headers) {
    const result = {};
    headers.forEach((value, key) => {
      result[key.toLowerCase()] = value;
    });
    return result;
  }

  /**
   * 获取响应体文本
   * @returns {string} 响应体文本
   */
  text() {
    if (this._bodyCache.text !== null) {
      return this._bodyCache.text;
    }
    
    // 同步API，但内部使用异步实现
    // 在实际应用中，应该使用异步API
    const textPromise = this.originalResponse.clone().text();
    this._bodyCache.text = textPromise.then ? textPromise : Promise.resolve(textPromise);
    return this._bodyCache.text;
  }

  /**
   * 获取响应体JSON
   * @returns {Object} 解析后的JSON对象
   */
  json() {
    if (this._bodyCache.json !== null) {
      return this._bodyCache.json;
    }
    
    try {
      const text = this.text();
      this._bodyCache.json = JSON.parse(text);
      return this._bodyCache.json;
    } catch (error) {
      throw new Error(`解析JSON失败: ${error.message}`);
    }
  }

  /**
   * 获取响应体Buffer
   * @returns {Buffer} 响应体Buffer
   */
  buffer() {
    if (this._bodyCache.buffer !== null) {
      return this._bodyCache.buffer;
    }
    
    // 同步API，但内部使用异步实现
    const bufferPromise = this.originalResponse.clone().buffer();
    this._bodyCache.buffer = bufferPromise.then ? bufferPromise : Promise.resolve(bufferPromise);
    return this._bodyCache.buffer;
  }

  /**
   * 异步获取响应体文本
   * @returns {Promise<string>} Promise响应体文本
   */
  async textAsync() {
    if (this._bodyCache.text !== null) {
      return this._bodyCache.text;
    }
    
    this._bodyCache.text = await this.originalResponse.clone().text();
    return this._bodyCache.text;
  }

  /**
   * 异步获取响应体JSON
   * @returns {Promise<Object>} Promise解析后的JSON对象
   */
  async jsonAsync() {
    if (this._bodyCache.json !== null) {
      return this._bodyCache.json;
    }
    
    try {
      const text = await this.textAsync();
      this._bodyCache.json = JSON.parse(text);
      return this._bodyCache.json;
    } catch (error) {
      throw new Error(`解析JSON失败: ${error.message}`);
    }
  }

  /**
   * 异步获取响应体Buffer
   * @returns {Promise<Buffer>} Promise响应体Buffer
   */
  async bufferAsync() {
    if (this._bodyCache.buffer !== null) {
      return this._bodyCache.buffer;
    }
    
    this._bodyCache.buffer = await this.originalResponse.clone().buffer();
    return this._bodyCache.buffer;
  }

  /**
   * 检查响应是否包含指定的内容类型
   * @param {string} contentType - 内容类型
   * @returns {boolean} 是否包含指定的内容类型
   */
  isContentType(contentType) {
    const responseContentType = this.headers['content-type'] || '';
    return responseContentType.toLowerCase().includes(contentType.toLowerCase());
  }

  /**
   * 检查响应是否为JSON
   * @returns {boolean} 是否为JSON
   */
  isJson() {
    return this.isContentType('application/json');
  }

  /**
   * 检查响应是否为文本
   * @returns {boolean} 是否为文本
   */
  isText() {
    return this.isContentType('text/');
  }

  /**
   * 检查响应是否为HTML
   * @returns {boolean} 是否为HTML
   */
  isHtml() {
    return this.isContentType('text/html');
  }

  /**
   * 检查响应是否为XML
   * @returns {boolean} 是否为XML
   */
  isXml() {
    return this.isContentType('application/xml') || this.isContentType('text/xml');
  }
}

module.exports = Response;