#!/usr/bin/env python

# Standard modules

from __future__ import print_function
import re
import shlex
import subprocess
import sys

# Variables

new = ('1.5', '1.5.1')
old = ('1.5', '1.5.0')
pyenv_versions = ('2.7.11', '3.5.1')
python_version_sphinx = '2.7.11'
sdist_version = '2.7.11'

# Functions

def reify(s):
    return re.sub(r'\.', '\\.', s)

def replace(replacements, filenames):
    if not isinstance(replacements, list):
        replacements = [replacements]
    if not isinstance(filenames, list):
        filenames = [filenames]
    for f in filenames:
        c = open(f).read().split('\n')
        for i in range(len(c)):
            for r in replacements:
                c[i] = re.sub(r[0], r[1], c[i])
        c = '\n'.join(c)
        h = open(f, 'wb')
        h.write(c.encode('utf8'))
        h.close()

def run(command):
    print(':: %s' % command)
    c = shlex.split(command)
    pipe = subprocess.PIPE
    p = subprocess.Popen(c, stdout=pipe, stderr=pipe)
    (out, err) = p.communicate()
    ret = p.wait()
    if ret != 0:
        raise Exception('Command failed: "%s"!' % command)
    return out.decode('utf8')

def run_(command):
    print(':: %s' % command)
    c = shlex.split(command)
    p = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, \
        stderr=sys.stderr)
    ret = p.wait()
    if ret != 0:
        raise Exception('Command failed: "%s"!' % command)

def main():

    # ensure entry in versions table
    c = open('README.rst').read().split('\n')
    found = False
    for l in c:
        if re.match(r'\| %s ' % reify(new[1]), l):
            found = True
            break
    if not found:
        raise Exception('Add an entry to the versions table in README.rst!')

    # store original python version
    pyenv_orig = run('pyenv version') #.split(' ')[0]

    # test with each python version
    for v in pyenv_versions:
        run('pyenv global %s' % v)
        run_('py.test')

    # update versions in files
    replace(
        [
            (reify(old[1]), new[1]),
        ],
        [
            'doc/source/conf.py',
            'kron.py',
            'setup.py',
            'test_kron.py',
        ],
    )
    replace(
        [
            (
                r'^version = u\'%s\'' % reify(old[0]),
                "version = u'%s'" % new[0],
            ),
        ],
        'doc/source/conf.py',
    )

    # github
    run('git clean -dxf')
    run('git add *')
    run(r'git commit -m release\ %s' % new[1])
    run_('git push')

    # sphinx documentation
    run('pyenv global %s' % python_version_sphinx)
    run('mkdir doc/source/_static')
    run('python setup.py build_sphinx upload_sphinx')

    # source distribution to pypi
    run('pyenv global %s' % sdist_version)
    run('python setup.py sdist upload')

    # wheel distributions to pypi
    for v in pyenv_versions:
        run('pyenv global %s' % v)
        run('python setup.py bdist_wheel upload')

    # restore original python version
    run('pyenv global %s' % pyenv_orig)

# Main

if __name__ == '__main__':
    main()

