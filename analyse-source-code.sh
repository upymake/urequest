#!/usr/bin/env bash

PACKAGE="urequest"


--entry-point-box() {
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
    --entry-point-box "black" && ( black --check ${PACKAGE} )
}


check-flake() {
:<<DOC
    Runs "flake8" code analysers
DOC
    --entry-point-box "flake" && ( flake8 ${PACKAGE} )
}


check-pylint() {
:<<DOC
    Runs "pylint" code analyser
DOC
    --entry-point-box "pylint" && ( pylint $(find "${PACKAGE}/") )
}


check-mypy() {
:<<DOC
    Runs "mypy" code analyser
DOC
    --entry-point-box "mypy" && ( mypy --package "${PACKAGE}" )
}


check-docstrings() {
:<<DOC
     Runs "pydocstyle" static documentation code style formatter
DOC
    --entry-point-box "pydocstyle" && ( pydocstyle --explain --count ${PACKAGE} )
}


check-unittests() {
:<<DOC
    Runs unittests using "pytest" framework
DOC
    --entry-point-box "unitests" && pytest
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
      check-unittests
    )
}

main