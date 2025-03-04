from setuptools import setup, find_packages

setup(
    name="swarm_demo",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pyautogen>=0.2.0",
        "python-dotenv>=0.19.0",
        "serpapi>=0.1.0",
        "yfinance>=0.1.70",
        "pandas>=1.3.0",
        "requests>=2.26.0",
        "aiohttp>=3.8.0",
        "python-dateutil>=2.8.2",
        "textblob>=0.15.3"
    ],
    python_requires=">=3.8",
)