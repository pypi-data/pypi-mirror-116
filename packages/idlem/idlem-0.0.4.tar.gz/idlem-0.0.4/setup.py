from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().split()

with open("README.md") as f:
    readme = f.read()

setup(
    name="idlem",
    version="0.0.4",
    author="...",
    author_email="some@mail.com",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    description="idle-m",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3, <4",
    license="MIT License",
    install_requires=requirements,
    # scripts to enable pausing/unpausing running miner
    entry_points={
        "console_scripts": ["mup=idlem.utils:miner_unpause", "mp=idlem.utils:miner_pause", "ms=idlem.run:main"],
    },
    # flag to also include `config` folder
    include_package_data=True,
    package_data={
        "idlem": ["configs/*.yaml", "configs/*/*.yaml"],
    }
)
