from setuptools import setup, find_packages

version = '0.1.0'

setup(name='abu.admin',
      version=version,
      description='',
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='LaiYonghao',
      author_email='mail@laiyonghao.com',
      url='http://code.google.com/p/abu-admin',
      license='MIT',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['abu'],
      include_package_data=True,
      test_suite='nose.collector',
      test_requires=['Nose'],  
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'argparse',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      abu.admin = abu.admin.main:main
      """,
      )

