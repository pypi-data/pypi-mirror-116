from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='selfbotdiscord',
    version='0.0.8',
    description='Discord self bot module',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='',
    author='Emrovsky',
    author_email='eemrovsky@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='discord',
    packages=find_packages(),
    install_requires=['websocket-client','requests']
)