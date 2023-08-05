from setuptools import setup, find_packages

file = open("README.md")
long_description = file.read() 
file.close()


setup(
    name = 'Tawpy', 
    version = '0.1.3', 
    author = 'devKeef',
    author_email = 'keef.devv@gmail.com',
    description = 'For requesting gifs from the tenor website',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/devKeef/Tawpy',
    classifiers =[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires = [
        "setuptools>=54",
        "wheel",
        "requests"
    ],
    packages = find_packages(),
    python_requires = '>=2.7', 
    include_package_data = True
)
