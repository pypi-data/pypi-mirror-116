# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 

setup(
    name='vcnadera',
    version='0.2.0',
    description='Nadera by Viniette & Clarity.',
    long_description='Private Use, Commercial Use are permitted. \
    Dont forget Copyright notice (e.g. https://vigne-cla.com/vcopt-tutorial/) in any social outputs. Thank you. \
    Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    author='Shoya Yasuda @ Viniette & Clarity, Inc.',
    author_email='selamatpagi1124@gmail.com',
    url='https://www.nadera.me/',
    license='Required: Copyright notice in any social outputs. \
    Permitted: Private Use, Commercial Use. \
    Forbidden: Sublicense, Modifications, Distribution, Patent Grant, Use Trademark, Hold Liable.',
    packages=find_packages(),
    install_requires=['numpy', 'opencv-python', 'torch', 'torchvision', 'pillow', 'matplotlib', 'keras==2.4.3', 'pycocotools'],
    package_dir={'vcnadera': 'vcnadera'},
    package_data={'vcnadera': ['utils/*', 'weights1/*', 'weights2/*']},
)