from setuptools import setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="my_integer",
    version="0.1.0",
    python_requires=">=3.6",
    author="Laszlo Kindrat",
    author_email="laszlokindrat@xmos.com",
    description="Toy example for an arbitrary length integer class",
    long_description=readme(),
    extras_require={"test": ["pytest>=5.2.0,<6.3.0"]},
    license="MIT",
)
