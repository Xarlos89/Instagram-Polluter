
import secret # usernames and passwords
import menus # pretty menus
import utilities # Big funcs
import os
import sys
import selenium
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC



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
    menu['3'] = "\033[0;33mUnfollow other accounts\033[m"
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
            confirm = input('\n - WARNING -\nThis action cannot be undone. \
                Proceed with caution.\nAre you sure you wish to delete all \
                Instagram pictures for {}?  (y or n): '.format(secret.username))
            if confirm.lower() == 'y' and confirm.isalpha() == True:
                deletePictures()
            else: 
                menu()
        elif selection == '3':
            os.system('clear')
            # Unfollow()
            print('Still working on that feature :-)')

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
        sleep(1)
        button_login.click()
    def handleStayLoggedIn(): ######### Click away the 'stay logged in' prompt
        try:
            WebDriverWait(webdriver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')))
            print("\033[0;33m               \033[m Clicking away 'Stay logged in' prompt...\033[m ")
            sleep(2)
            notnow = webdriver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/div/button')
            notnow.click()
            sleep(2)
        except:
            print('Oops, missed the Stay logged in box.')
    def handleNotifications(): ######### Click away the 'allow notifications' prompt
        try:
            WebDriverWait(webdriver, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]')))
            print("\033[0;33m               \033[m Clicking away notification prompt...\033[m ")
            sleep(2)
            notifications = webdriver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]')
            notifications.click()
            sleep(2)
        except:
            print('Oops, missed the Notifications box.')


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
    counter = 1
    while True:
        try:
            webdriver.get('https://www.instagram.com/' + secret.username)
            # Click first image
            sleep(3)
            WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]'))).click()
            sleep(1)
            # Click '3 dots' to get the options dropdown
            WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[1]/div/div/button'))).click()
            sleep(1)
            # Click Delete
            WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div/button[1]'))).click()
            sleep(1)
            # Confirm the deletion
            WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]/button[1]'))).click()
            counter += 1
        except NoSuchElementException:
            print('Congratulations. {} Photos have been removed.'.format(str(counter)))
            confirm = input('\nPress any key to continue...')
            return False

def Unfollow():
    print('Beginning unfollow process.')
    counter = 1
    webdriver.get('https://www.instagram.com/' + secret.username)
    sleep(2)

    # Click button to load followers modal
    WebDriverWait(webdriver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/div/span'))).click()
    sleep(3)

    # We need to load the profile list, so this scrolls 20 times. 
    # We should not unfollow more than 200 per day, or else we get blocked.
    # So no need to load more today.
    print("Loading profiles to unfollow.")
    for i in range(0,20):
        element = webdriver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[3]')
        webdriver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', element)
        sleep(1)
    counter = 1
    while True:
        try:

    ##### ToDO #### 
    # finish this. Cannot find the "unfollow button"
    # Add # of people user wishes to unfollow.  
            WebDriverWait(webdriver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div[3]/ul/div/li[1]/div/div[3]/button/div'))).click()
            counter += 1
            sleep(1)
        except:
            print("You unfollowed {} people today.".format(counter))



if __name__ == "__main__":
    menus.prettyIntro()
    Login()
    Menu()

