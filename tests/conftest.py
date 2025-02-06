import sys
from pathlib import Path

# this will add 'src' directory to sys.path thus enabling pytest to import my application and relevant packages
project_src = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(project_src))
