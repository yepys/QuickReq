/**
 * Modern Requests Library 基本用法示例
 */

// 导入库
const requests = require('../index');

// 基本GET请求示例
async function basicGetExample() {
  console.log('\n=== 基本GET请求示例 ===');
  try {
    // 异步GET请求
    const response = await requests.getAsync('https://jsonplaceholder.typicode.com/posts/1');
    console.log(`状态码: ${response.statusCode}`);
    console.log(`响应类型: ${response.headers['content-type']}`);
    console.log('响应数据:', await response.jsonAsync());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 带参数的GET请求示例
async function getWithParamsExample() {
  console.log('\n=== 带参数的GET请求示例 ===');
  try {
    // 带查询参数的GET请求
    const response = await requests.getAsync('https://jsonplaceholder.typicode.com/posts', {
      params: { userId: 1, _limit: 3 }
    });
    console.log(`状态码: ${response.statusCode}`);
    console.log(`获取到 ${(await response.jsonAsync()).length} 条记录`);
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// POST请求示例
async function postExample() {
  console.log('\n=== POST请求示例 ===');
  try {
    // 发送JSON数据
    const response = await requests.postAsync('https://jsonplaceholder.typicode.com/posts', {
      json: {
        title: '测试标题',
        body: '测试内容',
        userId: 1
      }
    });
    console.log(`状态码: ${response.statusCode}`);
    console.log('响应数据:', await response.jsonAsync());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 自定义请求头示例
async function customHeadersExample() {
  console.log('\n=== 自定义请求头示例 ===');
  try {
    const response = await requests.getAsync('https://jsonplaceholder.typicode.com/posts/1', {
      headers: {
        'X-Custom-Header': '自定义值',
        'Accept-Language': 'zh-CN'
      }
    });
    console.log(`状态码: ${response.statusCode}`);
    console.log('响应数据:', await response.jsonAsync());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 会话示例
async function sessionExample() {
  console.log('\n=== 会话示例 ===');
  try {
    // 创建会话
    const session = requests.createSession();
    
    // 设置会话级别的请求头
    session.options.headers = {
      'User-Agent': 'Modern-Requests/1.0',
      'Accept-Language': 'zh-CN'
    };
    
    // 第一个请求
    const response1 = await session.getAsync('https://jsonplaceholder.typicode.com/posts/1');
    console.log('第一个请求状态码:', response1.statusCode);
    
    // 第二个请求会自动使用相同的会话设置
    const response2 = await session.getAsync('https://jsonplaceholder.typicode.com/posts/2');
    console.log('第二个请求状态码:', response2.statusCode);
    
    // 查看会话的Cookie
    console.log('会话Cookie:', session.getCookies());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 超时和重试示例
async function timeoutAndRetryExample() {
  console.log('\n=== 超时和重试示例 ===');
  try {
    const response = await requests.getAsync('https://jsonplaceholder.typicode.com/posts/1', {
      timeout: 5000,  // 5秒超时
      maxRetries: 2,  // 最多重试2次
      retryDelay: 1000 // 重试间隔1秒
    });
    console.log(`状态码: ${response.statusCode}`);
    console.log('响应数据:', await response.jsonAsync());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 请求钩子示例
async function hooksExample() {
  console.log('\n=== 请求钩子示例 ===');
  try {
    const response = await requests.getAsync('https://jsonplaceholder.typicode.com/posts/1', {
      hooks: {
        beforeRequest: [
          options => {
            console.log('请求前钩子:', options.url);
            // 可以修改请求选项
            options.fetchOptions.headers = {
              ...options.fetchOptions.headers,
              'X-Hook-Added': 'true'
            };
            return options;
          }
        ],
        afterResponse: [
          response => {
            console.log('响应后钩子:', response.statusCode);
            // 可以修改响应
            return response;
          }
        ]
      }
    });
    console.log('响应数据:', await response.jsonAsync());
  } catch (error) {
    console.error('请求失败:', error.message);
  }
}

// 运行所有示例
async function runAllExamples() {
  await basicGetExample();
  await getWithParamsExample();
  await postExample();
  await customHeadersExample();
  await sessionExample();
  await timeoutAndRetryExample();
  await hooksExample();
  console.log('\n所有示例执行完成！');
}

// 执行示例
runAllExamples().catch(error => {
  console.error('示例运行失败:', error);
});