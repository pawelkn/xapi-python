from setuptools import setup

setup(
    name='xapi-python',
    author='Paweł Knioła',
    author_email='pawel.kn@gmail.com',
    description='The xStation5 API Python library',
    long_description=open('README.md', encoding='utf-8').read(),
    license='MIT',
    keywords='python trading websocket trading-api forex xapi forex-trading exchange-api forex-data xstation5 xtb xopenhub forex-api xopenhub-api xtb-api xstation-api x-trade-brokers bfbcapital xstation',
    url='https://github.com/pawelkn/xapi-python',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    version="0.0.1",
    packages=['xapi'],
)