from setuptools import setup, find_packages

with open("README.md", "r") as rd:
  long_description = rd.read()

setup(
 name='linearwinvolume',
 version='1.0.0',
 description="A Python implementation of pycaw that doesn't function on a logarithmic scale",
 long_description=long_description,
 long_description_content_type="text/markdown",
 url='https://github.com/That-CC/linearWinVolume', 
 author='Adrian Ornelas',
 author_email='afornelas@outlook.com',
 classifiers=[
   'Intended Audience :: Education',
   'Operating System :: Microsoft :: Windows',
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3',
 ],
 keywords=['python', 'pycaw', 'volume', 'windows volume','windows volume control'],
 packages=find_packages(),
 install_requires = ['pycaw','comtypes', 'enum34;python_version<"3.4"', 'psutil', 'future']
)