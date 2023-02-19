from setuptools import find_packages, setup


def get_version() -> str:
    rel_path = "src/lambdacloud/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


install_requires = [
    "requests",
    "tqdm>=4.42.1",
    "fire",
]

extras = {}
extras["testing"] = [
    "pytest",
    "pytest-cov",
]
extras["quality"] = [
    "black==22.3",
    "flake8>=3.8.3",
    "isort>=5.5.4",
    "mypy==0.982",
]
extras["dev"] = extras["testing"] + extras["quality"]

setup(
    name="lambdacloud",
    description="A Python client library for Lambda Lab's Cloud",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nateraw/lambdacloud",
    version=get_version(),
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    license="Apache",
    install_requires=install_requires,
    extras_require=extras,
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["lambdacloud=lambdacloud.cli:main"]},
)
