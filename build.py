#!/usr/bin/env python

if __name__ == '__main__':
    py_src = file('complexity.py').read()
    vim_src = file('base.vim').read()
    combined_src = vim_src % dict(python_source=py_src)
    file('complexity.vim', 'w').write(combined_src)

