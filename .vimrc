set nocompatible
set nu
colors desert

map <F2> :tabp<CR>
imap <F2> <Esc>:tabp<CR>a
map <F3> :tabn<CR>
imap <F3> <Esc>:tabn<CR>a
map <F5> :call CreateXetters()<CR>
imap <F5> <Esc>:call CreateXetters()<CR>a

set tabstop=2
set shiftwidth=2
set expandtab
set wrap
syntax on
set ai
set smartindent
set cindent
set incsearch
set wildmenu
set backspace=indent,eol,start
set hls!
set ruler
set ff=unix
set encoding=utf-8
set guioptions=
set hlsearch
set mouse=

function SetPhpSettings()
  set foldmethod=indent
  set tabstop=4
  set shiftwidth=4
endfunction
function CreateXetters()
  let l:indent = "    "
  let l:var_name = input ("Indiquer l'attribut à créer : ")

  " Génération de l'attribut version camel case sachant que j'arrive pas bien à manipuler 
  " les expressions régulières pour l'instant dans substitute : 
  "  * on remplace tous les "_." par la uppercase ("za_za_za" => "za_Za_Za").
  "  * on remplace la première lettre par la uppercase.
  "  * on vire tous les "_".
  " Sinon, on pourrait utiliser la regexp : s:/_\(.\)/\U\1/g. Mais bon...
  let l:camel_case_var_name = substitute (
      \l:var_name, 
      \"_.", 
      \"\\U\\0", 
      \"g")
  let l:camel_case_var_name = substitute (
      \l:camel_case_var_name, 
      \"^.", 
      \"\\U\\0", 
      \"")
  let l:camel_case_var_name = substitute (
      \l:camel_case_var_name, 
      \"_", 
      \"", 
      \"g")

  let l:attribute = l:indent . "private $" . l:var_name . ";"
  put = l:attribute
  let l:getter = l:indent . "public function get" . l:camel_case_var_name . "()\n
\" . l:indent . "{\n
\" . l:indent . l:indent . "return $this->" . l:var_name . ";\n
\" . l:indent . "}"
  put = l:getter
  let l:setter = l:indent . "public function set" . l:camel_case_var_name . "($" . l:var_name .")\n
\" . l:indent . "{\n
\" . l:indent . l:indent . "$this->" . l:var_name . " = $" . l:var_name . ";\n
\" . l:indent . l:indent . "return $this;\n
\" . l:indent . "}"
  put = l:setter

  let l:tester = l:indent . "/** \n
\" . l:indent . " * Fonction testant les Xetters " . l:var_name . ".\n
\" . l:indent . " **/\n
\" . l:indent . "/*\n
\" . l:indent . "$this->" . l:var_name . " = '1234';\n
\" . l:indent . "public function test" . l:camel_case_var_name . " (): void\n
\" . l:indent . "{\n
\" . l:indent . l:indent . "$this->set" . l:camel_case_var_name . " ($this->" . l:var_name .");\n
\" . l:indent . l:indent . "$this->assertEquals ($this->" . l:var_name .", $this->get". l:camel_case_var_name . "());\n
\" . l:indent . "}\n
\" . l:indent . "*/\n"
  put = l:tester
endfunction

au BufRead,BufNewFile *.html.twig set filetype=htmldjango
au BufRead,BufNewFile *.php call SetPhpSettings()
