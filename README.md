This integrate vim with coveragepy 5.3, which tracks which tests cover which lines. This means we can mark
uncovered tests, as well as all the lines passed by a failing test.

![alt text](https://github.com/gobaan/master/example.gif "Example of vim coverage in action")

First needs you to run coverage in the root folder

```
 py.test --cov -rA > out.txt
```

To install using Vundle add the following two lines to plugins.vim

```vim
Plugin 'gobaan/vim-panel'
Plugin 'gobaan/vim-coveragepy'
```

And the following line to your .vimrc

```vim
command ShowTests call CoveragePyShow#ShowTests()
au BufRead *.py call CoveragePyWatch#AddCoverageMarks()
```

Use :ShowTests to show test cases covering a given line

Use o to open the test case shown in the test panel

Use e to load the exception related to a failed test case

Use u to go back to the main test panel
