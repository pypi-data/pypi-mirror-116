import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chromcocluster",
    version="0.0.5",
    author="Thomas George and Sivan Leviyang",
    author_email="Sivan.Leviyang@georgetown.edu",
    description="Co-clustering of chromatin accessibility data across cell types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SLeviyang/chromcocluster",
    project_urls={
        "Bug Tracker": "https://github.com/SLeviyang/chromcocluster/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
