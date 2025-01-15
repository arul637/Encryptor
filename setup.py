from setuptools import setup, find_packages

setup(
    name='HaulEnc',
    version='0.1',
    description='A Python-based file encryption and decryption toolkit.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Arulkumaran S',
    author_email='sarulkumaran.21042004@gmail.com',
    url='https://github.com/arul637/Encryptor',  
    packages=find_packages(),
    install_requires=[
        'pycryptodome',   # For AES encryption and PBKDF2
        'colorama',       # For colored output in the terminal
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'haul=haul.main:main',  # Entry point for the CLI
        ],
    },
    python_requires='>=3.6',
)
