# QuickReq 发布指南

本文档提供了 QuickReq 库发布的简要步骤指南。详细的发布流程请参考 [PACKAGING.md](./PACKAGING.md)。

## 快速发布步骤

### 使用自动化脚本发布

我们提供了自动化发布脚本 `publish.py`，可以简化发布流程：

```bash
# 发布 Python 版本到测试环境
python publish.py --python

# 发布 Node.js 版本到测试环境
python publish.py --nodejs

# 发布两个版本到生产环境
python publish.py --python --nodejs --production
```

### 手动发布 Python 版本

1. 更新 `setup.py` 中的版本号
2. 运行测试: `python -m unittest discover tests`
3. 构建分发包: `python setup.py sdist bdist_wheel`
4. 上传到 PyPI: `twine upload dist/*`

### 手动发布 Node.js 版本

1. 更新版本号: `npm version patch/minor/major`
2. 运行测试: `npm test`
3. 创建 npm 包: `npm pack`
4. 发布到 npm: `npm publish`

## 发布前检查清单

- [ ] 所有测试通过
- [ ] 版本号已更新
- [ ] 文档已更新
- [ ] CHANGELOG.md 已更新
- [ ] 依赖项已更新到最新版本

## 发布后验证

### Python 版本

```bash
pip install modern-requests
python -c "from modern_requests import get; print(get('https://httpbin.org/get').status_code)"
```

### Node.js 版本

```bash
npm install modern-requests
node -e "const { get } = require('modern-requests'); console.log(get('https://httpbin.org/get').statusCode)"
```

## 常见问题

- **问题**: 上传到 PyPI 失败
  **解决方案**: 检查 PyPI 凭据，确保已安装最新版本的 twine

- **问题**: npm 发布失败
  **解决方案**: 检查是否已登录 npm (`npm login`)，确认包名未被占用

- **问题**: 安装后导入失败
  **解决方案**: 检查 `__init__.py` 文件，确保正确导出了所有模块

## 相关资源

- [Python 打包用户指南](https://packaging.python.org/)
- [npm 文档](https://docs.npmjs.com/)
- [语义化版本控制](https://semver.org/lang/zh-CN/)