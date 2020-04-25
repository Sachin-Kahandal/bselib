import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bselib",
    version="0.0.1",
    author="Sachin Kahandal",
    author_email="sachinkahandal142@gmail.com",
    description="A package for stocks data listed on Bombay Stock Exchange",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sachin-Kahandal/bselib",
    ducumentation = "https://bselib.readthedocs.io/en/latest/",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
        'bs4>=0.0.1',
        'requests>=2.23.0',
        'pandas>=1.0.0',
        'html5lib>=1.0.0',
    ],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology"
    ),
)