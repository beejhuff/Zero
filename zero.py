# -*- coding: utf-8 -*-
from random_words import RandomNicknames
import os
import rumps

rand_nicks = RandomNicknames()

# Reads the Computer, Host, Local names


def readScanUtility(tool):
    computer_name = os.popen("scutil --get ComputerName").read().strip()
    host_name = os.popen("scutil --get HostName").read().strip()
    local_host_name = os.popen("scutil --get LocalHostName").read().strip()
    if tool == "computer":
        return computer_name
    elif tool == "host":
        return host_name
    elif tool == "local":
        return local_host_name

# Change Computer, Host, Local names


def changeScanUtility(tool):
    raw_name = rand_nicks.random_nicks()
    new_name = "".join(raw_name + list('-PC'))
    notification = rumps.notification("Notification", "Your Computer Name has been changed to",
                       new_name, sound=None)
    if tool == "computer":
        return os.popen("sudo scutil --set ComputerName " + new_name).read().strip()
        notification
    elif tool == "host":
        return os.popen("sudo scutil --set HostName " + new_name).read().strip()
        notification
    elif tool == "local":
        return os.popen("sudo scutil --set LocalHostName " + new_name).read().strip()
        notification

# Reads the MAC Address of Wi-Fi


def readMacAddress(kind):
    hardwareDevice = detectAllHardware("device")
    # Scans all the Interfaces on the device and greps only Wi-Fi
    original_Mac = os.popen("networksetup -listallhardwareports | grep 'Ethernet Address:' | cut -c19-35 | awk 'NR==1{print $1}'").read().strip()
    # greps the current mac address
    current_mac = os.popen("ifconfig " + hardwareDevice +
                           " | grep ether | cut -d ' ' -f 2").read().strip()
    if kind == "current":
        return current_mac
    elif kind == "original":
        return original_Mac

# Checking if wifi is running


def checkWiFiStatus():
    wifiStatus = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep -w 'state' | cut -c18-24").read().strip()

    if wifiStatus == "running":
        return os.popen("sudo /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -z").read().strip()

# Checks for all Hardware Port(Human Readable name for Interface) and Device(Interface)


def detectAllHardware(typeOfHardware):
    # Changed Device from 'Device', 'Device' was giving extra /n as an output
    hardwareDevice = os.popen("networksetup -listallhardwareports | grep Device | awk 'NR==1{print $2}'").read().strip()
    hardwarePort = os.popen("networksetup -listallhardwareports | grep 'Hardware Port' | awk 'NR==1{print $3}'").read().strip()
    if typeOfHardware == "port":
        return hardwarePort
    elif typeOfHardware == "device":
        return hardwareDevice
    elif typeOfHardware == "all":
        return hardwarePort + " - " + hardwareDevice


@rumps.clicked(readMacAddress("current"), "Disable IPv6")
def toggleIPv6(sender):
    sender.title = "Enable IPv6" if sender.title == "Disable IPv6" else "Disable IPv6"
    if sender.title == "Disable IPv6":
        return os.popen("sudo networksetup -setv6automatic Wi-Fi")

    elif sender.title == "Enable IPv6":
        return os.popen("sudo networksetup -setv6off Wi-Fi")


@rumps.clicked(readMacAddress("current"), "Randomize")
def randomizedMac(sender):
    checkWiFiStatus()
    hardwareDevice = detectAllHardware("device")
    raw_mac = os.popen("openssl rand -hex 6").read().strip()
    new_mac = ':'.join([raw_mac[i:i+2] for i in range(0, len(raw_mac), 2)])
    # testing return_value
    return_value = os.popen("sudo ifconfig " + hardwareDevice + " ether %s" % new_mac).read().strip()
    return return_value

    os.popen("networksetup -setairportpower en0 off")
    os.popen("networksetup -setairportpower en0 on")
    rumps.notification("Notification", "Your MAC Address is Randomized.",
                       new_mac, sound=None)
#     randomizedMac.has_been_called = True
# randomizedMac.has_been_called = False


@rumps.clicked(readMacAddress("current"), "Restore Original")
def restoreOriginal(sender):
    checkWiFiStatus()
    hardwareDevice = detectAllHardware("device")
    getOriginalMac = readMacAddress("original")
    os.popen("sudo ifconfig " + hardwareDevice + " ether %s" % getOriginalMac).read().strip()
    os.popen("networksetup -setairportpower en0 off")
    os.popen("networksetup -setairportpower en0 on")

    rumps.notification("Notification", "Your MAC Address has been Restored.",
                       getOriginalMac, sound=None)


@rumps.timer(1)
def checkForMacLeak(sender):
    current_mac = readMacAddress("current")
    original_mac = readMacAddress("original")
    if current_mac == original_mac:
        app.icon = "leaked.png"
        rumps.notification("Notification", "Your MAC Address is leaking.",
                           original_mac, sound=None)
    else:
        app.icon = "normal.png"


# @rumps.timer(1)
# def updating(sender):
        # Scans MAC Address every second and stores it in current_mac
