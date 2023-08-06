from setuptools import setup, find_packages

setup(
    name='hisailors',
    url="https://github.com/skiloop/hisailors",
    version='1.0',
    license='MIT',
    zip_safe=False,
    author='skiloop',
    author_email='skiloop@gmail.com',
    description='A group of tools for http',
    python_requires='>=3.6',
    packages=find_packages(exclude=['tests', 'tests.*']),
)
