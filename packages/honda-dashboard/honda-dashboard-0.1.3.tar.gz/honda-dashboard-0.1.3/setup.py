from setuptools import setup

setup(
    name='honda-dashboard',
    version='0.1.3',
    description='OBD2 Honda honda_dashboard.',
    url='https://github.com/todstoychev/dashboard',
    author='Todor Todorov',
    author_email='todstoychev@gmail.com',
    license='BSD 2-clause',
    packages=['honda_dashboard'],
    install_requires=['qtawesome',
                      'pyqt5',
                      'obd'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'honda-dashboard=honda_dashboard.__main__:main',
        ],
    },
    package_data={
        '': ['config.ini', 'honda.png']
    },
)
