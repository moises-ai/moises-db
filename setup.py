import yaml
import setuptools


def load_requirements(envpath='./environment.yaml'):
    with open(envpath) as f:
        env = yaml.safe_load(f)
    return env['dependencies'][-1]['pip']


setuptools.setup(
    name="MoisesDB",
    version="0.0.1",
    author="Igor Pereira",
    author_email="igor@moises.ai",
    description="MoisesDB",
    packages=setuptools.find_packages(),
    install_requires=load_requirements(),
    python_requires='>=3.8',
)