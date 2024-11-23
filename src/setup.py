from setuptools import setup

setup(
    name="chatmgoblog",
    version="0.1",
    packages=["index_content", "ingest_mgoblog_data", "chatmgoblog"],
    install_requires=[
        'requests',
        'pydantic',
        "nltk",
        "pymongo",
        "bs4",
        "chromadb"
    ],
)