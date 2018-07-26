# pyassemble
pyassemble is a tool of package python code libs and dependencies for offline installation. pyassemble implements an project build process like maven assembly

## Get Started
Install pyassemble
```bash
pip install pyassemble
```

`setup.py` example

```python
from setuptools import find_packages, setup
from pyassemble.package import Package

setup(
    name='pyassembly_example',
    author="chaokunyang",
    version='1.0',
    description='assemble project with all dependencies for install offline',
    long_description=open('README.rst').read(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
      ],
    keywords='assembly pyassemble dist offline install dependencies',
    url='http://github.com/chaokunyang/pyassemble/example',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        "package": Package
    }
)
```

Package

```bash
python setup.py package
```

Install

Install dependencies
```bash
pip install -r requirements.txt --no-index --find-links wheelhouse
```
Install project package
```bash
pip install .
```

## Others

You can do it manually:
* Download libs
    ```bash
    pip download django -d wheelhouse
    pip download -r requirements.txt -d wheelhouse
    ```
* Install libs
    ```bash
    pip install -r requirements.txt --no-index --find-links wheelhouse
    ```