from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name='muusi',
    version='0.0.1',
    description='client library for a certain musician website',
    url='https://github.com/santerj/muusi',
    author='santerj',
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4==4.10.0",
        "requests==2.27.1"
    ],
    python_requires='>=3.8',
    include_package_data=True
)
