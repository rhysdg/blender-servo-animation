import setuptools

with open("README.md", "r") as f:
    long_description = f.read()
setuptools.setup(
    name="blendersmap", 
    version="0.0.1",
    author="Rhys Williams",
    author_email="rhysdgwilliams@gmail.com",
    description="A python module complementing blender-servo-animation for use with Rapsberry pi/ Jetson devices etc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/https://github.com/rhysdg/robonnx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['adafruit-circuitpython-servokit',
                      'Jetson.GPIO',
                      'ujson'
    ],
    tests_require=['pytest'],
    python_requires='>=3.6',
)