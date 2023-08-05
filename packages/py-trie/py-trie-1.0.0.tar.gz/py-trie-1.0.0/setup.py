import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).resolve().parent.parent
README = (HERE / "README.md").read_text()

setup(
    name="py-trie",
    version="1.0.0",
    description="CLI for communicating with a Trie hosted online",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ayush055/trie-project",
    author="Ayush Agarwal",
    author_email="ayushagarwal2500@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["click"],
    entry_points={
        "console_scripts": [
            "pytrie=pytrie.__main__:main",
        ]
    },
)