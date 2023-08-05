from setuptools import setup

def readme():
    with open('README.md','r') as f:
        return f.read()

setup(
   name='sawo',
   version='1.2.1',
   description="Sawo Project",
   long_description=readme(),
   long_description_content_type='text/markdown',
   author='Sawolab',
   author_email="tech@sawolabs.com",
   license="MIT",
   packages=['sawo'],
   install_requires=['bs4'],
)