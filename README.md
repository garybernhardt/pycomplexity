# pycomplexity

Scripts to show cyclomatic complexity of Python code in [Vim][VimHome] and [Emacs][EmacsHome].

Original vim script by **Gary Bernhardt**. Emacs support added by **Ignas Mikalajūnas**.

Patches contributed by:

 * Godefroid Chapelle
 * Steve Bedford
 * Chris Clark
 * Peter Prohaska


## vim plugin
Vim plugin is in *pycomplexity.vim* directory
![vim python complexity][VimScreenshot]

### install vim plugin with NeoBundle
If you're using [NeoBundle][NeoBundleRepository] plugin manager you can add this into ~/.vimrc:

```viml
NeoBundle 'garybernhardt/pycomplexity', {'rtp': 'pycomplexity.vim/'}
" optional F6 mapping to fire :Complexity command
nnoremap <silent> <F6> :Complexity<CR>
```

[VimHome]:http://www.vim.org/
[EmacsHome]:http://www.gnu.org/software/emacs/
[NeoBundleRepository]:https://github.com/Shougo/neobundle.vim
[VimScreenshot]:http://blog.extracheese.org/images/vim_complexity.png
