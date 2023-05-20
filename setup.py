import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aws_pylib',
    version='1.0.0',
    author='Matthew McCollom',
    author_email='matthew@mccollom.info',
    description="Library providing AWS service integration for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/prioritypower/aws_python_utils',
    project_urls={
        "Bug Tracker": "https://github.com/prioritypower/aws_python_utils/issues"
    },
    packages=['aws_util'],
    install_requires=[],
)