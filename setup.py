import os, sys, glob, fnmatch

from distutils.core import setup

def find_packages(srcdir):
    path_list = []
    badnames=["__pycache__",]
    for root, dirs, files in os.walk(srcdir):
        if not any(bad in root for bad in badnames):
            if "__init__.py" in files:
                path_list.append( root.replace("/",".").replace("\\",".").strip('.') )
    return path_list

cbe_packages = find_packages('cbe/')

setup(name='cbe',
    version='0.5-alpha',
    packages=cbe_packages
)
