#!/usr/bin/env bash

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
    fi
}

function start_tests_py {
    echo "Running tests '$TEST'"
    python "$TEST"
    return $?
}
