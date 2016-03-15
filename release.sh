#!/bin/sh

set -eo pipefail

prev=1.4.1
new=1.4.2

newre=$(echo $new |sed 's/\./\\./g')
prevre=$(echo $prev |sed 's/\./\\./g')

run() {
    echo :: $1
    $1
    echo
}

echo :: grep \\\|\\ $newre README.rst
grep \|\ $newre README.rst
echo

run "py.test"

run "sed -i '' s/$prevre/$new/ doc/source/conf.py kron.py setup.py test_kron.py"

run "git clean -dxf"

run "git add *"

echo :: git commit -m release\\ $new
git commit -m release\ $new
echo

run "git push"

run "mkdir doc/source/_static"
run "python setup.py build_sphinx upload_sphinx"
run "python setup.py sdist bdist_wheel upload"


