import setuptools # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyIdea",
    version="1.0.0",
    author="Omar Arabi",
    description="sort idea with pyIdea",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Omar-Arabi1/PyIdea",
    packages=setuptools.find_packages(),
)