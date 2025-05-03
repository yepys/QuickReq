#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
QuickReq 库打包发布脚本

此脚本用于自动化 QuickReq 库的打包和发布流程。
可以选择发布 Python 版本或 Node.js 版本。
"""

import os
import sys
import subprocess
import argparse


def run_command(command, error_message=None):
    """运行命令并处理错误"""
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        if error_message:
            print(f"错误: {error_message}")
        print(f"命令执行失败: {e}")
        return False


def publish_python(test=True):
    """发布 Python 版本的库"""
    print("\n=== 开始发布 Python 版本 ===")
    
    # 1. 运行测试
    print("\n运行测试...")
    if not run_command("python -m unittest discover tests", "测试失败"):
        return False
    
    # 2. 清理之前的构建
    print("\n清理之前的构建...")
    if os.path.exists("dist"):
        run_command("rm -rf dist build *.egg-info")
    
    # 3. 构建分发包
    print("\n构建分发包...")
    if not run_command("python setup.py sdist bdist_wheel", "构建分发包失败"):
        return False
    
    # 4. 检查分发包
    print("\n检查分发包...")
    if not run_command("twine check dist/*", "分发包检查失败"):
        return False
    
    # 5. 上传到 PyPI
    if test:
        print("\n上传到 TestPyPI...")
        if not run_command("twine upload --repository-url https://test.pypi.org/legacy/ dist/*", "上传到 TestPyPI 失败"):
            return False
        print("\n成功上传到 TestPyPI!")
        print("可以使用以下命令安装测试版本:")
        print("pip install --index-url https://test.pypi.org/simple/ modern-requests")
    else:
        print("\n上传到 PyPI...")
        if not run_command("twine upload dist/*", "上传到 PyPI 失败"):
            return False
        print("\n成功上传到 PyPI!")
        print("可以使用以下命令安装:")
        print("pip install modern-requests")
    
    return True


def publish_nodejs(test=True):
    """发布 Node.js 版本的库"""
    print("\n=== 开始发布 Node.js 版本 ===")
    
    # 1. 运行测试
    print("\n运行测试...")
    if not run_command("npm test", "测试失败"):
        return False
    
    # 2. 创建 npm 包
    print("\n创建 npm 包...")
    if not run_command("npm pack", "创建 npm 包失败"):
        return False
    
    # 3. 发布到 npm
    if not test:
        print("\n发布到 npm...")
        if not run_command("npm publish", "发布到 npm 失败"):
            return False
        print("\n成功发布到 npm!")
        print("可以使用以下命令安装:")
        print("npm install modern-requests")
    else:
        print("\n测试模式 - 跳过发布到 npm")
        print("检查生成的 .tgz 文件内容是否正确")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="QuickReq 库打包发布工具")
    parser.add_argument("--python", action="store_true", help="发布 Python 版本")
    parser.add_argument("--nodejs", action="store_true", help="发布 Node.js 版本")
    parser.add_argument("--production", action="store_true", help="发布到生产环境 (默认为测试环境)")
    
    args = parser.parse_args()
    
    if not (args.python or args.nodejs):
        parser.print_help()
        print("\n错误: 必须指定至少一个版本 (--python 或 --nodejs)")
        return 1
    
    test_mode = not args.production
    success = True
    
    if args.python:
        success = publish_python(test=test_mode) and success
    
    if args.nodejs:
        success = publish_nodejs(test=test_mode) and success
    
    if success:
        print("\n=== 发布流程完成! ===")
        return 0
    else:
        print("\n=== 发布流程失败! ===")
        return 1


if __name__ == "__main__":
    sys.exit(main())