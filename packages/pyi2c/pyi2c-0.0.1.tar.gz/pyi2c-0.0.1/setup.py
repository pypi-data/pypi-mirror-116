import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyi2c",
    version="0.0.1",
    author="Eunchong Kim",
    author_email="chariskimec@gmail.com",
    description="A useful i2c package for Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/newini/pyi2c",
    project_urls={
        "Bug Tracker": "https://github.com/newini/pyi2c/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["smbus2"],
)
