from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Commandline tool to display pi-hole statistics to be' + \
    'viewed in your terminal without any configuration or needing to log in.'

setup(
        name='holeinfo',
        version='2.0.2',
        author='Manik',
        author_email='me@manik.cc',
        url='https://github.com/mnk400/holeinfo',
        description='Pi.Hole statistics viewer',
        long_description=long_description,
        long_description_content_type="text/markdown",
        license='MIT',
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'holeinfo = holeinfo.src:main'
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords='pi hole manik raspberry pi adblock',
        install_requires=requirements,
        zip_safe=False
)
