from setuptools import setup, find_packages

CURRENT_VERSION = "2.0"


setup(name='pyinf',
      version=CURRENT_VERSION,
      description='Python infrastructure code for logging and config management',
      author='Alex xi',
      author_email='alexxi0213@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      classifiers=[
          'Environment :: Other Environment',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
      ],
)
