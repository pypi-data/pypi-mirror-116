from setuptools import setup

long_descr = ''
with open('README.md', 'r') as fh:
	long_descr = fh.read()

setup(
	name = 'meaning-eraser',  # package name in PyPi
	version = '0.0.1',
	description = 'Just use it. You will be pleased.',
	classifiers = [
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: POSIX :: Linux'
	],
	py_modules = ['meaning'],  # list of python packages
	package_dir = {'': 'src'},  # to look packages in src/
	long_description = long_descr,
	long_description_content_type = 'text/markdown',
	url = 'https://lh3.googleusercontent.com/proxy/Rmdoy5CW5W6qQtvP7mBHBadP0aOMHbn2X_RP5MktfoSvLXPpeLjIWF9CwmHAFiOqjAMbAknd4D6OrngLIVwMK1sQvMNluEUrw4KXrCxmZGYkePPSCQ',
	author = 'Danila Simanok',
	author_email = 'danilasimanok@gmail.com'
)
