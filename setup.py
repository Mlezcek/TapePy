from setuptools import setup, find_packages

setup(
    name="tapepy",
    version="0.1.0",
    description="Line-level code tracer and visualizer for Python functions",
    author="Mlezcek",
    #url="https://github.com/TwojGit/timewarp",
    packages=find_packages(),
    license="CUSTOM-NONSALE-LICENSE",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
