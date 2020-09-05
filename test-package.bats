#!/usr/bin/env bats


uninstall-package() {
:<<DOC
    Uninstalls a package
DOC
  pip uninstall -y ${PACKAGE_NAME}
}


@test "custom setup package" {
:<<DOC
    Test 'package' setup
DOC
  python setup.py install
  [ "$?" -eq 0 ]
}


@test "custom package install" {
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


@test "uninstall custom package" {
:<<DOC
    Test "uninstall package"
DOC
  uninstall-package
  [ "$?" -eq 0 ]
}


@test "install package via pip" {
:<<DOC
    Test 'package' setup
DOC
  pip install ${PACKAGE_NAME}==${PACKAGE_VERSION}
  [ "$?" -eq 0 ]
}


@test "cleanup" {
:<<DOC
    Cleans up environment
DOC
  rm -rf ${PACKAGE_NAME}.egg-info dist build
  uninstall-package
  [ "$?" -eq 0 ]
}
