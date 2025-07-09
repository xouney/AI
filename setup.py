from setuptools import setup, find_packages

setup(
    name="ai-desktop-app",
    version="1.0.0",
    description="Application de bureau avec IA pour analyser tous types de code",
    packages=find_packages(),
    install_requires=[
        "chardet>=5.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'ai-desktop-app=main:main',
        ],
    },
    author="Assistant IA",
    author_email="assistant@example.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
