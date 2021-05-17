:sign define notcovered text=M
:sign define failing text=F
let g:plugin_path = expand('<sfile>:p:h')

function! CoveragePyWatch#EnableImports()
python3 << endpython
import os
import sys
import vim

plugin_path = vim.eval("g:plugin_path")
python_module_path = os.path.abspath('%s' % (plugin_path))
sys.path.append(python_module_path)
endpython
endfunction

function! CoveragePyWatch#AddCoverageMarks()
python3 << endpython
import vim_mark_coverage
vim_mark_coverage.mark_buffer(vim.current.buffer)
endpython
endfunction

function! CoveragePyWatch#AttachCoverageListener()
python3 << endpython
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
class CoverageHandler(PatternMatchingEventHandler):
    def __init__(self):
        PatternMatchingEventHandler.__init__(self,
        patterns=['*.coverage'],
        ignore_directories=True, case_sensitive=False)

    def on_created(self, event):
        vim.command("Coveragepy refresh")

path = '.'
event_handler = CoverageHandler()
observer = Observer()
observer.schedule(event_handler, path)
observer.start()
endpython
endfunction

function! CoveragePyWatch#RecalculateCoverageMarks()
python3 << endpython
import subprocess
import vim_mark_coverage
import mark_coverage
import os.path

working_directory = mark_coverage.find_coverage_folder()
with open(os.path.join(working_directory, 'out.txt'), 'w') as fp:
    p = subprocess.run(['py.test', '--cov', '-rf'], stdout=fp, cwd=working_directory)

endpython

tabdo call CoveragePyWatch#AddCoverageMarks()
endfunction

:call CoveragePyWatch#EnableImports()
command RunCoverage call CoveragePyWatch#RecalculateCoverageMarks()
au BufRead *.py call CoveragePyWatch#AddCoverageMarks()
