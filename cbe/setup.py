import os

from distutils.core import setup

def find_packages(srcdir):
    package_list = []
    badnames=["__pycache__",]
    for root, dirs, files in os.walk(srcdir):
        if not any(bad in root for bad in badnames):
            if "__init__.py" in files:
                package_list.append( root.replace("/",".").replace("\\",".").strip('.') )
    return package_list

cbe_packages = find_packages('cbe/')

setup(name='cbe',
    version='0.5-alpha',
    packages=cbe_packages
)
