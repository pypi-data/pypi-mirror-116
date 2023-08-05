import os
from setuptools import setup, find_packages

# python setup.py check
# python setup.py sdist
# or python setup.py sdist --format=zip
# twine upload dist/aduck-*.tar.gz

path = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    with open(os.path.join(path, filename)) as f:
        long_description = f.read()
    return long_description

def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name="aduck",
    version="0.0.4",
    keywords=["common library", "5-layer" , "wrap layer"],
    description="util package",
    long_description=read_file("README.md"),
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",
    author="Daqian",
    author_email="daqian.zhang@g42.ai",
    url="https://g42.ai",
    packages = find_packages(),
    include_package_data=True,
    install_requires = [],
    platforms="any",
    scripts=[],
    zip_safe=False

)
