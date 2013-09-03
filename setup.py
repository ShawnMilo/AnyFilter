from setuptools import setup

setup(
    name='AnyFilter',
    version='0.02',
    description='Base class for easy filtering of iterable of dictionaries.',
    packages=['anyfilter',],
    license='BSD',
    url='https://github.com/ShawnMilo/anyfilter',
    author='Shawn Milochik',
    author_email='shawn@milochik.com',
    zip_safe=False,
    keywords='dictionary filter dict json',
    test_suite="anyfilter.tests",
)
