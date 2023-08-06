from distutils.core import setup
setup(
  name = 'expensify_client',
  packages = ['expensify_client'],
  version = '0.0.3',
  license='MIT',
  description = 'Python wrapper for Expensify API',
  author = 'Alex Lazich',
  author_email = 'lazich.alexander@gmail.com',
  url = 'https://github.com/alazich/expensify-client',
  download_url = 'https://github.com/alazich/expensify-client/archive/refs/tags/v0.0.3.tar.gz',
  keywords = ['api', 'accounting', 'expensify'],
  install_requires=[
          'validators',
          'beautifulsoup4',
          'PyYaml',
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ],
)