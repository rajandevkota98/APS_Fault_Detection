
# we create setup file to make our code to install it as an library. 
# - e.means--> editable extention... here . is locating the present directory
from setuptools import find_packages,setup

from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements()->List[str]:
    
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        print(requirement_list)
    requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
    
    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list



setup(
    name="sensor",
    version="0.0.2",
    author="Rajan Devkota",
    author_email="r.devkota.98@gmail.com",
    packages = find_packages(),
    install_requires=get_requirements(),
)


