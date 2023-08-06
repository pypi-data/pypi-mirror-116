import setuptools

setuptools.setup(name="rvbust-vis-test",  # 包名
                 version='1.0.0',  # 版本号
                 description='pip install Vis',
                 long_description='Asynchronous 3D Visualization Tool',
                 author='rvbust',
                 author_email='hi@rvbust.com',
                 url='',
                 license='MIT',

                 classifiers=["Programming Language :: Python :: 3",
                                  "License :: OSI Approved :: MIT License",
                                  "Operating System :: OS Independent",
                              ],

                 package_dir={'':  'src'},
                 packages=setuptools.find_packages(where="src"),

                 include_package_data=True,
                 package_data={"": ["*.so"]}


                 )
