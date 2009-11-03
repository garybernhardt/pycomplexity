" complexity.vim
" Gary Bernhardt (http://blog.extracheese.org)
"
" This will add cyclomatic complexity annotations to your source code. It is
" no longer wrong (as previous versions were!)

python << endpython
%(python_source)s
endpython

function! ShowComplexity()
    python << END
show_complexity()
END
endfunction

hi SignColumn guifg=fg guibg=bg
hi low_complexity guifg=#004400 guibg=#004400
hi medium_complexity guifg=#bbbb00 guibg=#bbbb00
hi high_complexity guifg=#ff2222 guibg=#ff2222
sign define low_complexity text=XX texthl=low_complexity
sign define medium_complexity text=XX texthl=medium_complexity
sign define high_complexity text=XX texthl=high_complexity

autocmd! BufReadPost,BufWritePost,FileReadPost,FileWritePost *.py call ShowComplexity()

