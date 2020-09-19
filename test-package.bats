#!/usr/bin/env bats


setup() {
:<<DOC
  Installs urequest package
DOC
  python setup.py install
}


teardown() {
:<<DOC
  Removes urequest package
DOC
  rm -rf ${PACKAGE_NAME}.egg-info dist build
  pip uninstall -y ${PACKAGE_NAME}
}


@test "package name" {
:<<DOC
  Test package name
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


@test "install package via pip" {
:<<DOC
  Test 'package' setup
DOC
  pip install ${PACKAGE_NAME}==${PACKAGE_VERSION}
  [ "$?" -eq 0 ]
}

