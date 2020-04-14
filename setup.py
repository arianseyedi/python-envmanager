from distutils.core import setup

setup(
    name='envmanager',  # How you named your package folder (MyLib)
    packages=['envmanager'],  # Chose the same as "name"
    version='8.1.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='TYPE YOUR DESCRIPTION HERE',  # Give a short description about your library
    author='YOUR NAME',  # Type in your name
    author_email='bytectgroup@gmail.com',  # Type in your E-Mail
    url='https://github.com/arianseyedi/python-envmanager',  # Provide either the link to your github or to your website
    download_url='https://github.com/arianseyedi/python-envmanager/archive/master.zip',  # I explain this later on
    keywords=['environment', 'variables', 'parsing', 'config', 'configuration', 'envvars'],
    # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'marshmallow',
    ],
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
