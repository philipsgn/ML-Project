from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = "-e ."
def get_requirements(file_path:str)->List[str]:
    '''
    this function return the list of requirements
    '''
    requirements=[]
    with open('requirements.txt') as file_obj:
        requirements= file_obj.readlines()
        requirements= [req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements
# Dang ky project
setup(
    name ='ML-project',
    version ='0.0.1',
    author='Philip',
    author_email='tanphat260705@gmail.com',
    packages= find_packages(),      # Tim thu muc co file __init__.py --> Cac file nam cung co the import lan nhau
    install_requires= get_requirements('requirements.txt')
)