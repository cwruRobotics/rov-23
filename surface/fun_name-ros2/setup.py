from setuptools import setup
from glob import glob
import os

package_name = 'fun_name'
setup(
    name=package_name,
    version='1.0.0',
    package_dir={'': 'src'}, 
    packages=[package_name],
    data_files=[
        (os.path.join('share', package_name, 'resource'), glob('resource/*')),
        (os.path.join('share', package_name), ['plugin.xml']),
        (os.path.join('share', package_name), ['package.xml']),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='[TODO: put your GitHub handle here] at CWRUbotix',
    maintainer='CWRUbotix',
    description=(
        'TODO: replace this example package description'
    ),
    license='Apache 2.0'
)