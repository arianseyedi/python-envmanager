from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'PyPI.md')) as f:
    long_description = f.read()

"""
 VERSIONING: 
    e.g.    1  .   9   .   7
           MAJ    MIN     FIX
"""
MAJ = 8
MIN = 1
FIX = 8


setup(
    name='envmanager',  # How you named your package folder (MyLib)
    packages=['envmanager', 'envmanager.decorators', 'envmanager.utils', 'envmanager.exceptions'],
    # Chose the same as "name"
    version=f'{MAJ}.{MIN}.{FIX}',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Validated environment variable management',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author='Arian Seyedi @Bytect',  # Type in your name
    author_email='bytectgroup@gmail.com',  # Type in your E-Mail
    url='https://github.com/arianseyedi/python-envmanager',  # Provide either the link to your github or to your website
    download_url=f'https://github.com/arianseyedi/python-envmanager/archive/v{MAJ}.{MIN}.{FIX}.tar.gz',
    # I explain this later on
    keywords=['environment', 'variables', 'parsing', 'config', 'configuration', 'envvars'],
    # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'marshmallow',
    ],
    setup_requires=['wheel'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
