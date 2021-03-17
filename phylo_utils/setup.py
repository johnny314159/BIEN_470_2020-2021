import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='phylo_utils',
     version='0.0.2',
     # scripts=[''] ,
     author="Faizy Ahsan",
     author_email="faizy.ahsan@mail.mcgill.ca",
     description="A Inference Booster package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/zaifyahsan/phylo_utils",
     packages=['phylo_utils'], #setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
