from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    '''
    This function returns the list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        # Strip whitespace và loại bỏ dòng trống
        requirements = [req.strip() for req in requirements]
        requirements = [req for req in requirements if req]  # Loại bỏ dòng trống
        
        # Loại bỏ '-e .'
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

# Đăng ký project
setup(
    name='ML-project',
    version='0.0.1',
    author='Philip',
    author_email='tanphat260705@gmail.com',
    packages=find_packages(),  # Tìm thư mục có file __init__.py , có thể import somewhere
    install_requires=get_requirements('requirements.txt')
)