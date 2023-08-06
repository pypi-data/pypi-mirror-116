from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='zephyr_behave',

    version='0.0.3',

    description='Based on allure, the output is recorded, and a Zephyr compatible json file is generated',
    long_description='Based on allure, the output is recorded, and a Zephyr compatible json file is generated',

    url='https://github.com/KotieSmit/zephyr_behave',

    author='Kotie Smit',
    author_email='',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.8',
    ],

    keywords='bdd behave automation json Zephyr',

    packages=find_packages(),

    install_requires=[],

    extras_require={},

    data_files=[],

    py_modules=['__init__', 'formatter', '*'],
    
    # entry_points={
    #     'console_scripts': [
    #         'behave2cucumberZephyr = behave2cucumberZephyr.behave2cucumberZephyr.__main__:main'
    #     ],
    # },
)
