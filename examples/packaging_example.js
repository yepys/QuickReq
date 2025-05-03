/**
 * QuickReq 打包发布示例 (Node.js版本)
 *
 * 本示例展示了如何使用 QuickReq 库的打包发布工具进行 Node.js 版本库的发布。
 */

// 导入库
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * 打印带分隔符的标题
 * @param {string} title 标题文本
 */
function printSection(title) {
  console.log('\n' + '='.repeat(50));
  console.log(` ${title} `);
  console.log('='.repeat(50));
}

/**
 * 运行命令并返回输出
 * @param {string} command 要运行的命令
 * @returns {string} 命令输出
 */
function runCommand(command) {
  try {
    return execSync(command, { encoding: 'utf8' });
  } catch (error) {
    console.error(`命令执行失败: ${error.message}`);
    return '';
  }
}

/**
 * 主函数
 */
function main() {
  printSection('QuickReq 打包发布示例 (Node.js版本)');
  
  // 显示当前版本
  try {
    const packageJson = require('../package.json');
    console.log(`当前 Node.js 版本: ${packageJson.version}`);
  } catch (error) {
    console.log('无法读取 package.json 文件');
  }
  
  // 显示打包发布选项
  console.log('\n可用的打包发布选项:');
  console.log('1. 使用自动化脚本发布');
  console.log('   python publish.py --nodejs  # 发布 Node.js 版本');
  
  console.log('\n2. 手动发布 Node.js 版本');
  console.log('   npm version patch  # 更新补丁版本号');
  console.log('   npm version minor  # 更新次要版本号');
  console.log('   npm version major  # 更新主要版本号');
  console.log('   npm pack           # 创建 npm 包进行测试');
  console.log('   npm publish       # 发布到 npm 仓库');
  
  // 显示发布前检查清单
  printSection('发布前检查清单');
  console.log('✓ 更新版本号 (package.json)');
  console.log('✓ 运行所有测试 (npm test)');
  console.log('✓ 更新文档 (README.md)');
  console.log('✓ 更新 CHANGELOG.md');
  console.log('✓ 检查 .npmignore 文件');
  
  // 显示发布后验证步骤
  printSection('发布后验证');
  console.log('1. 安装发布的包:');
  console.log('   npm install modern-requests');
  
  console.log('\n2. 验证功能:');
  console.log('   const { get } = require("modern-requests");');
  console.log('   const response = get("https://httpbin.org/get");');
  console.log('   console.log(response.statusCode);  // 应该输出 200');
  
  printSection('更多信息');
  console.log('详细的打包发布指南请参考项目根目录下的:');
  console.log('- PACKAGING.md: 详细的打包发布文档');
  console.log('- RELEASE_GUIDE.md: 发布流程简要指南');
  console.log('- CHANGELOG.md: 版本更新历史');
}

// 执行主函数
main();