/**
 * Modern Requests Library
 * 一个现代化高效的HTTP请求库
 */

const Request = require('./lib/request');
const Response = require('./lib/response');
const Session = require('./lib/session');
const utils = require('./lib/utils');

/**
 * 创建一个新的请求实例
 * @param {Object} options - 请求选项
 * @returns {Request} 请求实例
 */
function createRequest(options = {}) {
  return new Request(options);
}

/**
 * 发送GET请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function get(url, options = {}) {
  return new Request({ ...options, method: 'GET' }).send(url);
}

/**
 * 发送POST请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function post(url, options = {}) {
  return new Request({ ...options, method: 'POST' }).send(url);
}

/**
 * 发送PUT请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function put(url, options = {}) {
  return new Request({ ...options, method: 'PUT' }).send(url);
}

/**
 * 发送DELETE请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function del(url, options = {}) {
  return new Request({ ...options, method: 'DELETE' }).send(url);
}

/**
 * 发送PATCH请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function patch(url, options = {}) {
  return new Request({ ...options, method: 'PATCH' }).send(url);
}

/**
 * 发送HEAD请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function head(url, options = {}) {
  return new Request({ ...options, method: 'HEAD' }).send(url);
}

/**
 * 发送OPTIONS请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Response} 响应对象
 */
function options(url, options = {}) {
  return new Request({ ...options, method: 'OPTIONS' }).send(url);
}

/**
 * 异步发送GET请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function getAsync(url, options = {}) {
  return new Request({ ...options, method: 'GET' }).sendAsync(url);
}

/**
 * 异步发送POST请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function postAsync(url, options = {}) {
  return new Request({ ...options, method: 'POST' }).sendAsync(url);
}

/**
 * 异步发送PUT请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function putAsync(url, options = {}) {
  return new Request({ ...options, method: 'PUT' }).sendAsync(url);
}

/**
 * 异步发送DELETE请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function delAsync(url, options = {}) {
  return new Request({ ...options, method: 'DELETE' }).sendAsync(url);
}

/**
 * 异步发送PATCH请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function patchAsync(url, options = {}) {
  return new Request({ ...options, method: 'PATCH' }).sendAsync(url);
}

/**
 * 异步发送HEAD请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function headAsync(url, options = {}) {
  return new Request({ ...options, method: 'HEAD' }).sendAsync(url);
}

/**
 * 异步发送OPTIONS请求
 * @param {string} url - 请求URL
 * @param {Object} options - 请求选项
 * @returns {Promise<Response>} Promise响应对象
 */
function optionsAsync(url, options = {}) {
  return new Request({ ...options, method: 'OPTIONS' }).sendAsync(url);
}

/**
 * 创建一个新的会话实例
 * @param {Object} options - 会话选项
 * @returns {Session} 会话实例
 */
function createSession(options = {}) {
  return new Session(options);
}

module.exports = {
  // 核心类
  Request,
  Response,
  Session,
  
  // 工具函数
  createRequest,
  createSession,
  
  // 同步方法
  get,
  post,
  put,
  delete: del,
  patch,
  head,
  options,
  
  // 异步方法
  getAsync,
  postAsync,
  putAsync,
  deleteAsync: delAsync,
  patchAsync,
  headAsync,
  optionsAsync,
  
  // 工具函数
  utils
};