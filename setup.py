import setuptools

setuptools.setup(
    name="mcbe-binarystream",
    version="1.1.0",
    author="GlacieTeam",
    description="BinaryStream",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GlacieTeam/BinaryStream-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    license="LGPLv3",
    python_requires=">=3",
)
