/**
 * Modern Requests Library 高级用法示例
 */

// 导入库
const requests = require('../index');

// 并发请求示例
async function concurrentRequestsExample() {
  console.log('\n=== 并发请求示例 ===');
  try {
    // 创建多个请求的Promise数组
    const promises = [
      requests.getAsync('https://jsonplaceholder.typicode.com/posts/1'),
      requests.getAsync('https://jsonplaceholder.typicode.com/posts/2'),
      requests.getAsync('https://jsonplaceholder.typicode.com/posts/3'),
      requests.getAsync('https://jsonplaceholder.typicode.com/posts/4'),
      requests.getAsync('https://jsonplaceholder.typicode.com/posts/5')
    ];
    
    // 并发执行所有请求
    console.log('开始并发请求...');
    const startTime = Date.now();
    const responses = await Promise.all(promises);
    const endTime = Date.now();
    
    console.log(`完成所有请求，耗时: ${endTime - startTime}ms`);
    console.log(`获取到 ${responses.length} 个响应`);
    
    // 处理所有响应
    for (let i = 0; i < responses.length; i++) {
      const data = await responses[i].jsonAsync();
      console.log(`响应 ${i + 1} 的标题: ${data.title}`);
    }
  } catch (error) {
    console.error('并发请求失败:', error.message);
  }
}

// 高级错误处理示例
async function advancedErrorHandlingExample() {
  console.log('\n=== 高级错误处理示例 ===');
  
  // 自定义状态码验证函数
  const customValidator = status => status === 200; // 只接受200状态码
  
  try {
    // 请求一个不存在的资源，会返回404
    await requests.getAsync('https://jsonplaceholder.typicode.com/nonexistent', {
      validateStatus: customValidator,
      maxRetries: 2
    });
  } catch (error) {
    console.log('预期的错误被捕获:', error.message);
  }
  
  try {
    // 使用工具函数进行重试
    const fetchWithRetry = requests.utils.withRetry(
      async () => {
        const response = await fetch('https://jsonplaceholder.typicode.com/nonexistent');
        if (!response.ok) throw new Error(`HTTP错误: ${response.status}`);
        return response;
      },
      {
        maxRetries: 3,
        retryDelay: 500,
        shouldRetry: error => {
          console.log(`发生错误，准备重试: ${error.message}`);
          return true; // 所有错误都重试
        }
      }
    );
    
    await fetchWithRetry();
  } catch (error) {
    console.log('重试后仍然失败:', error.message);
  }
}

// 表单提交示例
async function formSubmissionExample() {
  console.log('\n=== 表单提交示例 ===');
  try {
    // URL编码表单
    const formResponse = await requests.postAsync('https://jsonplaceholder.typicode.com/posts', {
      form: {
        title: '表单提交测试',
        body: '这是通过表单提交的内容',
        userId: 1
      }
    });
    
    console.log('表单提交响应:', await formResponse.jsonAsync());
    
    // FormData（多部分表单）
    // 在实际应用中，可以包含文件上传
    const formDataResponse = await requests.postAsync('https://jsonplaceholder.typicode.com/posts', {
      formData: {
        title: '多部分表单提交测试',
        body: '这是通过多部分表单提交的内容',
        userId: 1
        // 文件上传示例:
        // file: fs.createReadStream('path/to/file.jpg')
      }
    });
    
    console.log('多部分表单提交响应:', await formDataResponse.jsonAsync());
  } catch (error) {
    console.error('表单提交失败:', error.message);
  }
}

// 自定义请求实例示例
async function customRequestInstanceExample() {
  console.log('\n=== 自定义请求实例示例 ===');
  try {
    // 创建自定义请求实例
    const customRequest = requests.createRequest({
      timeout: 10000,
      maxRetries: 2,
      headers: {
        'User-Agent': 'CustomRequestInstance/1.0',
        'X-Custom-Header': '自定义值'
      },
      // 添加全局钩子
      hooks: {
        beforeRequest: [
          options => {
            console.log('全局请求前钩子执行');
            return options;
          }
        ],
        afterResponse: [
          response => {
            console.log('全局响应后钩子执行');
            return response;
          }
        ]
      }
    });
    
    // 使用自定义实例发送请求
    const response = await customRequest.sendAsync('https://jsonplaceholder.typicode.com/posts/1');
    console.log('自定义实例响应:', await response.jsonAsync());
  } catch (error) {
    console.error('自定义实例请求失败:', error.message);
  }
}

// 连接池和性能优化示例
async function connectionPoolExample() {
  console.log('\n=== 连接池和性能优化示例 ===');
  try {
    // 创建会话（内部使用连接池）
    const session = requests.createSession();
    
    console.log('开始批量请求测试...');
    const startTime = Date.now();
    
    // 使用相同会话发送多个请求
    // 会话会自动复用连接，提高性能
    const results = [];
    for (let i = 1; i <= 10; i++) {
      const response = await session.getAsync(`https://jsonplaceholder.typicode.com/posts/${i}`);
      results.push(await response.jsonAsync());
    }
    
    const endTime = Date.now();
    console.log(`完成所有请求，耗时: ${endTime - startTime}ms`);
    console.log(`获取到 ${results.length} 个响应`);
    
    // 现在进行并发请求测试
    console.log('\n开始并发请求测试（使用会话）...');
    const concurrentStartTime = Date.now();
    
    const promises = [];
    for (let i = 11; i <= 20; i++) {
      promises.push(session.getAsync(`https://jsonplaceholder.typicode.com/posts/${i}`));
    }
    
    const responses = await Promise.all(promises);
    const concurrentResults = await Promise.all(responses.map(r => r.jsonAsync()));
    
    const concurrentEndTime = Date.now();
    console.log(`完成所有并发请求，耗时: ${concurrentEndTime - concurrentStartTime}ms`);
    console.log(`获取到 ${concurrentResults.length} 个响应`);
  } catch (error) {
    console.error('连接池测试失败:', error.message);
  }
}

// 运行所有高级示例
async function runAllAdvancedExamples() {
  await concurrentRequestsExample();
  await advancedErrorHandlingExample();
  await formSubmissionExample();
  await customRequestInstanceExample();
  await connectionPoolExample();
  console.log('\n所有高级示例执行完成！');
}

// 执行示例
runAllAdvancedExamples().catch(error => {
  console.error('示例运行失败:', error);
});