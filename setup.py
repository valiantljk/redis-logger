import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redis_logger", # Replace with your own username
    version="0.0.6",
    author="Jialin Liu",
    author_email="valiantljk@gmail.com",
    description="Logger for K8S services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/valiantljk/service_logger.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)