from setuptools import setup, find_namespace_packages

setup(name='Clean Folder',
      version='0.0.1',
      description='This program sorts the files in the specified folder',
      url='https://github.com/S-Stepanov-1/GoIT_homework_02.git',
      author='S_Stepanov',
      author_email='stepa.sergey.nov@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      entry_points={'console_scripts': [
            'clean-folder=clean_folder.clean:main']}
      )
