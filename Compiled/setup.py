# Build up paper plane
# Run python setup.py py2exe
# ------------------------------------------
#      ^
#     / \
#    / ! \ You need Py2exe installed  !!!!!
#   /_____\
# 
# You can find it @
# http://www.py2exe.org/
# ------------------------------------------
from distutils.core import setup
import py2exe

setup(windows=["../Source/paper_plane.py"]) 