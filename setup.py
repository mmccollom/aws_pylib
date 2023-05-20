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
    url='https://github.com/mmccollom/aws_pylib',
    project_urls={
        "Bug Tracker": "https://github.com/mmccollom/aws_pylib/issues"
    },
    packages=['aws_pylib'],
    install_requires=[],
)