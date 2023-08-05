import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aomaker",
    version="1.0.0",
    author="ancientone",
    author_email="listeningsss@163.com",
    description="An api testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ae86sen/aomaker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'atomicwrites == 1.4.0',
        'attrs == 21.2.0',
        'certifi == 2021.5.30',
        'chardet == 4.0.0',
        'colorama == 0.4.4',
        'Faker == 8.11.0',
        'idna == 2.10',
        'iniconfig == 1.1.1',
        'Jinja2 == 3.0.1',
        'jsonpath == 0.82',
        'loguru == 0.5.3',
        'MarkupSafe == 2.0.1',
        'packaging == 21.0',
        'pluggy == 0.13.1',
        'py == 1.10.0',
        'PyMySQL == 1.0.2',
        'pyparsing == 2.4.7',
        'pytest == 6.2.4',
        'pytest-tmreport == 1.3.7',
        'python-dateutil == 2.8.2',
        'PyYAML == 5.4.1',
        'requests == 2.25.1',
        'six == 1.16.0',
        'text-unidecode == 1.3',
        'toml == 0.10.2',
        'urllib3 == 1.26.5',
        'win32-setctime == 1.0.3'
    ],
    entry_points={
        'console_scripts': [
            'amake=httprunner.cli:main_make_alias',
            'arun=aomaker.cli:main_arun_alias',
            'aomaker=aomaker.cli:main',
        ]
    }
)
