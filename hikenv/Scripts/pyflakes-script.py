#!F:\learn_python\Hikvision\hikenv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pyflakes==2.3.1','console_scripts','pyflakes'
__requires__ = 'pyflakes==2.3.1'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyflakes==2.3.1', 'console_scripts', 'pyflakes')()
    )
