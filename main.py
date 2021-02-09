#! /usr/bin/env python

import datetime
import logging
import os
import time
import xml.dom.minidom

global app


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def check_chrome():
    os.system('adb shell input keyevent KEYCODE_HOME')
    print('Checking Chrome...')
    chrome = dom_report.createElement('Chrome')
    app.appendChild(chrome)
    preload = dom_report.createElement('Preload')
    # check chrome is preloaded or not
    test = 'adb shell pm list packages -i | grep -c com.android.chrome'
    result = os.popen(test).read()
    if int(result) == 1:
        print('Chrome is preloaded')
        logging.info('Chrome is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Chrome is not preloaded")
        logging.error('Chrome is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Chrome is not preloaded')
        preload.appendChild(false_statement)
    chrome.appendChild(preload)
    default = dom_report.createElement('Default')
    # check default browser
    test = 'adb shell am start -W -a android.intent.action.VIEW -d "http://www.baidu.com/" | grep -c ' \
           'com.android.chrome '
    result = os.popen(test).read()
    time.sleep(1)
    if int(result) == 1:
        print("Chrome is the default browser")
        logging.info('Chrome is the default browser')
        default.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Chrome is not the default browser")
        logging.error('Chrome is not the default browser')
        default.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Chrome is not default')
        preload.appendChild(false_statement)
    chrome.appendChild(default)
    time.sleep(2)
    os.system('adb shell am force-stop com.android.chrome')  # force-stop the process
    time.sleep(2)
    os.system('adb shell input keyevent KEYCODE_HOME')
    # check if Chrome is at hotseat or not
    hotseat = dom_report.createElement('Hotseat')
    os.system('adb pull $(adb shell uiautomator dump | grep -oP "[^ ]+.xml") /tmp/view.xml')
    os.system('adb pull sdcard/window_dump.xml')
    test1 = 'xmllint /tmp/view.xml --xpath "//node[contains(@resource-id,"hotseat")]/node/node/@text" | grep -c Chrome'
    test2 = 'xmllint /tmp/view.xml --xpath "//node[contains(@resource-id,"hotseat")]/node/node/node/@text" | grep -c ' \
            'Chrome '
    if int(os.popen(test1).read()) == 1 or int(os.popen(test2).read()) == 1:
        print('Chrome is at hotseat')
        logging.info('Chrome is at hotseat')
        hotseat.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + 'Chrome is not at hotseat')
        logging.error('Chrome is not at hotseat')
        hotseat.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Chrome is not at hotseat')
        hotseat.appendChild(false_statement)
    os.system('rm window_dump.xml')
    chrome.appendChild(hotseat)


def check_photo():
    print("\nChecking Google Photo...")
    photo = dom_report.createElement('Photo')
    app.appendChild(photo)
    default_pick = dom_report.createElement('Default_pick_image')
    # Check Gallery Go is default or not
    test = 'adb shell am start -W -a android.intent.action.PICK -t image/* | grep -c com.google.android.apps.photos'
    result = os.popen(test).read()
    if int(result) == 1:
        print("Google Photo is the default app to pick image")
        logging.info('Google Photo is the default app to pick image')
        default_pick.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Google Photo is not the default app to pick image")
        logging.error('Google Photo is not the default app to pick image')
        default_pick.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Photo is not the default app to pick image')
        default_pick.appendChild(false_statement)
    default_review = dom_report.createElement('Default_review_image')
    test = 'adb shell am start -W -a com.android.camera.action.REVIEW -t image/* | grep -c ' \
           'com.google.android.apps.photos '
    result = os.popen(test).read()
    if int(result) == 1:
        print("Google Photo is the default app to review image")
        logging.info('Google Photo is the default app to review image')
        default_review.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Google Photo is not the default app to review image")
        logging.error('Google Photo is not the default app to review image')
        default_review.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Photo is not the default app to review image')
        default_review.appendChild(false_statement)
    photo.appendChild(default_pick)
    photo.appendChild(default_review)
    time.sleep(3)
    os.system('adb shell am force-stop com.google.android.apps.photos')
    time.sleep(1)
    print("Check Camera preview Gallery\n" + Color.BOLD + Color.BLUE + "Open camera, capture a photo and check whether "
                                                                       "Gallery Go is the default gallery" + Color.END)
    os.system('adb shell am start -W -a android.media.action.STILL_IMAGE_CAMERA')
    time.sleep(1)
    os.system("adb shell input keyevent 27")
    time.sleep(1)