##     current_mac = readMacAddress("current")
    # If Randomized have been called, then the block bellow executes
#     if randomizedMac.has_been_called:
#         randomized_Mac = readMacAddress("current")
#         if current_mac != randomized_Mac:
#               sender.title = readMacAddress("current")
#               sender.title[readMacAddress("current")] = readMacAddress("current")
#               app.menu[readMacAddress("current")] = readMacAddress("current")


@rumps.clicked(readMacAddress("current"))
def refresh(sender):
    sender.title = readMacAddress("current") if sender.title ==\
        readMacAddress("current") else readMacAddress("current")


@rumps.clicked("Random Tools", "Change Computer Name")
def changeComputerName(sender):
    changeScanUtility("computer")


@rumps.clicked("Random Tools", "Change Local Hostname")
def changeLocalHostname(sender):
    changeScanUtility("local")


@rumps.clicked("Random Tools", "Change Hostname")
def changeHostname(sender):
    changeScanUtility("host")


@rumps.clicked("Utilities", "Enable Sudo Security")
def toggleSudoSec(sender):
    sender.title = "Disable Sudo Security" if sender.title == "Enable Sudo Security" else "Enable Sudo Security"
#    sudo echo "Defaults    env_reset,timestamp_timeout=0" | sudo tee -a /etc/sudoers | sudo echo "Defaults    tty_tickets" | sudo tee -a /etc/sudoers
    rumps.notification("Notification", "To Disable this option, please uncheck it.",
                            "", sound=None)


@rumps.clicked("Utilities", "Enable User Folder Security")
def toggleUserSecurity(sender):
    all_users = os.listdir("/Users/")
    all_users.remove(".localized")
    all_users.remove("Shared")
    sender.title = "Disable User Folder Security" if sender.title == "Enable User Folder Security" else "Enable User Folder Security"
    if sender.title == "Enable User Folder Security":
        for item in all_users:
            path = "/Users/%s" % item
            os.chmod(path, 0755)
    elif sender.title == "Disable User Folder Security":
        for item in all_users:
            path = "/Users/%s" % item
            os.chmod(path, 0700)


@rumps.clicked("Utilities", "Show Hidden Files")
def toggleHiddenFiles(sender):
    sender.title = "Hide Hidden Files" if sender.title == "Show Hidden Files" else "Show Hidden Files"
    if sender.title == "Show Hidden Files":
        os.popen("defaults write com.apple.finder AppleShowAllFiles false")
        os.popen("killall Finder")

    elif sender.title == "Hide Hidden Files":
        os.popen("defaults write com.apple.finder AppleShowAllFiles true")
        os.popen("killall Finder")


@rumps.clicked("Utilities", "Disable Captive Portal")
def toggleCaptivePortal(sender):
    sender.title = "Enable Captive Portal" if sender.title == "Disable Captive Portal" else "Disable Captive Portal"
    if sender.title == "Enable Captive Portal":
        os.popen("sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -bool false")
        rumps.notification("Notification", "Captive Portal is Disabled.",
                            "", sound=None)

    elif sender.title == "Disable Captive Portal":
        os.popen("sudo defaults write /Library/Preferences/SystemConfiguration/com.apple.captive.control Active -bool true")
        rumps.notification("Notification", "Captive Portal is Enabled.",
                            "", sound=None)


@rumps.clicked("Utilities", "Clear Download Logs")
def toggleDownloadLogs(sender):
    print "Download Logs are cleared!"
    os.popen("sudo rm -rfv /Volumes/*/.Trashes; sudo rm -rfv ~/.Trash; sudo rm -rfv /private/var/log/asl/*.asl; sqlite3 ~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV* 'delete from LSQuarantineEvent'")
    rumps.notification("Notification", "Download Logs are cleared.",
                            "", sound=None)

# @rumps.clicked("Launch at startup")
# def toggle(sender):
#     sender.state = not sender.state
#     if sender.state:
#         rumps.notification("Notification", "To Disable this option, please uncheck it.",
#                            "", sound=None)

# def manualMac(sender):
#     response = rumps.Window("Enter MAC Address:", dimensions=(200, 20)).run()
#     if response.clicked:
#         rumps.notification("Notification", "Your MAC Address is set to: " +
#                            response.text, "", sound=None)


@rumps.clicked("Help")
def toggleHelp(sender):
    rumps.notification("Notification", "Add Help Window.",
                           "", sound=None)
    print "Help is here!"


app = rumps.App("Right Tool For The Right Job.", title=None, icon='normal.png')
app.menu = [
    rumps.MenuItem(detectAllHardware("all")), {readMacAddress("current"):
    ["Disable IPv6", "Randomize", None, "Restore Original", readMacAddress("original")]}, None,
    {"Utilities": ["Clear Download Logs", "Enable User Folder Security", "Enable Sudo Security", "Disable Captive Portal", None,
    "Show Hidden Files"]}, None, {"Random Tools": ["Change Computer Name", "Change Local Hostname",
                      "Change Hostname"]}, None, rumps.MenuItem("Launch at startup"), "Help",
]
app.run()
