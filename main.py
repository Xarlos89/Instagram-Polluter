import os
import sys
import secret # usernames and passwords
import menus # pretty menus
import utilities # Big funcs
from time import sleep
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait 

webdriver = webdriver.Firefox()
pictures = []

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    clear()
    menus.prettyMenu()
    menu = {}
    menu['1'] = "\033[0;33mDownload all pictures from my instagram\033[m"
    menu['2'] = "\033[0;33mDelete all pictures from Instagram\033[m"
    menu['3'] = "\033[0;33mXXXXXXX\033[m"
    menu['4'] = "\033[0;33mExit\033[m"
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, ' ---  ' + menu[entry])

        selection = str(input("\nWhat would you like to do? "))
        if selection == '1':
            os.system('clear')
            menus.prettyPictures()
            downloadPictures()
        elif selection == '2':
            os.system('clear')
            confirm = input('\n - WARNING -\nThis action cannot be undone. Proceed with caution.\nAre you sure you wish to delete all Instagram pictures for {}?  (y or n): '.format(secret.username))
            if confirm.lower() == 'y' and confirm.isalpha() == True:
                deletePictures()
            else: 
                menu()
        elif selection == '3':
            os.system('clear')
            
        elif selection == '4':
            os.system('clear')
            webdriver.close()
            sys.exit()
        else:
            print("\nYou have to choose an option between 1 and 4. \n")
            menu()
                
def Login(): # Handle the whole login process
    def handleCookies(): ######### This accepts the cookies offered by instagram
        WebDriverWait(webdriver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div/button[1]')))
        print("\033[0;33m               \033[m Accepting cookies...\033[m ")
        acceptCookies = webdriver.find_element(By.XPATH, '/html/body/div[4]/div/div/button[1]')
        acceptCookies.click()
        sleep(2)
    def handleLogin(): ######### This uses the form to log into instagram
        WebDriverWait(webdriver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        print("\033[0;33m               \033[m Logging in... \033[m ")
        usernameEntry = webdriver.find_element(By.NAME, 'username')
        usernameEntry.clear()
        usernameEntry.send_keys(secret.username)

        WebDriverWait(webdriver, 20).until(EC.presence_of_element_located((By.NAME, 'password')))
        passwordEntry = webdriver.find_element(By.NAME, 'password');
        passwordEntry.send_keys(secret.password)

        WebDriverWait(webdriver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
        button_login = webdriver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')
        sleep(2)
        button_login.click()
    def handleStayLoggedIn(): ######### Click away the 'stay logged in' prompt
        try:
            WebDriverWait(webdriver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
            print("\033[0;33m               \033[m Clicking away 'Stay logged in' prompt...\033[m ")
            sleep(1)
            notnow = webdriver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')
            notnow.click()
            sleep(2)
        except:
            pass
    def handleNotifications(): ######### Click away the 'allow notifications' prompt
        try:
            WebDriverWait(webdriver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]')))
            print("\033[0;33m               \033[m Clicking away notification prompt...\033[m ")
            sleep(1)
            notifications = webdriver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[3]/button[2]')
            notifications.click()
            sleep(2)
        except:
            pass

    webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    handleCookies()
    handleLogin()
    handleStayLoggedIn()
    handleNotifications()
    menu()

def downloadPictures():
    subfolders = [ f.path for f in os.scandir(os.getcwd()) if f.is_dir() ]
    if secret.username not in str(subfolders): # If your Instagram username is not in the path, warn and break
            print('-WARNING-\nNo data folder detected.\nThis program requires you do download your data from https://www.instagram.com/download/request/\nPlease download the data in HTML format, and place the folder next to the python script.')
            webdriver.get('https://www.instagram.com/download/request/')
            pause = input('\nPress any key to continue...')
            menu()
    else: 
        utilities.grabAllPictures()
        menu()

def deletePictures():
    try:
        webdriver.get('https://www.instagram.com/' + secret.username)
        # Click first image
        WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a/div/div[1]'))).click()
        
        # Click '3 dots' to get the options dropdown
        WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[1]/div/div/button/div/div'))).click()

        # Click Delete
        WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div/div/button[1]'))).click()

        # Confirm the deletion
        WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div/div/div/div[2]/button[1]'))).click()

    except NoSuchElementException:
        print('Congratulations. All photos have been removed.')
        confirm = input('\nPress any key to continue...')
        return False









if __name__ == "__main__":
    menus.prettyIntro()
    Login()
    Menu()

