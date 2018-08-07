from setuptools import setup

from setup_common import setup_options

setup(extras_require={
    'pyqt5': ['pyqt5==5.10']
},
    zip_safe=False,
    **setup_options)
