# Copyright © 2025 GlacieTeam. All rights reserved.
#
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0. If a copy of the MPL was not
# distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# SPDX-License-Identifier: MPL-2.0

import setuptools

setuptools.setup(
    name="mcbe-binarystream",
    version="2.0.1",
    author="GlacieTeam",
    description="BinaryStream",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GlacieTeam/BinaryStream-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
    license="MPL-2.0",
    python_requires=">=3",
)
