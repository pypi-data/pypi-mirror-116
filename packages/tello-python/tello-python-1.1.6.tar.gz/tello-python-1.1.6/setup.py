import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tello-python',
    version='1.1.6',
    author='C灵C',
    author_email='c0c@cocpy.com',
    description='Control DJI Tello drone with Python3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cocpy/Tello-Python',
    packages=setuptools.find_packages(),
    install_requires=[
        'opencv-python', 'flask', 'paddlepaddle', 'paddlehub'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)