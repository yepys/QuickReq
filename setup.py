from setuptools import setup, find_packages

setup(
    name="modern_requests",
    version="1.0.0",
    description="一个现代化高效的Python HTTP请求库",
    author="",
    author_email="",
    url="",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.7.0",
        "urllib3>=1.26.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)