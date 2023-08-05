import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xmltocd",
    version="0.2.3.2",
    author="jiyang",
    author_email="jiyangj@foxmail.com",
    description="An effective, powerful, fast and simple XML Python parsing tool.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JIYANG-PLUS/xml-to-chain-dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)