from skbuild import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="NumbaMinpack",
    packages=['NumbaMinpack'],
    version='0.1.2',
    license='MIT',
    install_requires=['numpy','numba'],
    author = 'Nicholas Wogan',
    author_email = 'nicholaswogan@gmail.com',
    description = 'Python wrapper of Minpack (root finding)'+\
                  ' which can be called from within numba functions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>3.6',
    url = "https://github.com/Nicholaswogan/NumbaMinpack",
    cmake_args=['-DSKBUILD=ON']
    )