def check_messages():
    print("\nChecking Message app...")
    messsage = dom_report.createElement('Message')
    app.appendChild(messsage)
    preload = dom_report.createElement('Preload')
    # Check Android Messages is preloaded
    test = 'adb shell pm list features | grep -c android.hardware.telephony'
    result = os.popen(test).read()
    if int(result) == 0:
        print('Tablet does not requires to preload Android Message')
        logging.info('Tablet does not requires to preload Android Message')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Tablet does not requires to preload Android Message')
        preload.appendChild(false_statement)
        messsage.appendChild(preload)
        return
    test = 'adb shell pm list packages -i | grep -c com.google.android.apps.messaging'
    result = os.popen(test).read()
    if int(result) == 1:
        print("Android Message is preloaded")
        logging.info('Android Message is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + "Android Message is not preloaded")
        logging.error('Android Message is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Android Message is not preloaded')
        preload.appendChild(false_statement)
    messsage.appendChild(preload)
    time.sleep(1)
    os.system('adb shell input keyevent 03')
    hotseat = dom_report.createElement('Hotseat')
    # Check Android Message is at the hotseat
    os.system('adb pull $(adb shell uiautomator dump | grep -oP "[^ ]+.xml") /tmp/view.xml')
    os.system('adb pull sdcard/window_dump.xml')
    test1 = 'xmllint /tmp/view.xml --xpath "//node[contains(@resource-id,"hotseat")]/node/node/@text" | grep -c ' \
            'Messages '
    test2 = 'xmllint /tmp/view.xml --xpath "//node[contains(@resource-id,"hotseat")]/node/node/node/@text" | grep -c ' \
            'Messages '
    if int(os.popen(test1).read()) == 1 or int(os.popen(test2).read()) == 1:
        print("Messages is at hotseat")
        logging.info('Message is at hotseat')
        hotseat.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + "Messages is not at hotseat")
        logging.error('Messages is not at hotseat')
        hotseat.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Messages is not at hotseat')
        hotseat.appendChild(false_statement)
    os.system('rm window_dump.xml')
    messsage.appendChild(hotseat)
    # Check default messages
    default = dom_report.createElement('Default')
    test = 'adb shell am start -W -a android.intent.action.SENDTO -d sms:CCXXXXXXXXXX | grep -c ' \
           'com.google.android.apps.messaging '
    result = os.popen(test).read()
    if int(result) == 1:
        print("Android Message is the default")
        logging.info('Android Message is the default')
        default.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + "Android Message is not the default")
        logging.error('Android Message is not the default')
        default.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Messages is not the default')
        default.appendChild(false_statement)
    messsage.appendChild(default)
    # Check Android Messages flag
    flag = dom_report.createElement('Flag')
    test = 'adb shell getprop | grep ro.com.google.acsa | grep -c true'
    result = os.popen(test).read()
    if int(result) == 1:
        print('Android Message ro.com.google.acsa is' + Color.BOLD + Color.RED + 'set' + Color.END)
        logging.info('Android Message ro.com.google.acsa is set')
        flag.setAttribute("Result", "Pass")
    else:
        print(
            Color.BOLD + Color.RED + "Error!!!" + Color.END + "Android Message ro.com.google.acsa is not " + Color.BOLD
            + Color.RED + 'set' + Color.END)
        logging.error('Android Message ro.com.google.acsa is not set')
        flag.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Android Message ro.com.google.acsa is not set')
        flag.appendChild(false_statement)
    messsage.appendChild(flag)
    time.sleep(3)
    os.system('adb shell am force-stop com.google.android.apps.messaging')
    time.sleep(1)


