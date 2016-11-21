#!/bin/sh

set -eo pipefail

prev_=1.6
new_=1.6
prev=1.6.7
new=1.6.8

versions=( 2.7.12 3.5.2 )

newre=$(echo $new |sed 's/\./\\./g')
prevre=$(echo $prev |sed 's/\./\\./g')
prev_re=$(echo $prev_ |sed 's/\./\\./g')

pyenv_orig=$(pyenv version |cut -d\  -f1)

run() {
    echo :: $1
    $1
    echo
}

# ensure entry added to versions table
echo :: grep \\\|\\ $newre doc/source/index.rst
grep \|\ $newre doc/source/index.rst
echo

# test in each pyenv version
for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "py.test"
    done
run "pyenv global $pyenv_orig"

# update versions in files
run "sed -i _ s/$prevre/$new/ doc/source/conf.py kron.py setup.py test_kron.py"
echo ":: sed -i _ 's/^version = .*/version = u'\'$new_\''/' doc/source/conf.py"
sed -i _ 's/^version = .*/version = u'\'$new_\''/' doc/source/conf.py
echo

exit

# generate documentation
run "sphinx-build doc/source doc/build/html"

# github
run "git clean -dxf"
run "git add *"
echo :: git commit -m release\\ $new
git commit -m release\ $new
echo
run "git push"

# source distribution to pypi
run "python setup.py sdist upload"

# wheel distributions to pypi
for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "python setup.py bdist_wheel upload"
    done
run "pyenv global $pyenv_orig"

