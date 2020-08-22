#!/usr/bin/env bash


test-setup-package() {
:<<DOC
    Test 'package' setup
DOC
  echo -e "Test package setup"
  python setup.py install
  if [[ "$?" -ne 0 ]]; then
    echo "Package setup is failed"
    exit 100
  fi
}


test-package-install() {
:<<DOC
    Test package is installed
DOC
    echo -e "Test package is installed"
    (pip list | grep ${PACKAGE_NAME})  \
       || (echo 'Package was not installed' && exit 100)
}


test-package-version() {
:<<DOC
    Test "version" of a package
DOC
    echo -e "\n\n Test package version"
    (pip show ${PACKAGE_NAME} | grep ${PACKAGE_VERSION}) \
       || (echo 'Package image version is wrong' && exit 100)
}


cleanup() {
:<<DOC
    Cleans up environment
DOC
  echo -e 'Cleanup package builds' 
  rm -rf ${PACKAGE_NAME}.egg-info dist build && \
  pip uninstall -y ${PACKAGE_NAME}
  if [[ "$?" -ne 0 ]]; then
    echo -e 'Package was not removed'
    exit 100
  fi
}


main() {
:<<DOC
    Runs unit tests
DOC
  echo -e "uRequest package assessment ..."
  test-setup-package && \
  test-package-install && \
  test-package-version && \
  cleanup 
  echo -e "uRequest package is ready to go"
}


main
