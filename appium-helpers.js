/* jshint node: true, multistr: true */

var exec = require('child_process').exec,
  mkdirp = require("mkdirp");

// The buttons on the ad screen cannot be recognized by same appium methods
// on iOS as on Android, Use this method instead.
var staticTextElement = function(staticText, timeOut, pollInterval) {
  if(process.env.APPIUM_PLATFORM == "ios"){
    return this
      .waitForElementByIosUIAutomation('.scrollViews()[0]\
                                        .webViews()[0]\
                                        .staticTexts()["' + staticText+ '"]',
                                        timeOut, pollInterval);
  } else {
    return this
      .waitForElementByName(staticText, timeOut, pollInterval);
  }
};

// Use native Instruments for finding elements in iOS
var iosWaitElement = function(staticText, timeOut, pollInterval) {
  if(process.env.APPIUM_PLATFORM == "ios") {
    return this
      .waitForElementByIosUIAutomation('UIATarget.localTarget()\
                                        .frontMostApp()\
                                        .mainWindow()\
                                        .buttons()["' +staticText+ '"]',
                                        timeOut, pollInterval);
  }
  else {
    return this
      .waitForElementByName(staticText, timeOut, pollInterval);
  }

};

// Collect certain messages from log
var messagesFromLog = function(logType, regexFilter) {
  return this
    .log(logType)
    .then(function(logBuffer) {
      var entries = logBuffer.filter(function(entry) {
        return regexFilter.test(entry.message);
      });
      return entries;
    });
};

var jsonObjectsFromLog = function(logType, generalFilter, arrayOfFilterStrings) {
  var jsonObjects = {};
  return this
    .messagesFromLog(logType, generalFilter)
    .then(function(entries) {
      for( var i = 0 ; i < arrayOfFilterStrings.length ; i++ ) {
        var filterStr = arrayOfFilterStrings[i];
        var regex = new RegExp(filterStr);
        var messages = entries.filter(function(entry) {
          return regex.test(entry.message);
        });
        var lastMessage = messages[ messages.length -1 ];
        if(!lastMessage){
          throw new Error("No such message found! '" + filterStr + "'");
        }
        jsonObjects[filterStr] = parseJsonFromMessage(messages[ messages.length -1 ].message);
      }
      return jsonObjects;
    });
};

var logContexts = function(tagStr){
  return this
    .contexts()
    .then(function(contexts){
      console.log("Visible contexts at " + tagStr + ": " + contexts);
      return this;
    });
};

var screenShotLoop = function(fileName, index, max, cb){
  console.log("asked to screenshot '" + fileName + index + "', upto '" + max + "'");
  if(index >= max){
    cb();
  } else {
    var cmdLineCall = "adb shell screencap -p \"/sdcard/" + fileName + index + ".png\"";
    exec(cmdLineCall, function(){
      var nextIndex = index + 1;
      screenShotLoop(fileName, nextIndex, max, cb);
    });
  }
};

var burstScreenshot = function(fileName, photosCount, cb){
  screenShotLoop(fileName, 1, photosCount, function(){
    cb();
  });
};

var pullFileLoop = function(fileName, dest, index, max, cb){
  console.log("asked to pull '" + fileName + index + "', upto '" + max + "'");
  if(index >= max){
    cb();
  } else {
    exec("adb pull '/sdcard/" + fileName + index + ".png' " + dest + "", function(){
      nextIndex = index + 1;
      pullFileLoop(fileName, dest, nextIndex, max, cb);
    });
  }
};

var pullBursts = function(fileName, dest, photosCount, cb) {
    mkdirp(dest);
    pullFileLoop(fileName, dest, 1, photosCount, function(){
      cb();
    });
};

exports.configureWd = function(wd) {
  wd.addPromiseChainMethod('staticTextElement', staticTextElement);
  wd.addPromiseChainMethod('iosWaitElement', iosWaitElement);
  wd.addPromiseChainMethod('messagesFromLog', messagesFromLog);
  wd.addPromiseChainMethod('jsonObjectsFromLog', jsonObjectsFromLog);
  wd.addPromiseChainMethod('logContexts', logContexts);
  wd.addPromiseChainMethod('burstScreenshot', burstScreenshot);
  wd.addPromiseChainMethod('pullBursts', pullBursts);
};

exports.configureYiewdDriver = function(driver){
  driver.staticTextElement = staticTextElement;
  driver.iosWaitElement = iosWaitElement;
  driver.messagesFromLog = messagesFromLog;
  driver.jsonObjectsFromLog = jsonObjectsFromLog;
  driver.logContexts = logContexts;
};
