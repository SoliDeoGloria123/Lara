from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="lara-cli",
    version="0.1.0",
    author="SoliDeoGloria123",
    author_email="contact@lara-cli.dev",
    description="CLI tool para generar proyectos FastAPI rápidamente",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SoliDeoGloria123/Lara",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'lara': ['templates/**/*', 'templates/**/**/*'],
    },
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "jinja2>=3.1.0",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "click>=8.0.0",
    ],
    extras_require={
        'dev': [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
        'mongodb': [
            "pymongo>=4.6.0",
            "motor>=3.3.0",
        ],
    },
    entry_points={
        'console_scripts': [
            'lara=lara.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
)
