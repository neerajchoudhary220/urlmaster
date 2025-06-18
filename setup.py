from setuptools import setup, find_packages

setup(
    name="urlmaster",
    version="1.0",
    description="CLI tool to launch FastAPI + static frontend with system service installation",
    author="Neeraj Choudhary",
    packages=find_packages(include=["urlmaster", "urlmaster.*", "services", "services.*"]),
    include_package_data=True,
    install_requires=[
        "typer[all]",
        "fastapi",
        "uvicorn"
    ],
    entry_points={
        "console_scripts": [
            "urlmaster = urlmaster.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
