from setuptools import setup

with open("README.md", "r") as handle:
    long_description = handle.read()

# fmt: off
configuration = dict(
    name="hind",
    version="0.1.2",
    description="hind",
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
    url="https://gitlab.com/air64/hind",
    project_urls={
        "Gitlab": "https://gitlab.com/air64/hind",
    },
    license="MIT",
    packages=["hind"],
    python_requires=">=3.7",
    install_requires=[
        "boundless==0.1.0",
    ],
    include_package_data=True,
    scripts=[
        "bin/hind",
    ],
)
setup(**configuration)
# fmt: on
