from setuptools import find_packages, setup


def read_md(md_file):
    try:
        # pip install m2r
        from m2r import parse_from_file
        return parse_from_file(md_file)
    except ImportError:
        print("warning: m2r module not found, could not convert Markdown to RST")
        return open(md_file, 'r').read()


setup(
    name='pyassemble',
    author="chaokunyang",
    version='1.0.0',
    description='Assemble project code with all dependencies for offline installation',
    long_description=read_md('README.md'),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
      ],
    keywords='assembly dist offline install dependencies',
    url='http://github.com/chaokunyang/py_assembly',
    license='Apache License 2.0',
    packages=['pyassemble'],
    include_package_data=True,
    zip_safe=False
)
