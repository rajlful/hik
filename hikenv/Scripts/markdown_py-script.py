#!F:\learn_python\Hikvision\hikenv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Markdown==3.3.4','console_scripts','markdown_py'
__requires__ = 'Markdown==3.3.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Markdown==3.3.4', 'console_scripts', 'markdown_py')()
    )
