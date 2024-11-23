from setuptools import setup

setup(
    name="chatmgoblog",
    version="0.1",
    packages=["chatmgoblog"],
    install_requires=[
        'requests',
        'pydantic',
        "nltk"
    ],
)