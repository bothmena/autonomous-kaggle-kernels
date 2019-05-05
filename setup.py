import setuptools


setuptools.setup(
    name="akk",
    version="0.1",
    author="Aymen Ben Othmen",
    author_email="aymenbenothmenabo@gmail.com",
    description="Autonomous Kaggle Kernels",
    long_description='a python package to manage kaggle kernels and run code that take more than 9 hours to finish on multiple commits autonomously.',
    long_description_content_type="text/markdown",
    url="https://github.com/bothmena/autonomous-kaggle-kernels",
    keywords=['Autonomous', 'Kernel', 'Kaggle', 'API'],
    packages=setuptools.find_packages(exclude=["src", "kaggle-api", "examples", "tests"]),
    entry_points={'console_scripts': ['akk = akk.cli.commands:main']},
    install_requires=[
        'gitpython >= 2.1.*',
        'python-slugify'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
# gitpython
# rm -rf akk.egg-info/ build/ dist/ && pip uninstall akk -y && python3 setup.py sdist bdist_wheel && pip install dist/akk-0.1-py3-none-any.whl
