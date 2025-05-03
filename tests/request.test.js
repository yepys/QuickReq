/**
 * Modern Requests Library 测试文件
 */

const requests = require('../index');

// 模拟测试环境
const mockResponse = {
  status: 200,
  statusText: 'OK',
  headers: new Map([
    ['content-type', 'application/json'],
    ['set-cookie', 'session=123; Path=/; HttpOnly']
  ]),
  url: 'https://example.com/api',
  ok: true,
  redirected: false,
  type: 'basic',
  clone: function() { return this; },
  text: function() { return Promise.resolve('{"message":"测试成功"}'); },
  json: function() { return Promise.resolve({message: '测试成功'}); },
  buffer: function() { return Promise.resolve(Buffer.from('{"message":"测试成功"}')); }
};

// 模拟fetch函数
global.fetch = jest.fn().mockImplementation(() => {
  return Promise.resolve(mockResponse);
});

// 请求测试
describe('Request 类测试', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('应该能发送GET请求', async () => {
    const response = await requests.getAsync('https://example.com/api');
    
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith(
      'https://example.com/api',
      expect.objectContaining({ method: 'GET' })
    );
    
    expect(response.statusCode).toBe(200);
    expect(response.ok).toBe(true);
    
    const data = await response.jsonAsync();
    expect(data).toEqual({message: '测试成功'});
  });

  test('应该能发送带参数的GET请求', async () => {
    await requests.getAsync('https://example.com/api', {
      params: { id: 123, query: 'test' }
    });
    
    expect(global.fetch).toHaveBeenCalledWith(
      'https://example.com/api?id=123&query=test',
      expect.anything()
    );
  });

  test('应该能发送POST请求带JSON数据', async () => {
    const data = { name: '测试', value: 123 };
    await requests.postAsync('https://example.com/api', { json: data });
    
    expect(global.fetch).toHaveBeenCalledWith(
      'https://example.com/api',
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify(data),
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        })
      })
    );
  });

  test('应该能处理请求钩子', async () => {
    const beforeRequestHook = jest.fn(options => {
      options.fetchOptions.headers = {
        ...options.fetchOptions.headers,
        'X-Test-Header': 'test-value'
      };
      return options;
    });
    
    const afterResponseHook = jest.fn(response => response);
    
    await requests.getAsync('https://example.com/api', {
      hooks: {
        beforeRequest: [beforeRequestHook],
        afterResponse: [afterResponseHook]
      }
    });
    
    expect(beforeRequestHook).toHaveBeenCalledTimes(1);
    expect(afterResponseHook).toHaveBeenCalledTimes(1);
    
    expect(global.fetch).toHaveBeenCalledWith(
      'https://example.com/api',
      expect.objectContaining({
        headers: expect.objectContaining({
          'X-Test-Header': 'test-value'
        })
      })
    );
  });
});

// 会话测试
describe('Session 类测试', () => {
  test('应该能管理Cookie', async () => {
    const session = requests.createSession();
    
    // 第一个请求，获取Cookie
    await session.getAsync('https://example.com/api');
    
    // 第二个请求，应该发送之前获取的Cookie
    await session.getAsync('https://example.com/api/data');
    
    // 检查第二次请求是否包含Cookie
    const secondCallArgs = global.fetch.mock.calls[1][1];
    expect(secondCallArgs.headers).toHaveProperty('Cookie');
    expect(secondCallArgs.headers.Cookie).toContain('session=123');
  });
});

// 响应测试
describe('Response 类测试', () => {
  test('应该能正确解析JSON响应', async () => {
    const response = await requests.getAsync('https://example.com/api');
    
    expect(response.isJson()).toBe(true);
    
    const data = await response.jsonAsync();
    expect(data).toEqual({message: '测试成功'});
  });
  
  test('应该能获取响应头', async () => {
    const response = await requests.getAsync('https://example.com/api');
    
    expect(response.headers['content-type']).toBe('application/json');
  });
});