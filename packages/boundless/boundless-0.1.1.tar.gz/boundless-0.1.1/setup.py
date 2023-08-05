from setuptools import find_packages, setup

with open("README.md", "r") as handle:
    long_description = handle.read()

# fmt: off
configuration = dict(
    name="boundless",
    version="0.1.1",
    description="Erases boundaries between interface and python code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
    ],
    author="air64",
    author_email="air64@mailfence.com",
    maintainer=", ".join(
        (
            "air64 <air64@mailfence.com>",
        ),
    ),
    maintainer_email="air64@mailfence.com",
    url="https://gitlab.com/air64/boundless",
    project_urls={
        "Gitlab": "https://gitlab.com/air64/boundless",
    },
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.7.3",
        "jmespath==0.10.0",
    ],
    include_package_data=True,
    scripts=[
        "bin/brpc",
    ],
)
setup(**configuration)
# fmt: on
