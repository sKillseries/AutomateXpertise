# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open('requirements.txt', encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name='automatexpertise',
    author="sKillseries",
    description="Utilitaire qui permet de d'automatiser l'initialisation d'AutomateXpertise",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires='>=3.9, <4',
    version="1.1.3",
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        automatexpertise=automate.cli:cli
    ''',
    install_requires=requirements
)