def check_calendar():
    print('\nChecking Google Calendar...')
    calendar = dom_report.createElement('Calendar')
    app.appendChild(calendar)
    preload = dom_report.createElement('Preload')
    test = 'adb shell pm list packages -i | grep -c com.google.android.calendar'
    result = os.popen(test).read()
    if int(result) == 1:
        print('Google Calendar is preloaded')
        logging.info('Google Calendar is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Google Calendar is not preloaded")
        logging.error('Google Calendar is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Android Message ro.com.google.acsa is not set')
        preload.appendChild(false_statement)
    calendar.appendChild(preload)
    test = 'adb shell am start -W -a android.intent.action.VIEW -d content://com.android.calendar/time/1410665898789 ' \
           '| grep -c com.google.android.calendar '
    result = os.popen(test).read()
    default = dom_report.createElement('Default')
    if int(result) == 1:
        print("Google Calendar is the default Calendar")
        logging.info('Google Calendar is the default Calendar')
        default.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + "Google Calendar is not the default Calendar")
        logging.error('Google Calendar is not the default Calendar')
        default.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Calendar is not default')
        default.appendChild(false_statement)
    calendar.appendChild(default)
    time.sleep(1)
    os.system('adb shell am force-stop com.google.android.calendar')
    time.sleep(1)


