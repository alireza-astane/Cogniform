# fastapi = "^0.75.0"
# uvicorn = "^0.17.0"
# pydantic = "^1.9.0"
# matplotlib = "^3.7.3"
# seaborn = "^0.12.2"
# sqlalchemy = "^1.4.0"
# jinja2 = "^3.1.0"
# python-multipart = "^0.0.20"
# pytest = "^7.0"
# requests = "^2.32.3"
# pytest = "^7.0.0"
# flake8 = "^4.0.0"
# black = "^22.0.0"

packages = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "matplotlib",
    "seaborn",
    "sqlalchemy",
    "jinja2",
    "python-multipart",
    "pytest",
    "requests",
    "flake8",
    "black",
]

import fastapi
import uvicorn
import pydantic
import matplotlib
import seaborn
import sqlalchemy
import jinja2
import python_multipart
import pytest
import requests
import flake8
import black


print(f'fastapi = "^{fastapi.__version__}"')
print(f'uvicorn = "^{uvicorn.__version__}"')
print(f'pydantic = "^{pydantic.__version__}"')
print(f'matplotlib = "^{matplotlib.__version__}"')
print(f'seaborn = "^{seaborn.__version__}"')
print(f'sqlalchemy = "^{sqlalchemy.__version__}"')
print(f'jinja2 = "^{jinja2.__version__}"')
print(f'python-multipart = "^{python_multipart.__version__}"')
print(f'pytest = "^{pytest.__version__}"')
print(f'requests = "^{requests.__version__}"')
print(f'flake8 = "^{flake8.__version__}"')
print(f'black = "^{black.__version__}"')
