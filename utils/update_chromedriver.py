from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec,wait
from selenium.common.exceptions import SessionNotCreatedException
import argparse
import time
import shutil
import os
import subprocess
import zipfile
import requests,re


def getBrowserVesionLinux():
    proc = subprocess.Popen(
        r'google-chrome --version',
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()    
    version = str(stdout.strip())
    ver = re.search(r"\d+(\.\d+)+", version)    
    finalversion = ver.group()        
    return finalversion


def getChromeDriverVesionLinux(driverpath):
    cmd = driverpath + ' -v'
    proc = subprocess.Popen(
        cmd,
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    version = str(stdout.strip())
    ver = re.search(r"\d+(\.\d+)+", version)  
    finalversion = ver.group()
    return finalversion


def getBrowserVesionWindows():
    proc = subprocess.Popen(
        r'wmic datafile where name="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" get Version /value',
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    version = str(stdout.strip())
    ver = re.search(r"(=.*')", version)
    vers = ver.group()
    last = len(vers)
    finalversion = vers[1:last - 1]    
    return finalversion


def getChromeDriverVesionWindows(driverpath):
    cmd = driverpath + ' -v'
    proc = subprocess.Popen(
        cmd,
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    version = str(stdout.strip())
    finalversion = version.split(" ")        
    return finalversion[1]

def createDriver(exepath,downloaddir):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": downloaddir}
    options.add_experimental_option("prefs", prefs)    
    print("ExE path : ", exepath)
    driver = webdriver.Chrome(executable_path=exepath, options=options)
    return driver


def downloadChromeDriverZip(browserversion,driverdirpath,platform):
    print("Downloading chromedriver zip file...")
    version_to_check = re.search(r"\d+(\.\d+){2}",browserversion).group()
    print("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"+str(version_to_check))
    webresponse = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE_"+str(version_to_check))
    latest_chromedriver_version =  webresponse.text    
    print("Latest chromedriver version available is : " + latest_chromedriver_version)
    if platform=='linux':
        websrc = requests.get("https://chromedriver.storage.googleapis.com/"+str(latest_chromedriver_version)+"/chromedriver_linux64.zip")
    else:
        websrc = requests.get("https://chromedriver.storage.googleapis.com/"+str(latest_chromedriver_version)+"/chromedriver_win32.zip")
    with open(driverdirpath+'//chromedriver.zip', 'wb') as file:
        file.write(websrc.content)

    for file in os.listdir(driverdirpath):
        if file == "chromedriver.zip":            
            zippath = driverdirpath + str("//") + file

    print("zip file path : ", zippath)
    with zipfile.ZipFile(zippath, 'r') as zip_ref:
        zip_ref.extractall(driverdirpath)

    # remove the downloaded zip file
    os.remove(zippath)


def killProcess(platform):
    if platform == 'linux':
        os.system("killall chromedriver")
        os.system("killall chrome")
    else:
        os.system("taskkill /IM chromedriver.exe /f")
        os.system("taskkill /IM chrome.exe /f")


def copyAndRemoveExe(copyfrompath,copytopath):
    time.sleep(10)
    shutil.copy(copyfrompath,copytopath)
    os.remove(copyfrompath)




def main(argv):
    driver_dir_path = os.path.dirname(os.path.abspath(__file__))+'/../webdrivers'
    if argv.platform == 'linux':
        chrome_driver_path = driver_dir_path + "//linux//chromedriver"
    elif argv.platform == 'windows':
        chrome_driver_path = driver_dir_path + "//windows//chromedriver.exe"
    else:
        print("Please enter valid argument......")
        exit(1)
    
     
    try:
        driver = createDriver(chrome_driver_path,driver_dir_path)        
        print("Chrome and Chromedrivers are up to date")
        killProcess(argv.platform)
    except SessionNotCreatedException as e:
        print("Session can't be created : ",e)
        if argv.platform == 'linux':
            print("Updating chromedriver version ...")
            browserversion = getBrowserVesionLinux()
            print("Actual Version of Chrome is: ", browserversion)
            driverversion = getChromeDriverVesionLinux(chrome_driver_path)
            print("Chromedriver Version is: ", driverversion)
            downloadChromeDriverZip(browserversion,driver_dir_path,argv.platform)
            killProcess(argv.platform)
            copyAndRemoveExe(driver_dir_path+"//chromedriver",driver_dir_path + "//linux")
            print("Chromedriver version updated successfully...")
        else:
            print("Updating chromedriver version ...")
            browserversion = getBrowserVesionWindows()
            print("Actual Version of Chrome is: ", browserversion)
            driverversion = getChromeDriverVesionWindows(chrome_driver_path)
            print("Chromedriver Version is: ", driverversion)
            downloadChromeDriverZip(browserversion,driver_dir_path,argv.platform)
            killProcess(argv.platform)
            copyAndRemoveExe(driver_dir_path+"//chromedriver.exe",driver_dir_path + "//windows")
            print("Chromedriver version updated successfully...")

    except Exception as e:
        print("Unable to execute due to error : ", e)
        

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Run Script With Arguments To Download Chromedriver')    
    parser.add_argument('-platform', help='Platform As linux/windows',required=True)
    args = parser.parse_args()
    
    main(args)