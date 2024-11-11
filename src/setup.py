from setuptools import setup

setup(
    name="ingest_mgoblog_data",
    version="0.1",
    packages=["ingest_mgoblog_data", "embed_data"],
    install_requires=[
        'requests',
        'bs4',
        'pydantic',
        'pymongo'
    ],
)