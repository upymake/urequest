#!/usr/bin/env bash

# specifies a set of variables to declare files to be used for code assessment
PACKAGE="urequest"

# specifies a set of variables to declare CLI output color
FAILED_OUT="\033[0;31m"
PASSED_OUT="\033[0;32m"
NONE_OUT="\033[0m"


entry-point-box() {
:<<DOC
    Provides pretty-printer check box
DOC
    echo "Start ${1} analysis ..."
}


remove-pycache() {
:<<DOC
    Removes python cache directories
DOC
    ( find . -depth -name __pycache__ | xargs rm -r )
}


check-black() {
:<<DOC
    Runs "black" code analyser
DOC
    entry-point-box "black" && ( black --check ${PACKAGE} )
}


check-flake() {
:<<DOC
    Runs "flake8" code analysers
DOC
    entry-point-box "flake" && ( flake8 ./ )
}


check-pylint() {
:<<DOC
    Runs "pylint" code analyser
DOC
    entry-point-box "pylint" && ( pylint $(find "${PACKAGE}/") )
}


check-mypy() {
:<<DOC
    Runs "mypy" code analyser
DOC
    entry-point-box "mypy" && ( mypy --package "${PACKAGE}" )
}


check-docstrings() {
:<<DOC
     Runs "pydocstyle" static documentation code style formatter
DOC
    entry-point-box "pydocstyle" && ( pydocstyle --explain --count ${PACKAGE} )
}


check-unittests() {
:<<DOC
    Runs unittests using "pytest" framework
DOC
    entry-point-box "unitests" && pytest
}


is-passed() {
:<<DOC
    Checks if code assessment is passed
DOC
    if [[ $? -ne 0 ]]; then
      echo -e "${FAILED_OUT}Code assessment is failed, please fix errors!${NONE_OUT}"
      exit 100
    else
      echo -e "${PASSED_OUT}Congratulations, code assessment is passed!${NONE_OUT}"
    fi
}


main() {
:<<DOC
    Runs "main" code analyser
DOC
    (
      remove-pycache
      check-black && \
      check-mypy && \
      check-pylint && \
      check-flake && \
      check-docstrings && \
      check-unittests && \
      is-passed
    )
}

main