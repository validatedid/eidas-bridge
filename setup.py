""" package eidas_bridge """

from setuptools import setup, find_packages

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setup(
        name='eidas_bridge',
        version='0.2.0',
        author='Validated Id <info@validatedid.com>',
        description='Python eIDAS Bridge Library',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://www.validatedid.com',
        license='Apache 2.0',
        packages=find_packages(exclude=['tests', 'demo', 'scripts', 'docker']),
        install_requires=parse_requirements('requirements.txt'),
        python_requires='>=3.6',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent'
        ]
    )