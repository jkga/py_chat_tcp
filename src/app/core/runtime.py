import os
import sys
from dotenv import load_dotenv

# load to environment variable that is readable by pyinstaller
if getattr(sys, 'frozen', False):
  # global configurations
  #load_dotenv (find_dotenv())
  load_dotenv(
    dotenv_path = os.path.join(os.path.dirname(__file__),".env")
  )
else :
    pass
