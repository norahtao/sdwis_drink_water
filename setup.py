from setuptools import setup, find_packages

setup(
    name='sdwis_drink_water',
    version='1.0',
    packages=find_packages(),
    description='Python wrappers for the Envirofacts Data Service API provided by the U.S. Environmental Protection Agency (EPA), with a focus on the Safe Drinking Water Information System (SDWIS).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='norahtao',
    author_email='rt2912@columbia.edu',
    url='https://github.com/norahtao/sdwis_drink_water',
    install_requires=[
        # Any package dependencies here
        "requests"
    ],
    classifiers=[
        # Choose classifiers: https://pypi.org/classifiers/
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
