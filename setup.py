from setuptools import setup, find_packages

setup(name='gdspy_addons',
      version='0.0.1',
      description='Add ons for gdspy for the design of EBL defined CPWs',
      url='https://github.com/Emigon/gdspy-addons',
      author='Daniel Parker',
      author_email='danielparker@live.com.au',
      packages=find_packages(),
      install_requires=[
          'gdspy>=1.4',
          'numpy>=1.16.3',
        ])
