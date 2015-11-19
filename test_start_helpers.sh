#!/bin/bash
# Helpers for commandline scripts related to appium tests.

function get_full_path {
  echo "$( cd "$(dirname "$1")"; echo "$(pwd)/$(basename "$1")" )"
}

function android_reboot_and_wait_for_device_ready {
  echo "Rebooting android device"
  adb reboot
  sleep 5
  adb wait-for-device
  while [ -z "$(adb shell getprop sys.boot_completed | tr -d '\r')" ]; do
    sleep 1
    printf "_"
  done
  until [ "$(adb shell getprop sys.boot_completed | tr -d '\r')" -eq 1 ]; do
    sleep 1
    print "."
  done
  echo
  echo "Rebooted"
}

function start_script {
  npm install chai@2.1.2 colors underscore chai-as-promised wd path mkdirp yiewd tail mocha mocha-junit-reporter
  echo "mocha executable: '$(file node_modules/.bin/mocha)'"
  MOCHA_BIN='./node_modules/.bin/mocha'

  echo "Running tests '$TEST'"
  if [ "$TESTDROID" == "1" ]; then
    ${MOCHA_BIN} "${TEST}" --reporter mocha-junit-reporter --reporter-options mochaFile=./TEST-all.xml 2>&1
  else
    ${MOCHA_BIN} "$TEST"
  fi
  return $?
}
