#!/bin/sh

set -eo pipefail

prev=1.4.2
new=1.5.0

versions=( 2.7.11 3.5.1 )

newre=$(echo $new |sed 's/\./\\./g')
prevre=$(echo $prev |sed 's/\./\\./g')
pyenv_orig=$(pyenv version |cut -d\  -f1)

run() {
    echo :: $1
    $1
    echo
}

echo :: grep \\\|\\ $newre README.rst
grep \|\ $newre README.rst
echo

for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "py.test"
    done

run "sed -i '' s/$prevre/$new/ doc/source/conf.py kron.py setup.py test_kron.py"

run "git clean -dxf"
run "git add *"
echo :: git commit -m release\\ $new
git commit -m release\ $new
echo
run "git push"

run "pyenv global 2.7.11"
run "mkdir doc/source/_static"
run "python setup.py build_sphinx upload_sphinx"
run "python setup.py sdist upload"

for v in "${versions[@]}"; do
    run "pyenv global $v"
    run "python setup.py bdist_wheel upload"
    done

run "pyenv global $pyenv_orig"

