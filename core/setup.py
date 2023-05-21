from setuptools import setup

setup(
    name='core',
    version='0.1.0',    
    description='El core del proyecto brainssys.databrain',
    author='Cesar Linares',
    author_email='cesar98.linares@gmail.com',
    license='BSD 2-clause',
    packages=['core'],
    install_requires=['kafka-python',
                    'kink',
                    'minio',
                    'elastic-transport',
                    'elasticsearch'                
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.10',
    ],
)