def check_gmail():
    print("\nChecking Gmail...")
    gmail = dom_report.createElement('Gmail')
    app.appendChild(gmail)
    preload = dom_report.createElement('Preload')
    test = 'adb shell pm list packages -i | grep -c com.google.android.gm'
    result = os.popen(test).read()
    if int(result) >= 1:
        print('Gmail is preloaded')
        logging.info('Gmail is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail is not preloaded")
        logging.error('Gmail is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Calendar is not default')
        preload.appendChild(false_statement)
    gmail.appendChild(preload)
    time.sleep(1)
    default = dom_report.createElement('Default')
    test = 'adb shell am start -W -a android.intent.action.SENDTO -d mailto:someone@gmail.com | grep -c ' \
           'com.google.android.gm '
    result = os.popen(test).read()
    if int(result) == 1:
        print('Gmail is the default Email')
        logging.info('Gmail is the default Email')
        default.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail is not the default Email")
        logging.error('Gmail is not the default Email')
        default.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gmail is not the default Email')
        default.appendChild(false_statement)
    gmail.appendChild(default)
    time.sleep(1)
    read_calendar = dom_report.createElement('Read_Calendar')
    test = 'adb shell dumpsys package com.google.android.gm | grep -c "android.permission.READ_CALENDAR: granted=true"'
    result = os.popen(test).read()
    if int(result) >= 1:
        print("Gmail can read calendar")
        logging.info('Gmail can read calendar')
        read_calendar.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail cannot read calendar")
        logging.error('Gmail cannot read calendar')
        read_calendar.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gmail cannot read calendar')
        read_calendar.appendChild(false_statement)
    gmail.appendChild(read_calendar)
    write_calendar = dom_report.createElement('Write_Calendar')
    time.sleep(1)
    test = 'adb shell dumpsys package com.google.android.gm | grep -c "android.permission.WRITE_CALENDAR: granted=true"'
    result = os.popen(test).read()
    if int(result) >= 1:
        print("Gmail can write calendar")

        logging.info('Gmail can write calendar')
        write_calendar.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail cannot write calendar")

        logging.error('Gmail cannot write calendar')
        write_calendar.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gmail cannot write calendar')
        write_calendar.appendChild(false_statement)
    gmail.appendChild(write_calendar)
    read_contacts = dom_report.createElement('Read_Contacts')
    time.sleep(1)
    test = 'adb shell dumpsys package com.google.android.gm | grep -c "android.permission.READ_CONTACTS: granted=true"'
    result = os.popen(test).read()
    if int(result) >= 1:
        print("Gmail can read contacts")
        logging.info('Gmail can read contacts')
        read_contacts.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail cannot read contacts")
        logging.error('Gmail cannot read contacts')
        read_contacts.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gmail cannot read contacts')
        read_contacts.appendChild(false_statement)
    gmail.appendChild(read_contacts)
    time.sleep(1)
    write_contacts = dom_report.createElement('Write_Contacts')
    test = 'adb shell dumpsys package com.google.android.gm | grep -c "android.permission.WRITE_CONTACTS: granted=true"'
    result = os.popen(test).read()
    if int(result) >= 1:
        print("Gmail can write contacts")
        logging.info('Gmail can write contacts')
        write_contacts.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gmail cannot write contacts")
        logging.error('Gmail cannot write contacts')
        write_contacts.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gmail cannot write contacts')
        write_contacts.appendChild(false_statement)
    gmail.appendChild(write_contacts)
    time.sleep(1)
    os.system('adb shell am force-stop com.google.android.gm')
    time.sleep(1)


def check_gboard():
    print("\nChecking Gboard...")
    gboard = dom_report.createElement('Gboard')
    app.appendChild(gboard)
    preload = dom_report.createElement('Preload')
    # Check Gboard is preloaded
    test = 'adb shell settings get secure default_input_method | grep -c com.google.android.inputmethod'
    result = os.popen(test).read()
    if int(result) == 1:
        print("Gboard is preloaded")
        logging.info('Gboard is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gboard is not preloaded")
        logging.error('Gboard is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gboard is not preloaded')
        preload.appendChild(false_statement)
    gboard.appendChild(preload)
    # Check Gboard is default IME
    default = dom_report.createElement('Default_IME')
    test = 'adb shell ime list -a | grep mId | grep -v -c mId=com.google.android'
    result = os.popen(test).read()
    if int(result) == 0:
        print("Gboard is default IME")
        logging.info('Gboard is default IME')
        default.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Gboard is not default IME")
        logging.error('Gboard is not default IME')
        default.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Gboard is not default IME')
        default.appendChild(false_statement)
    gboard.appendChild(default)


def check_assistant():
    print("\nChecking Google Assistant...")
    assistant = dom_report.createElement('Assistant')
    app.appendChild(assistant)
    uniqueness = dom_report.createElement('Uniqueness')
    test = 'adb shell am start -W -a android.intent.action.VOICE_COMMAND | grep -c ' \
           'com.google.android.googlequicksearchbox '
    result = os.popen(test).read()
    if int(result) == 1:
        print("Google Assistant is the only assistant")
        logging.info('Google Assistant is the only assistant')
        uniqueness.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Google Assistant is not the only assistant")
        logging.error('Google Assistant is not the only assistant')
        uniqueness.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Assistant is not the only assistant')
        uniqueness.appendChild(false_statement)
    assistant.appendChild(uniqueness)
    time.sleep(1)
    os.system('adb shell am force-stop com.google.android.googlequicksearchbox')
    time.sleep(2)


def check_search():
    print("\nChecking Google Search...")
    search = dom_report.createElement('Search')
    app.appendChild(search)
    preload = dom_report.createElement('Preload')
    test = 'adb shell pm list packages -i | grep -c com.google.android.googlequicksearchbox'
    result = os.popen(test).read()
    if int(result) == 1:
        print("Google Search is preloaded")
        logging.info('Google search is preloaded')
        preload.setAttribute("Result", "Pass")
    else:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " Google Search is not preloaded")
        logging.error('Google Search is not preloaded')
        preload.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google Search is not preloaded')
        preload.appendChild(false_statement)
    search.appendChild(preload)
    uniqueness = dom_report.createElement('Uniqueness')
    test = 'adb shell am start -W -a android.intent.action.WEB_SEARCH -e query wikipedia | grep -c ' \
           'com.google.android.googlequicksearchbox '
    result = os.popen(test).read()
    if int(result) == 1:
        print('Google search is the only search engine' + Color.BOLD + Color.RED + " in " + Color.END + "the device")

        logging.info('Google search is the only search engine in the device')
        uniqueness.setAttribute("Result", "Pass")
    else:
        print(
            Color.BOLD + Color.RED + "Error!!!" + Color.END + 'Google search is not the only search engine' + Color.BOLD
            + Color.RED + " in " + Color.END + "the device")
        logging.error('Google search is not the only search engine in the device')
        uniqueness.setAttribute("Result", "Fail")
        false_statement = dom_report.createTextNode('Google search is not the only search engine in the device')
        uniqueness.appendChild(false_statement)
    search.appendChild(uniqueness)
    time.sleep(3)
    os.system('adb shell am force-stop com.google.android.googlequicksearchbox')
    time.sleep(1)


def check_ram():
    print("\nChecking device is 1GM RAM or above...")
    test = "adb shell dumpsys meminfo|grep -m 1 'Total RAM:'|cut -d '(' -f 1|cut -d ':' -f 2|awk '{$1=$1;print}'|tr " \
           "-d ',kBK' "
    result = os.popen(test).read()
    if int(result) < 800000:
        print(Color.BOLD + Color.RED + "Error!!!" + Color.END + " GMS Express Plus Device requires 1GB RAM or above")
        exit(0)
    print(Color.BOLD + Color.RED + Color.UNDERLINE + "\nAssessment start" + Color.END)


def wake_up_device():
    os.system('adb shell input keyevent 224')
    os.system('adb shell input keyevent 82')
    os.system('adb shell input keyevent 03')


def check_app_category():
    global app
    app = dom_report.createElement('App')
    start = datetime.datetime.now()
    check_ram()
    print(Color.BOLD + Color.DARKCYAN + "\n#1 Check APP Category\n" + Color.END)
    try:
        if root.getElementsByTagName('Chrome')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_chrome()
        elif root.getElementsByTagName('Chrome')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Chrome\n")
            logging.error("Wrong configuration for Chrome")
    except AttributeError:
        print("No attribute 'data' for Chrome,please configure the file\n")
        logging.error("No attribute 'data' for Chrome")
    try:
        if root.getElementsByTagName('Gallery')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            os.system("adb shell input keyevent 224")
            check_photo()
        elif root.getElementsByTagName('Gallery')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Gallery\n")
            logging.error('Wrong configuration for Gallery')
    except AttributeError:
        print("No attribute 'data' for Gallery,please configure the file\n")
        logging.error("No attribute 'data' for Gallery")
    try:
        if root.getElementsByTagName('Messaging')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_messages()
        elif root.getElementsByTagName('Messaging')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Messages\n")
            logging.error('Wrong configuration for Messages')
    except AttributeError:
        print("No attribute 'data' for Messages,please configure the file\n")
        logging.error("No attribute 'data' for Messages")
    try:
        if root.getElementsByTagName('Calendar')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_calendar()
        elif root.getElementsByTagName('Calendar')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for for Calendar\n")
            logging.error('Wrong configuration for Calendar')
    except AttributeError:
        print("No attribute 'data' for Calendar,please configure the file\n")
        logging.error("No attribute 'data' for Calendar")
    try:
        if root.getElementsByTagName('Email')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_gmail()
        elif root.getElementsByTagName('Email')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Email\n")
            logging.error('Wrong configuration for Email')
    except AttributeError:
        print("No attribute 'data' for Email,please configure the file\n")
        logging.error("No attribute 'data' for Email")
    try:
        if root.getElementsByTagName('Keyboard')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_gboard()
        elif root.getElementsByTagName('Keyboard')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Keyboard\n")
            logging.error('Wrong configuration for Keyboard')
    except AttributeError:
        print("No attribute 'data' for Keyboard,please configure the file\n")
        logging.error("No attribute 'data' for Keyboard")
    try:
        if root.getElementsByTagName('Voice_assistant')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_assistant()
        elif root.getElementsByTagName('Voice_assistant')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Voice_assistant\n")
            logging.error('Wrong configuration for Voice_assistant')
    except AttributeError:
        print("No attribute 'data' for voice assistant ,please configure the file\n")
        logging.error("No attribute 'data' for Voice_assistant")
    try:
        if root.getElementsByTagName('Search')[0].firstChild.data == 'on':
            root_report.appendChild(app)
            check_search()
        elif root.getElementsByTagName('Search')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for for Search\n")
            logging.error('Wrong configuration for Search')
    except AttributeError:
        print("No attribute 'data' for Search ,please configure the file\n")
        logging.error("No attribute 'data' for Search")
    end = datetime.datetime.now()
    process_time = (end - start).microseconds

    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 1 is: " + str(process_time) +
          " ms\n" + Color.END)


