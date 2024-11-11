from setuptools import setup

setup(
    name="chatmgoblog",
    version="0.1",
    packages=["ingest_mgoblog_data", "embed_data"],
    install_requires=[
        'requests',
        'bs4',
        'pydantic',
        'pymongo',
        "chromadb"
    ],
)