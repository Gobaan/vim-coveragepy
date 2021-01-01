let s:CoverageShow = {}
function! CoveragePyShow#GotoTest()
    " take the buffer line, split it and go to the function
python3 << endpython
import vim
import mark_coverage
line = vim.current.line
test, status = line.split(' ... ')
filename, function_name = test.split('::')
print (filename)
filename = mark_coverage.get_absolute_path(filename)
cmd = f"execute ':tabedit {filename}'"
vim.command(cmd)
cmd = f"execute '/def {function_name}'"
vim.command(cmd)
endpython
endfunction

" TODO: Factor this out and call it seperately
function! CoveragePyShow#ShowTests()
python3 << endpython
import vim
import vim_mark_coverage
window = vim.current.window
pos = window.cursor
vim_mark_coverage.show_tests(vim.current.buffer, pos[0])
endpython
    " Bind a hotkey to the panel just created
    call keyMap#Create({'scope':'example', 'text': 'press g to goto failing test', 'key': 'g', 'callback': function  ('show_results#goto_test')})
    call keyMap#Create({'scope':'example', 'text': 'press e to display exception', 'key': 'e', 'callback': function  ('show_results#show_exception')})
    call keyMap#BindAll()
endfunction

:call CoveragePyWatch#EnableImports()
