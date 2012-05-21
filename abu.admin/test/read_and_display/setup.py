from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='read_and_display',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='LaiYonghao',
      author_email='mail@laiyonghao.com',
      url='',
      license='mit',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),

      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      read_and_display = read_and_display.main:main
      [abu.admin]
      read_and_display = read_and_display.admin:Admin
      """,
      )