def fingerprint_check():
    start = datetime.datetime.now()
    print(Color.BOLD + Color.DARKCYAN + "\n#2 Fingerprint Check\n" + Color.END)
    try:
        if root.getElementsByTagName('Fingerprinter')[0].firstChild.data == 'on':
            fingerprint1 = dom_report.createElement('Fingerprint')
            root_report.appendChild(fingerprint1)
            legality = dom_report.createElement('Uniqueness')
            fingerprint1.appendChild(legality)
            # Check fingerprint Check
            fingerprint = os.popen('adb shell getprop ro.build.fingerprint').read().strip()
            fingerprint_log = os.popen('adb shell getprop | grep ro.build.fingerprint').read().strip()
            print('Fingerprint : ' + fingerprint)
            logging.info(fingerprint_log)
            # Get brand
            brand = os.popen('adb shell getprop ro.product.brand').read().strip()
            # Get product name
            product_name = os.popen('adb shell getprop ro.product.name').read().strip()
            # Get product device
            product_device = os.popen('adb shell getprop ro.product.device').read().strip()
            # Get build version release
            build_version_release = os.popen('adb shell getprop ro.build.version.release ').read().strip()
            # Get build id
            build_id = os.popen('adb shell getprop ro.build.id').read().strip()
            # Get build version incremental value
            build_version = os.popen('adb shell getprop ro.build.version.incremental').read().strip()
            # Get build type
            build_type = os.popen('adb shell getprop ro.build.type').read().strip()
            # Get build tags
            build_tags = os.popen('adb shell getprop ro.build.tags').read().strip()
            # compare
            print('\nStart comparing...\n')
            new_fingerprint = brand + '/' + product_name + '/' + product_device + ':' + build_version_release + '/' + build_id + '/' + build_version + ':' + build_type + '/' + build_tags
            if fingerprint == new_fingerprint:
                print(Color.BOLD + Color.GREEN + 'Fingerprint matched\n' + Color.END)
                print(Color.BOLD + Color.BLUE + 'Fingerprint is LEGAL' + Color.END)
                logging.info('Fingerprint matched')
                legality.setAttribute("Result", "Pass")
            else:
                print(Color.BOLD + Color.RED + Color.UNDERLINE + 'Fingerprint Unmatched!!!' + Color.END)
                print(Color.BOLD + Color.BLUE + 'Fingerprint is ILLEGAL' + Color.END)

                logging.critical('Fingerprint Unmatched')
                legality.setAttribute("Result", "Fail")
                false_statement = dom_report.createTextNode('GFingerprint is ILLEGAL')
                legality.appendChild(false_statement)

        elif root.getElementsByTagName('Fingerprinter')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Fingerprinter")
            logging.error('Wrong configuration for Fingerprinter')

    except AttributeError:
        print("No attribute 'data' for Fingerprinter ,please configure the file")
        logging.error("No attribute 'data' for Fingerprinter")

    end = datetime.datetime.now()
    process_time = (end - start).microseconds
    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 2 is: " + str(process_time) +
          " ms\n" + Color.END)


