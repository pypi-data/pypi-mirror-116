import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poetry-foundation-terminal",
    version="0.0.1",
    author="Vishwas Modhera",
    author_email="vishwasmodhera@pm.me",
    description="A small package to read daily poetries and essays posted by Poetry Foundation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishxm/poetry-in-terminal/",
    project_urls={
        "Bug Tracker": "https://github.com/vishxm/poetry-in-terminal/",
        "Reddit": "https://reddit.com/u/vishxm"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pFoundation = poetry_foundation.final_v1.py:start',
        ]
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)