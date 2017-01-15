import time
from pyvirtualdisplay import Display
from datetime import datetime
from selenium import webdriver
import random
import os
import platform
from os.path import expanduser

home = expanduser("~")
crontab = False  # If use crontab or ssh, change to True

# Before run this program. Please follow the instruction
# First, create profile SELENIUM
#       MAC: Type in terminal     /Applications/Firefox.app/Contents/MacOS/firefox -P
#       LINUX: Type in terminal    firefox -P
# Second, select that profile and login your account in Bing with keeping sign in option
# Third, run this program
# PS: run test() first to make sure it work
pathlib = os.path.dirname(__file__) if os.path.dirname(__file__) != "" else os.getcwd()
geckoPath = pathlib + "/driver"
path = str()
if platform.system() == "Darwin":
    path = home + "/Library/Application Support/Firefox/Profiles/"
    geckoPath += "/geckodriver_mac"
elif platform.system() == "Linux":
    path = home + "/.mozilla/firefox/"
    if platform.machine() == "x86_64":
        geckoPath += "/geckodriver_linux64"
    elif platform.machine() == "armv7l":
        geckoPath += "/geckodriver_arm7"
    else:
        print("Not support your processor")
        exit(0)
else:
    print("Not support your system")
    exit(0)

# print(geckoPath)

dirs = os.listdir(path)
found = False
dList = []
pList = []
folder = str()
for file in dirs:
    if len(file.split(".")) != 2:
        continue
    # print(os.path.abspath(file))
    p = file.split(".")[1]
    if p[:8] == "SELENIUM" and p != "SELENIUMTEST":
        found = True
        folder = path + file
        dList.append(folder)
        pList.append(p)

if not found or not os.path.isdir(folder):
    print("You didn't setup your Firefox profile SELENIUM")
    exit(0)

pList.reverse()
dList.reverse()
# Setup
timeout = 7
logfile = open('myfile.txt', 'a')
android = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G928F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36"
edge = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"


def get_random_words_file(times):
    # read file
    file = pathlib + '/words.txt'
    with open(file) as f:
        alist = random.sample(f.readlines(), times)  # get random words from file
    alist = [line.rstrip() for line in alist]  # strip \n
    return alist


# Shuffle each element of a list
def shuffle_list(times):
    alist = get_random_words_file(times)
    r = get_random_words_file(4)
    for i in r:
        alist = [i + ' ' + a for a in alist]
    # shuffle words in element of list
    for word in alist:
        word_split = word.split(" ")
        random.shuffle(word_split)
        word_split = ' '.join(word_split)
        alist[alist.index(word)] = word_split
    return alist


# driver.get("http://bing.com/rewardsapp/bepflyoutpage?style=modular")
# driver.find_element_by_id("credits").find_elements_by_class_name("details")[1].find_element_by_class_name("progress").text
# 150/150
# driver.find_element_by_id("credits").find_elements_by_class_name("details")[2].find_element_by_class_name("progress").text
# 100/100

# bing.com
# driver.find_element_by_id("id_n").text
# Quyen
# driver.find_element_by_class_name("id_link_text").text
# 'Sign out'
progressStr = str()


def auto_bing(pbrowser, search_times, nbrowser):
    for p in range(len(pList)):
        alist = shuffle_list(search_times)
        if crontab:
            display = Display(visible=0, size=(400, 300))
            display.start()
        profile = webdriver.FirefoxProfile(dList[p])
        profile.set_preference("general.useragent.override", pbrowser)
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=geckoPath)
        driver.implicitly_wait(30)
        # driver.get("https://account.microsoft.com/rewards/dashboard")
        # time.sleep(2)
        # name = driver.find_element_by_id("id_n").text
        # name = driver.find_element_by_class_name("msame_Header_name").text
        for i in range(len(alist)):
            if check_point(driver, nbrowser):
                break
            strtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            driver.get("http://bing.com/search?q=" + alist[i])
            time.sleep(random.randint(10, 15))
            print([i + 1], strtime, nbrowser, "in profile", pList[p], progressStr, "Searching:", alist[i],
                  file=logfile)
        driver.quit()


def open_firefox():
    print("List of profiles in FireFox:")
    for i in range(len(pList)):
        print([i + 1], pList[i])
    p = input("Which profiles you want to run? ")
    profile = webdriver.FirefoxProfile(dList[int(p) - 1])
    profile.set_preference("general.useragent.override", edge)
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=geckoPath)
    driver.implicitly_wait(30)
    # driver.get("http://bing.com/")
    driver.get("http://bing.com/rewardsapp/bepflyoutpage?style=modular")
    progress = driver.find_elements_by_class_name("progress")
    for i in progress:
        print(i.text)
        #     if driver.current_url != "http://bing.com/rewardsapp/bepflyoutpage?style=modular":
        #         driver.get("http://bing.com/rewardsapp/bepflyoutpage?style=modular")
        #
        #     if len(i.text.split(" ")) != 4:
        #         continue
        #     e = i.text.split(" ")
        #     if e[2] == '10':
        #         i.click()
        # driver.quit()


def check_point(driver, nbrowser):
    global progressStr
    if nbrowser == "Edge":
        i = 1
    else:
        i = 2
    driver.get("http://bing.com/rewardsapp/bepflyoutpage?style=modular")
    progress = driver.find_elements_by_class_name("progress")[i].text

    # click daily point
    #
    dailypoint_click = driver.find_elements_by_class_name("progress")[3]
    dailypoint = dailypoint_click.text.split(' ')
    if int(dailypoint[2]) == 10:
        dailypoint_click.click()
    #########################
    progressStr = progress
    progress = progress.split('/')
    if int(progress[0]) < int(progress[1]):
        return False
    return True


def test():
    if crontab:
        display = Display(visible=0, size=(400, 300))
        display.start()
    profile = webdriver.FirefoxProfile(folder)
    profile.set_preference("general.useragent.override", edge)
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=geckoPath)
    driver.get("http://bing.com/")
    time.sleep(5)
    # driver.find_element_by_class_name().find_element_by_class_name()
    # for element in driver.find_element_by_id('id_rc'):
    # print(driver.find_element_by_id('id_rc').get_attribute('element'))
    # print(driver.find_element_by_id('id_rc').get_attribute('text'))
    # print(driver.find_element_by_id('id_rh'))

    # driver.get("http://www.whatsmybrowser.org")
    # time.sleep(10)
    print("Success")
    driver.quit()


# print(shuffle_list(30))
# check_point()
# print(shuffle_list(4))
# print(folder)

# print(pList)
# print(dList)
# open_firefox()
auto_bing(edge, 30, "Edge")
auto_bing(android, 20, "Android")
# test()
logfile.close()
