from setuptools import setup
from setup_common import setup_options

setup(**setup_options,
      extras_require={
          'pyqt5': ['pyqt5']
      },
      zip_safe=False)
