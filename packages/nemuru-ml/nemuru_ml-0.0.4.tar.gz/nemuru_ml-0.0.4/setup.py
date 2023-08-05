from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='nemuru_ml',
    packages=find_packages(),
    py_modules=["nemuru_ml"],
    package_dir={
        'common':'nemuru_ml/common',
        'pipeline':'nemuru_ml/pipeline',
        'stages':'nemuru_ml/stages'
    },
    version='0.0.4',
    description='Nemuru ML core library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    author='Enric Gilabert',
    license='MIT',
    install_requires=['pandas~=1.3.1'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
