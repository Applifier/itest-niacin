#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function setup_virtualenv {
    virtualenv -p /usr/local/bin/python3 --no-site-packages --distribute .env
}

function install_libs_py {
    echo "installing py libs"
    if [ "$TESTDROID" == "1" ]; then
        sudo easy_install pip
        sudo pip install Appium-Python-Client unittest-xml-reporting
        #sudo brew install ios-webkit-debug-proxy

        export JUNIT_REPORT_STACK=1
        export JUNIT_REPORT_PATH="TEST-all.xml"
        JUNIT_REPORT_NAME="$DEVICE_NAME"
        JUNIT_REPORT_NAME=${JUNIT_REPORT_NAME:="No Device Name Set"}
        export JUNIT_REPORT_NAME
    else
        echo "using virtual env.."
        setup_virtualenv
        
        source "$SCRIPT_DIR/activate_venv.sh"
        pip install -r "$SCRIPT_DIR/requirements.txt"
    fi
}

function start_tests_py {
    echo "Running tests '$TEST'"
    python "$TEST"
    return $?
}

# Bash magic to call functions defined here from the CLI e.g.
## ./install_and_start_py.sh setup_virtualenv
"$@"
