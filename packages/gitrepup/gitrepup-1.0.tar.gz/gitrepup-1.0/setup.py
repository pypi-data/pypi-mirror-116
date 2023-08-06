import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="gitrepup",
    version="1.0",
    description="A simple python utility script to update all github repositories in a location giving the user a good UI using the python rich module",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ruthvikvegunta/gitrepup",
    author="Ruthvik Vegunta",
    author_email="ruthvikv@icloud.com, ruthvikvegunta2@gmail.com",
    keywords=["Python", "Script", "Github", "Update"],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        'rich'
    ],
    entry_points = {
         "console_scripts": ['gitrepup = gitrepup.gitrepup:main']
     },
)