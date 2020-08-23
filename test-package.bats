#!/usr/bin/env bats


@test "setup package" {
:<<DOC
    Test 'package' setup
DOC
  python setup.py install
  [ "$?" -eq 0 ]
}


@test "package install" {
:<<DOC
    Test package is installed
DOC
  pip list | grep ${PACKAGE_NAME}
  [ "$?" -eq 0 ]
}


@test "package version" {
:<<DOC
    Test "version" of a package
DOC
  pip show ${PACKAGE_NAME} | grep ${PACKAGE_VERSION}
  [ "$?" -eq 0 ]
}


@test "cleanup" {
:<<DOC
    Cleans up environment
DOC
  rm -rf ${PACKAGE_NAME}.egg-info dist build
  pip uninstall -y ${PACKAGE_NAME}
  [ "$?" -eq 0 ]
}
