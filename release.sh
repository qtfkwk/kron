#!/bin/sh

set -eo pipefail

prev_=1.6
new_=1.6
prev=1.6.11
new=1.6.12

sdist_version=2.7.12
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

# ensure entry added to versions list
echo :: grep \\\*\\ $newre docs/index.rst \>/dev/null
grep \*\ $newre docs/index.rst >/dev/null
echo

# test in each pyenv version
for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "py.test"
    done
run "pyenv global $pyenv_orig"

# update versions in files
run "sed -i _ s/$prevre/$new/ docs/conf.py kron.py setup.py test_kron.py"
echo ":: sed -i _ 's/^version = .*/version = u'\'$new_\''/' docs/conf.py"
sed -i _ 's/^version = .*/version = u'\'$new_\''/' docs/conf.py
echo

# github
run "git clean -dxf"
run "git add *"
echo :: git commit -m release\\ $new
git commit -m release\ $new
echo
run "git push"

# source distribution to pypi
run "pyenv global $sdist_version"
run "python setup.py sdist upload"
run "pyenv global $pyenv_orig"

# wheel distributions to pypi
for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "python setup.py bdist_wheel upload"
    done
run "pyenv global $pyenv_orig"

