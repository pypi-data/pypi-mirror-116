from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='mcapi.run',
  version='1.0',
  scripts=['mcapi-help.py'],
  description='simple minecraft api made for the api.mcapi.run website || by overnice.exe',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Overnice.exe',
  author_email='silkepilon2009@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='minecraft', 
  packages=find_packages(),
  install_requires=['requests', 'colorama'] 
)
