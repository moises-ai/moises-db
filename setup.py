import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="moises-db",
    version="0.0.2",
    author="Igor Pereira",
    author_email="igor@moises.ai",
    description="moises-db",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moises-ai/moises-db",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.8",
)
