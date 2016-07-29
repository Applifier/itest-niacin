#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PYTHON=${PYTHON:=python3}
PIP=${PIP:=pip3}

function setup_virtualenv {
    virtualenv -p /usr/local/bin/python3 --no-site-packages --distribute .env
}


function venv_activation {
    setup_virtualenv
    source "$SCRIPT_DIR/activate_venv.sh"
}

function install_libs_py {
    echo "installing py libs"
    if [ "$TESTDROID" == "1" ]; then
        # TODO: after TestDroid fixes their env lets not use python3
        brew install ios-webkit-debug-proxy #python3
        sudo easy_install pip
        export JUNIT_REPORT_STACK=1
        export JUNIT_REPORT_PATH="TEST-all.xml"
        JUNIT_REPORT_NAME="$DEVICE_NAME"
        JUNIT_REPORT_NAME=${JUNIT_REPORT_NAME:="No Device Name Set"}
        export JUNIT_REPORT_NAME

        sudo $PIP install -r "$SCRIPT_DIR/requirements.txt"
    else
        # install python-packages inside the VirtualEnvironment
        venv_activation
        $PIP install -r "$SCRIPT_DIR/requirements.txt"
    fi
}

function start_tests_py {
    echo "Running tests '$TEST'"
    $PYTHON "$TEST"
    return $?
}

# Bash magic to call functions defined here from the CLI e.g.
## ./install_and_start_py.sh setup_virtualenv
"$@"