def relevant_version_check():
    start = datetime.datetime.now()
    print(Color.BOLD + Color.DARKCYAN + "\n#3 Relevant Version Check\n" + Color.END)
    try:
        if root.getElementsByTagName('Relevant_version_check')[0].firstChild.data == 'on':
            version_check = dom_report.createElement('Relevant_Version_Check')
            root_report.appendChild(version_check)
            gms_version1 = dom_report.createElement('GMS_VERSION')
            security_patch1 = dom_report.createElement('SECURITY_PATCH')
            first_api_level1 = dom_report.createElement('FIRST_API_LEVEL')
            version_check.appendChild(gms_version1)
            version_check.appendChild(security_patch1)
            version_check.appendChild(first_api_level1)
            # GMS version
            gms_version = os.popen('adb shell getprop ro.com.google.gmsversion').read()
            gms_version_log = os.popen('adb shell getprop | grep ro.com.google.gmsversion').read().strip()
            print('GMS version: ' + gms_version)
            version = dom_report.createTextNode(gms_version.strip())
            gms_version1.appendChild(version)
            logging.info(gms_version_log)
            # Security Patch version
            security_patch = os.popen('adb shell getprop ro.build.version.security_patch').read()
            security_patch_log = os.popen('adb shell getprop | grep ro.build.version.security_patch').read().strip()
            print('Security patch: ' + security_patch)
            version = dom_report.createTextNode(security_patch.strip())
            security_patch1.appendChild(version)
            logging.info(security_patch_log)
            # Check first_api_level
            first_api_level = os.popen('adb shell getprop ro.product.first_api_level').read()
            first_api_level_log = os.popen('adb shell getprop | grep ro.product.first_api_level').read().strip()
            print('first_api_level: ' + first_api_level)
            version = dom_report.createTextNode(first_api_level.strip())
            first_api_level1.appendChild(version)
            logging.info(first_api_level_log)
        elif root.getElementsByTagName('Relevant_version_check')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for Relevant version check")
            logging.error('Wrong configuration for Relevant_version_check')
    except AttributeError:
        print("No attribute 'data' for Relevant version Check,please configure the file\n")
        logging.error("No attribute 'data' for Relevant_version_check")
    end = datetime.datetime.now()
    process_time = (end - start).microseconds
    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 3 is: " + str(process_time) +
          " ms\n" + Color.END)


