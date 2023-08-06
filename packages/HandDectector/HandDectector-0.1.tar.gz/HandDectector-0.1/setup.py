from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1'
DESCRIPTION = 'HandDetector'
LONG_DESCRIPTION = 'A package to Hand Tracking , Hnad Detector, Hand Recognition .'

# Setting up
setup(
    name="HandDectector",
    version=VERSION,
    author="Rishabh",
    author_email="rinku87096@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['opencv-python','mediapipe'],
    keywords=['Hand Recognition', 'HandDectector', 'Hand Tracking', 'python tutorial', 'Rishabh', 'Sahil'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
