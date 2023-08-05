"""
Flask-Logging
-------------
 
Log every request to specific view
"""
from setuptools import setup
 
setup(
    name='Flask-Pay-WX',
    version='1.0.5',
    url='http://iotwonderful.com',
    license='BSD',
    author='lisichen, zhangchi',

    description='attachment file',
    long_description=__doc__,
    packages=['flask_pay_wx'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask','xmltodict','requests','pycryptodome','cryptography'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)