import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysnag",
    version="0.0.4",
    author="Karl Berggren",
    author_email="kalle@jjabba.com",
    description="lib for easy access to bugsnags's APIv2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jjabba/pysnag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)