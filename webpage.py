import time
from pyvirtualdisplay import Display
from datetime import datetime, timedelta, date
from selenium import webdriver
import random
import os
import platform
from sendmail import send
import jsonconfig

home = os.path.expanduser("~")
crontab = False  # If use crontab or ssh, change to True, need to setup some stuff if required

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
elif platform.system() == "Windows":
    if platform.machine() == "AMD64":
        path = home + "/AppData/Roaming/Mozilla/Firefox/Profiles/"
        geckoPath += "/geckodriver_win64.exe"
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

# Why I put it ?
pList.reverse()
dList.reverse()

# Setup
timeout = 7
logPath = pathlib + '/query.txt'
if not os.path.isfile(logPath) or date.today() > date.fromtimestamp(os.path.getmtime(logPath)):
    logfile = open(logPath, 'w')
else:
    logfile = open(logPath, 'a')
android = "Mozilla/5.0 (Linux; Android 6.0.1; SM-G928F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.85 Mobile Safari/537.36"
edge = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"

proFile = pathlib + '/profile.json'
profileData = jsonconfig.readjson(proFile)


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


# bing.com
# driver.find_element_by_id("id_n").text
# Quyen
# driver.find_element_by_class_name("id_link_text").text
# 'Sign out'
progressStr = str()


def auto_bing(pbrowser, search_times, nbrowser):
    for p in range(len(pList)):
        if pList[p] not in profileData:
            profileData[pList[p]] = {'isSend': 0, 'name': str(pList[p]),
                                     'datetime': jsonconfig.toStrtime(datetime.now())}
            jsonconfig.writejson(proFile, profileData)
        user = profileData[pList[p]]['name']
        alist = shuffle_list(search_times)
        if crontab:
            display = Display(visible=0, size=(400, 300))
            display.start()
        profile = webdriver.FirefoxProfile(dList[p])
        profile.set_preference("general.useragent.override", pbrowser)
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=geckoPath)
        driver.implicitly_wait(90)
        # driver.get("https://account.microsoft.com/rewards/dashboard")
        # time.sleep(2)
        # name = driver.find_element_by_id("id_n").text
        # name = driver.find_element_by_class_name("msame_Header_name").text
        for i in range(len(alist)):
            strtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            driver.get("http://bing.com/search?q=" + alist[i])
            time.sleep(random.randint(10, 15))
            # user = driver.find_element_by_id("id_n").text
            # if user != profileData[pList[p]]['name']:
            #     profileData[pList[p]]['name'] = user
            #     jsonconfig.writejson(proFile, profileData)
            if check_point(driver, nbrowser, user, pList[p]):
                break
            print([i + 1], strtime, nbrowser, "for", user, "in profile", pList[p],
                  progressStr, "Searching:", alist[i], file=logfile)
        driver.quit()


# use this method to open firefox with specific profile to manually do questions
def open_firefox(k):
    print("List of profiles in FireFox:")
    for i in range(len(pList)):
        print([i + 1], pList[i])
    p = input("Which profiles you want to run? ")
    profile = webdriver.FirefoxProfile(dList[int(p) - 1])
    profile.set_preference("general.useragent.override", edge)
    driver = webdriver.Firefox(firefox_profile=profile, executable_path=geckoPath)
    driver.implicitly_wait(90)
    # driver.get("http://bing.com/")
    # name = driver.find_element_by_id("id_n").text
    # print(name)
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
    if k == 1:
        driver.quit()


# check if do enough point in a day
def check_point(driver, nbrowser, user, profile):
    global progressStr
    if nbrowser == "Edge":
        i = 1
    else:
        i = 2
    driver.get("http://bing.com/rewardsapp/bepflyoutpage?style=modular")
    progress = driver.find_elements_by_class_name("progress")[i].text
    bonus = driver.find_elements_by_class_name("progress")[0].text

    # click daily point
    #
    dailypoint_click = driver.find_elements_by_class_name("progress")[3]
    dailypoint_click2 = driver.find_elements_by_class_name("progress")[4]
    dailypoint = dailypoint_click.text.split(' ')
    dailypoint2 = dailypoint_click2.text.split(' ')
    if int(dailypoint[2]) == 10 or int(dailypoint[2]) == 5:
        dailypoint_click.click()
    elif int(dailypoint[2]) == 30:
        # send mail
        if jsonconfig.toDatetime(profileData[profile]["datetime"]) \
                + timedelta(hours=23) + timedelta(minutes=50) < datetime.now():
            profileData[profile]["isSend"] = 0
            profileData[profile]["datetime"] = jsonconfig.toStrtime(datetime.now())
            jsonconfig.writejson(proFile, profileData)

        if profileData[profile]["isSend"] == 0:
            profileData[profile]["isSend"] = 1
            jsonconfig.writejson(proFile, profileData)
            send(user, "Please do bing questions before " + jsonconfig.toStrtime(datetime.now() + timedelta(days=1)))

        if int(dailypoint2[2]) == 10 or int(dailypoint2[2]) == 5:
            dailypoint_click2.click()
    #########################
    progressStr = progress
    progress = progress.split('/')
    bonus = bonus.split('/')
    if int(progress[0]) < int(progress[1]) or (int(bonus[0]) + 30) < int(bonus[1]):
        return False
    return True


# test if setting work
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


# open_firefox(0)
auto_bing(edge, 35, "Edge")
auto_bing(android, 25, "Android")
# test()
logfile.close()
