from setuptools import setup, find_packages

setup(
    name="movie-recommendation-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "flask_pymongo",
        "flask_cors",
        "jwt"
    ],
)
