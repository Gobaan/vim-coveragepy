:sign define notcovered text=M
:sign define failing text=F
let g:plugin_path = expand('<sfile>:p:h')

function! EnableImports()
python3 << endpython
import os
import sys
import vim

plugin_path = vim.eval("g:plugin_path")
python_module_path = os.path.abspath('%s' % (plugin_path))
sys.path.append(python_module_path)
endpython
endfunction


function! MyVimPlugin()
python3 << endpython
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import mark_coverage

def is_keyword(word):
    return word.split()[0] in ('', 'def', 'class', 'else:')

def mark_buffer():
    cb = vim.current.buffer
    if not mark_coverage.handles(cb.name):
        return

    try:
        marker = mark_coverage.get_file_marker(cb.name)
        print ('got markers')
    except TypeError:
        print (f'no coverage information found for {cb.name}')
        return

    for line_number in range(len(cb)):
        sign = ''
        if not cb[line_number].strip():
            continue

        if marker.line_fails(line_number + 1):
            sign = 'failing'
        elif not marker.line_is_tested(line_number + 1) and not is_keyword(cb[line_number]):
            sign = 'notcovered'

        if sign:
            cmd = f"execute ':sign place {1000 + line_number} line={line_number + 1} name={sign} file={cb.name}'"
            vim.command(cmd)


print ('started')
mark_buffer()
class CoverageHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self,
        patterns=['*.coverage'],
        ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        print ("testing")
        vim.command("Coveragepy refresh")

path = '.'
event_handler = CoverageHandler()
observer = Observer()
observer.schedule(event_handler, path)
observer.start()
endpython
endfunction

:call EnableImports()
au VimEnter * call MyVimPlugin()
