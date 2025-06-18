from setuptools import setup, find_packages

setup(
    name="urlmaster",
    version="1.0",
    description="CLI tool to launch FastAPI + static frontend with system service installation",
    author="Neeraj Choudhary",
    packages=find_packages(include=["urlmaster", "urlmaster.*"]),  # ✅ No need to include "services" separately

    package_data={
        "urlmaster": ["install/*.template", "public/*", "main.py"],
        "urlmaster.services": ["*.json"],  # ✅ Include JSON files in services subpackage
    },
    
    include_package_data=True,

    install_requires=[
        "typer[all]",
        "fastapi",
        "uvicorn"
    ],

    entry_points={
    "console_scripts": [
        "urlmaster = urlmaster.cli:app"  # ✅ FIXED
    ]
},

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    python_requires='>=3.7',
)
