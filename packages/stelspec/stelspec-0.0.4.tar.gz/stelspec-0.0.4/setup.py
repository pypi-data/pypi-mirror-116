import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stelspec",
    version="0.0.4",
    author="Behrouz Safari",
    author_email="behrouz.safari@gmail.com",
    description="A python package for retrieving and analysing stellar spectra (ELODIE-SOPHIE Archive)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/behrouzz/stelspec",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["stelspec"],
    include_package_data=True,
    install_requires=["requests", "numpy", "pandas"],
    python_requires='>=3.4',
)
