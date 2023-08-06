from setuptools import setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="sfp",
    version="1.0.0",
    author="XenoCorn",
    description="Python implementation of SFP",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/xenocorn/PySFP",
    packages=['sfp'],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet",
    ],
)
