from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["fasttext>=0.9.2", "wget>=3.2"]

setup(
    name="langidentification",
    version="1.2",
    author="Abhishek Suresh",
    author_email="abhishek.sures@gmail.com",
    description="A package for language identification based on fastText, including romanised South Asian languages "
                "and Arabic",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/absu5530/langidentification",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)