NativeScript for Sublime Text
==========================

*Build and deploy iOS and Android native applications using a single XML, CSS, and JavaScript code base*

[![NativeScript](https://raw.githubusercontent.com/Mitko-Kerezov/ns-sublime-plugin/master/ns-logo.png "NativeScript")](https://www.nativescript.org/ "NativeScript web site")

This package lets you run your mobile app on connected devices or in emulators, and synchronize your code changes to the running app without redeploying it. The package requires that the [NativeScript Command-Line Interface](https://www.npmjs.com/package/nativescript "NativeScript Command-Line Interface") is installed on your system.

Usage
===

After you install this package, you can access the available build and sync commands from **Tools** -> **NativeScript**.

* [Run on Device](#run-on-device "Build and deploy to device")
* [LiveSync](#livesync "LiveSync")
* [LiveSync on Save](#livesync-on-save "Enable LiveSync on Save")

### Run on Device

You can build and deploy your app on one device at a time with the **Tools** -> **NativeScript** -> **Build and Deploy** operation.

1. Connect your devices.
1. Select **Tools** -> **NativeScript** -> **Build and Deploy**.<br/>If you have connected multiple devices, Sublime Text will display a drop-down list of the connected devices with their unique identifiers and mobile platform.
1. If prompted, select the device on which you want to deploy.
1. Track the deployment process in the status bar and in the log.
1. After the deployment completes, run your app on device.

### LiveSync

You can synchronize all your changes to an app deployed on a connected device at once with the **Tools** -> **NativeScript** -> **LiveSync Application** operation. This operation replaces all application files at once.

1. Verify that you have connected your device and you have deployed the app.
1. Run your app.
1. Modify your code and save changes.
1. Select **Tools** -> **NativeScript** -> **LiveSync Application**.
1. Track the deployment process in the status bar and in the log.

### LiveSync on Save

You can toggle real-time synchronization of your code changes on save with the **Tools** -> **NativeScript** -> **LiveSync on Save** option.

When you modify your code and save your changes, your running app will refresh automatically if the device is connected to your system. This operation replaces only the modified application files.

1. Select **Tools** -> **NativeScript** -> **Enable LiveSync on Save**.
1. On your connected devices, run your app.
1. Modify your code and save changes.

The app refreshes automatically.

[Back to Top][1]

[1]: #nativescript-for-sublime-text
