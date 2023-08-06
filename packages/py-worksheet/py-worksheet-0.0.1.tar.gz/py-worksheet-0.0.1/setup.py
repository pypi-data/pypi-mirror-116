from setuptools import setup, find_packages
from version import version, name

with open("README.md") as f:
    long_description = f.read()

setup(
    name=f'{name}',
    version=f'{version}',
    packages=find_packages(),
    long_description=long_description,
    url="https://pysheet.github.io/pysheet/",
    author='Gilad Kutiel',
    author_email='gilad.kutiel@gmail.com',
    install_requires=[
        'fire',
        'numpy',
    ],
    package_data={
        'helpful_tools': ['*'],
    },
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gk-arithmetic = pysheet.arithmetic:main',

            'gk-equation-1 = pysheet.equation_1:main',
            'gk-equation-2 = pysheet.equation_2:main',
            'gk-equation-3 = pysheet.equation_3:main',

            'gk-frac-1 = pysheet.frac_1:main',
        ],
    }
)