def check_targetSdkVersion():
    start = datetime.datetime.now()
    print(Color.BOLD + Color.DARKCYAN + "\n#5 Sdk Version Check\n" + Color.END)
    try:
        if root.getElementsByTagName('SDK_version_check')[0].firstChild.data == 'on':
            sdk_version = dom_report.createElement('Sdk_Version_Check')
            root_report.appendChild(sdk_version)
            sett = dom_report.createElement('Version_Value')
            sdk_version.appendChild(sett)
            # open the file
            print('Fetching data...\n')
            os.system('adb shell dumpsys package | grep -n -E "^|targetSdk">targetSdk_all.txt')
            version_value = []
            str_lookup = 'targetSdk='
            filename = 'targetSdk_all.txt'
            # obtain the line included targetSdk value
            with open(filename, 'r') as fp:
                for line in fp:
                    if str_lookup in line:
                        version_value.append(int(line.strip().split("targetSdk=")[1]))
            print('Checking value...\n')
            # check each value
            for value in version_value:
                if value < 28:
                    print(Color.BOLD + Color.RED + "Sdk Version Check Done. Fail!!!" + Color.END)
                    logging.critical('Sdk Version Check Failed')
                    sett.setAttribute("Result", "Fail")
                    false_statement = dom_report.createTextNode(
                        'Sdk Version Check Failed Due to Value Less than 28 Exists')
                    sett.appendChild(false_statement)
                    fp.close()
                    os.system('rm targetSdk_all.txt')
                    end = datetime.datetime.now()
                    process_time = (end - start).microseconds
                    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 5 is: " + str(process_time) +
                          " ms\n" + Color.END)
                    return
            print(Color.BOLD + Color.GREEN + "Sdk Version Check Passed" + Color.END)
            logging.info('Sdk Version Check Passed')
            sett.setAttribute("Result", "Pass")
            fp.close()
            os.system('rm targetSdk_all.txt')
        elif root.getElementsByTagName('SDK_version_check')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for SDK_version_check")
            logging.error('Wrong configuration for SDK_version_check')
    except AttributeError:
        print("No attribute 'data' for SDK version check,please configure the file\n")
        logging.error("No attribute 'data' for SDK_version_check")
    end = datetime.datetime.now()
    process_time = (end - start).microseconds
    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 5 is: " + str(process_time) +
          " ms\n" + Color.END)


