import sys
import os

# Add the server directory to the Python path so that modules can be imported properly
# This will make imports work consistently across the project
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))