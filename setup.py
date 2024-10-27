from setuptools import setup

setup(name='hrflow_test',
      version='0.0.1',
      author='Yanis Farhat',
      packages=['mingpt', 'pydparser'],
      description='A job application portal',
      install_requires=[
            'torch',
      ],
)
