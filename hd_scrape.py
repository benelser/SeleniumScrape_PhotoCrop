from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common import keys
import urllib.request
import sys
import time
from getpass import getpass
import ssl
import os
import re
import requests
import json
from subprocess import Popen, PIPE, STDOUT
import shutil
import apt
import datetime
import argparse


browser_options = webdriver.FirefoxOptions()
browser_options.add_argument('-headless')
browser = webdriver.Firefox(options=browser_options)
#browser = webdriver.Firefox(proxy=proxy, options=browser_options)

def Check_for_bad_sku(sku):
    badskus = open("/Tools/badskus.txt", 'r')
    bad_dict = {}
    count = 1
    for s in badskus:
        bad_dict[count] = s.split("\n")[0]
        count += 1
    if sku.split("\n")[0] in bad_dict.values():
        print(f"{sku} is a bad sku...Moving on")
        return True
    badskus.close()
    return False

def GetImageUrl(sku):
    time.sleep(2)
    browser.get("https://www.homedepot.com/")
    time.sleep(2)
    value = browser.find_element_by_id("headerSearch")
    value.send_keys(sku)
    button = browser.find_element_by_id("headerSearchButton")
    button.click()
    time.sleep(2)
    badskus = open("/Tools/badskus.txt", 'a')
    try:
         image = browser.find_element_by_id("mainImage")
         return image.get_attribute('src')
    except :
        print(f"Something went wrong trying to grab {sku} image")
        badskus.write(f"{sku}\n")
        badskus.close()
        return False

def download_screenshot(srcurl, sku):
    print(f"Downloading image for {sku}")
    browser.get(srcurl)
    browser.get_screenshot_as_file(f"/Tools/{sku}.png")

f = open("sku.txt", "r")

for sku in f:
    sku = sku.split("\n")[0]
    if Check_for_bad_sku(sku):
        continue
    else:
        if os.path.isfile(f"/Tools/{sku}.png"):
            print(f"{sku} image already downloaded...Moving on")
            continue
        srcurl = GetImageUrl(sku)
        if srcurl != False:
            download_screenshot(srcurl, sku)
