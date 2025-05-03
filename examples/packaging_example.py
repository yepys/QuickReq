#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QuickReq 打包发布示例

本示例展示了如何使用 QuickReq 库的打包发布工具进行库的发布。
"""

import os
import sys
import subprocess

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def print_section(title):
    """打印带分隔符的标题"""
    print("\n" + "=" * 50)
    print(f" {title} ")
    print("=" * 50)


def main():
    """打包发布示例主函数"""
    print_section("QuickReq 打包发布示例")
    
    # 显示当前版本
    try:
        from modern_requests import __version__ as py_version
        print(f"当前 Python 版本: {py_version}")
    except ImportError:
        print("无法导入 modern_requests 模块")
    
    # 显示打包发布选项
    print("\n可用的打包发布选项:")
    print("1. 使用自动化脚本发布")
    print("   python publish.py --python  # 发布 Python 版本")
    print("   python publish.py --nodejs  # 发布 Node.js 版本")
    
    print("\n2. 手动发布 Python 版本")
    print("   python setup.py sdist bdist_wheel")
    print("   twine upload dist/*")
    
    print("\n3. 手动发布 Node.js 版本")
    print("   npm version patch  # 更新版本号")
    print("   npm publish")
    
    # 显示发布前检查清单
    print_section("发布前检查清单")
    print("✓ 更新版本号")
    print("✓ 运行所有测试")
    print("✓ 更新文档")
    print("✓ 更新 CHANGELOG.md")
    
    # 显示发布后验证步骤
    print_section("发布后验证")
    print("1. 安装发布的包:")
    print("   pip install modern-requests")
    print("   npm install modern-requests")
    
    print("\n2. 验证功能:")
    print("   from modern_requests import get")
    print("   response = get('https://httpbin.org/get')")
    print("   print(response.status_code)  # 应该输出 200")
    
    print_section("更多信息")
    print("详细的打包发布指南请参考项目根目录下的:")
    print("- PACKAGING.md: 详细的打包发布文档")
    print("- RELEASE_GUIDE.md: 发布流程简要指南")
    print("- CHANGELOG.md: 版本更新历史")


if __name__ == "__main__":
    main()