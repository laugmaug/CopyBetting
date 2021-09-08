from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time,os

realPath = os.path.dirname(__file__)
slp = 5

class linkManager:
    def __init__(self):
        #Login Inputs
        self.btnLogin_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/ul/li[1]/a"
        self.loginInput_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[1]/div/div/input"
        self.passwdInput_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[2]/div/div/input"
        self.txtBox_xpath = "//*[@id='bs-example-navbar-collapse-1']/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[3]/div/label"
        self.btnlogin2_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[4]/div[1]/button[1]"
        self.recentBets_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/ul/li[4]/h5/a[1]"
        self.soccer_tab_xpath = "/html/body/app-root/betting-page/div/app-three-column/div/div[1]/div/betting-sports-selector/div/div[3]/div/a[10]"

        #Recent Bets
        self.recentBetsTableBody_xpath = "/html/body/app-root/app-account/div/div/div[2]/div/app-account-recent-bets/div/div/div/div[1]/table/tbody"




class credentialManager:
    def __init__(self):
        self.master_dir = ""
        self.clients_dir = ""

    def credMaster(self):
        with open(realPath + "/master.dat") as f:
            line = f.readline()
            usr, psw = line.split(",")

        return (usr,psw)

    def credClients(self):
        client = []
        with open(realPath + "/clients.dat") as f:
            for line in f.readlines():
                usr, psw = line.split()
        client.append(tuple(usr,psw))

class algorithm:
    def __init__(self):
        self.PATH = ""

        with open(realPath + "/driver_dir.txt") as f:
            self.PATH = f.readline()

        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("https://new.hollywoodbets.net/betting")
        self.linkManager = linkManager()
        
    def login(self, masterLogin, masterPassword):
        #logiin
        btnlogin = self.driver.find_element(By.XPATH, self.linkManager.btnLogin_xpath)
        btnlogin.click()

        #username
        txtLogin = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, self.linkManager.loginInput_xpath)))
        txtLogin.send_keys(masterLogin)

        #password
        txtPassword = self.driver.find_element(By.XPATH, self.linkManager.passwdInput_xpath)
        txtPassword.send_keys(masterPassword)

        #textbox terms & conditions
        txtBox = self.driver.find_element(By.XPATH, self.linkManager.txtBox_xpath)
        txtBox.click()

        #textBox
        btnlogin2 = self.driver.find_element(By.XPATH, self.linkManager.btnlogin2_xpath)
        btnlogin2.click()

        pass

    def getPendingBets(self):
        self.driver.find_element(By.XPATH, self.linkManager.recentBets_xpath).click()
        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.XPATH, self.linkManager.recentBetsTableBody_xpath)))

        for el in element.find_elements(By.TAG_NAME, "tr"):
            el.click()

            slip_table = element.find_elements(By.CLASS_NAME, "transaction-details")
            slip_bets = slip_table.find_element(By.XPATH, "/td[1]/app-transaction-details/div/div/table")


            el.click()
        pass

    def placeBet(self, bet):
        pass
            
        pass

    def placeBets(self, bets, clientLogin, clientPassword):
        pass

    def logout(self):
        pass


main = algorithm()
credentials = credentialManager()

username, passwd = credentials.credMaster()


main.login(username, passwd)

#master login
print("Done")