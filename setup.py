from setuptools import setup

setup(name='lpstools',
      version='0.1',
      description='Loco positioning tools',
      url='http://github.com/bitcraze/lpstools',
      author='Bitcraze',
      author_email='contact@bitcraze.io',
      license='MIT',
      packages=['lpstools', 'dfuse'],
      install_requires=[
          'pyqt5',
      ],
      zip_safe=False)