def camera_notch_check():
    start = datetime.datetime.now()
    print(Color.BOLD + Color.DARKCYAN + "\n#4 Camera notch Check\n" + Color.END)
    try:
        if root.getElementsByTagName('notch_check')[0].firstChild.data == 'on':
            notch_check = dom_report.createElement('Camera_Notch_Check')
            root_report.appendChild(notch_check)
            notch = os.popen('adb shell "pm list features | grep camera_notch"').read()
            if notch == "":
                print("Camera notch is not set")
                logging.critical("Camera notch is not set")
                notch_check.setAttribute("Result", "Fail")
                false_statement = dom_report.createTextNode('Camera notch is not set')
                notch_check.appendChild(false_statement)
            else:
                print('camera notch is set')
                logging.info('camera notch is set')
                notch_check.setAttribute("Result", "Pass")
        elif root.getElementsByTagName('notch_check')[0].firstChild.data == 'off':
            pass
        else:
            print("Please correct the configuration for notch_check")
            logging.error('Wrong configuration for notch_check')
    except AttributeError:
        print("No attribute 'data' for notch_check ,please configure the file\n")
        logging.error("No attribute 'data' for notch_check")
    end = datetime.datetime.now()
    process_time = (end - start).microseconds
    print(Color.BOLD + Color.PURPLE + "\nTotal testing time for part 4 is: " + str(process_time) +
          " ms\n" + Color.END)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='TestResult_' + os.popen(
        "adb shell getprop | grep ro.build.product | awk -F ':' '{print$2}' | tr -d '[]'").read() + ".log",
                        filemode='w', format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(''message)s')
    try:
        print('Fetching data from config file...')
        dom = xml.dom.minidom.parse("config.xml")
    except IOError:
        print('Config File Not Found or Wrong Filename')
        logging.critical('Config File Not Found or Wrong Filename')
        exit(1)
    root = dom.documentElement
    impl = xml.dom.minidom.getDOMImplementation()
    dom_report = impl.createDocument(None, 'GMS_CHECK_REPORT', None)
    root_report = dom_report.documentElement
    wake_up_device()
    check_app_category()
    fingerprint_check()
    relevant_version_check()
    camera_notch_check()
    check_targetSdkVersion()
    f = open('Report_' + os.popen(
        "adb shell getprop | grep ro.build.product | awk -F ':' '{print$2}' | tr -d '[]'").read() + ".xml", 'w')
    dom_report.writexml(f, addindent='  ', newl='\n')
    f.close()
    print(Color.BOLD + Color.CYAN + '\n\nGMS Check Finished' + Color.END)
