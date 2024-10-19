from setuptools import setup, find_packages

setup(
    name='kgraphservice',
    version='0.0.8',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='KGraph Service',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/kgraphservice',
    packages=find_packages(exclude=["test","vitalhome","test_data","docs"]),
    license='Apache License 2.0',
    scripts=[
        'bin/kgraphservice'
    ],
    install_requires=[
        'vital-ai-vitalsigns>=0.1.22',
        'vital-ai-domain>=0.1.7',
        'six',
        'pyyaml',
        'vital-ai-haley-kg>=0.1.18',
        'rdflib==7.0.0',
        'SPARQLWrapper==2.0.0',
        'networkx',
        'uvicorn[standard]==0.27.0.post1',
        'fastapi==0.109.2',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10'
)
