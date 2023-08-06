from distutils.core import setup

setup(
  name = 'pearpy',
  packages = ['pearpy'],
  version = '0.1.1',
  license='MIT',
  description = 'A Python package for writing multithreaded code and parallelizing tasks across CPU threads.',
  author = 'Aiden Szeto',
  author_email = 'aszeto35@gmail.com',
  url = 'https://github.com/MLH-Fellowship/pear',
  download_url = 'https://github.com/MLH-Fellowship/pear/archive/refs/tags/v0.1.1.tar.gz',
  keywords = ['multithreading', 'parallelism', 'processes'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
