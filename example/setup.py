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
    keywords='assembly dist offline install dependencies',
    url='http://github.com/chaokunyang/pyassemble/example',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        "package": Package
    }
)
