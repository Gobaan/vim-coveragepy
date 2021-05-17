let s:CoveragePyShow = {}

function! s:test_and_set_mode(target, next)
    if w:mode == a:target
        let w:mode = a:next
        return 1
    endif
    return 0
endfunction

function! CoveragePyShow#GotoTest()
    if !s:test_and_set_mode('Tests', 'Tests')
        return
    endif

python3 << endpython
import vim
import mark_coverage

line = vim.current.line
test, status = line.split(' ... ')
filename, function_name = test.split('::')
filename = mark_coverage.get_absolute_path(filename)
cmd = f"execute ':tabedit {filename}'"
vim.command(cmd)
cmd = f"execute '/def {function_name}'"
vim.command(cmd)
endpython
endfunction


function! CoveragePyShow#ShowException()
    if !s:test_and_set_mode("Tests", "Exceptions")
        return
    endif
python3 << endpython
import vim
import mark_coverage
b = '\n'.join(vim.current.buffer[:])
w = vim.current.window
w.vars['saved_text'] = b
line = vim.current.line
test, status = line.split(' ... ')
filename, function_name = test.split('::')
message = mark_coverage.show_exception(function_name)
filename = mark_coverage.get_absolute_path(filename)
cmd = f"""execute ':call vimPanel#Render("{message}", "coveragepy_exception")'"""
vim.command(cmd)
endpython
endfunction

function! CoveragePyShow#LoadSavedPanel()
    if !s:test_and_set_mode("Exceptions", "Tests")
        return
    endif

python3 << endpython
import vim
message = vim.current.window.vars['saved_text'].decode('utf-8')
cmd = f"""execute ':call vimPanel#Render("{message}", "coveragepy")'"""
vim.command(cmd)
endpython
endfunction

function! CoveragePyShow#ShowTests()

python3 << endpython
import vim
import vim_mark_coverage
window = vim.current.window
pos = window.cursor
vim_mark_coverage.show_tests(vim.current.buffer, pos[0])
endpython
    " Bind a hotkey to the panel just created
    call keyMap#Create({'scope':'coveragepy', 'text': 'press o to open failing test', 'key': 'o', 'callback': function  ('CoveragePyShow#GotoTest')})
    call keyMap#Create({'scope':'coveragepy', 'text': 'press e to display exception', 'key': 'e', 'callback': function  ('CoveragePyShow#ShowException')})
    call keyMap#Create({'scope':'coveragepy_exception', 'text': 'press u to go back to test results', 'key': 'u', 'callback': function  ('CoveragePyShow#LoadSavedPanel')})
    call keyMap#BindAll()
    let w:mode = 'Tests'
endfunction

:call CoveragePyWatch#EnableImports()
