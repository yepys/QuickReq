# 贡献指南

感谢您考虑为QuickReq库做出贡献！这个文档提供了一些指导，帮助您顺利地参与到项目中来。

## 开发环境设置

1. 克隆仓库
   ```bash
   git clone https://github.com/yepys/quickreq.git
   cd quickreq
   ```

2. 安装依赖
   ```bash
   npm install
   ```

3. 运行测试
   ```bash
   npm test
   ```

## 代码风格

本项目使用ESLint来保持代码风格的一致性。在提交代码前，请确保您的代码通过了lint检查：

```bash
npm run lint
```

## 提交Pull Request

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加了一些很棒的特性'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个Pull Request

## 报告Bug

如果您发现了bug，请创建一个issue，并尽可能详细地描述问题，包括：

- 问题的简要描述
- 重现步骤
- 预期行为
- 实际行为
- 环境信息（Node.js版本、操作系统等）

## 功能请求

如果您有新功能的想法，欢迎创建一个issue来讨论。请包括：

- 功能的详细描述
- 为什么这个功能对项目有价值
- 如果可能，提供一些实现思路

## 文档改进

文档改进也是非常重要的贡献。如果您发现文档中有错误或者不清晰的地方，请提交PR来改进它。

## 版本发布流程

1. 更新版本号（遵循[语义化版本控制](https://semver.org/lang/zh-CN/)）
2. 更新CHANGELOG.md
3. 创建一个新的发布标签
4. 发布到npm

## 行为准则

请确保您的行为符合我们的行为准则。简而言之：

- 尊重所有参与者
- 使用包容性语言
- 接受建设性批评
- 关注社区最佳利益

## 许可证

通过贡献您的代码，您同意您的贡献将在MIT许可证下发布。