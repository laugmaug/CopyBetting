from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import *
import tkinter as tk
import time
import os

realPath = os.path.dirname(__file__)
slp = 5
window = tk.Tk()


class linkManager:
    def __init__(self):
        # Login Inputs
        self.btnLogin_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/ul/li[1]/a"
        self.loginInput_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[1]/div/div/input"
        self.passwdInput_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[2]/div/div/input"
        self.txtBox_xpath = "//*[@id='bs-example-navbar-collapse-1']/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[3]/div/label"
        self.btnlogin2_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/div/div/div/div[2]/div/form/fieldset/div[4]/div[1]/button[1]"
        self.recentBets_xpath = "/html/body/app-root/header/div/div[2]/app-login/div[1]/ul/li[4]/h5/a[1]"
        self.soccer_tab_xpath = "/html/body/app-root/betting-page/div/app-three-column/div/div[1]/div/betting-sports-selector/div/div[3]/div/a[10]"

        # Recent Bets
        self.recentBetsTableBody_xpath = "/html/body/app-root/app-account/div/div/div[2]/div/app-account-recent-bets/div/div/div/div[1]/table/tbody"

        # My Account
        self.myAcc = "//*[@id='myAccountDropdown']"
        self.btnLogout = "/html/body/bs-dropdown-container/div/ul/li[7]/a"

        # Mobile version
        self.mUsername = '/html/body/form/nav/div[2]/div[1]/div[1]/input'
        self.mPassword = '/html/body/form/nav/div[2]/div[1]/div[2]/input'
        self.TnC = '/html/body/form/nav/div[2]/div[1]/div[1]/div/label/small'
        self.bLogin = '/html/body/form/nav/div[2]/div[1]/div[2]/div/a[2]'
        
        self.SoccerTab = '/html/body/form/main/nav[2]/ul/li[22]/label'

class credentialManager:
    def __init__(self):
        self.master_dir = ""
        self.clients_dir = ""

    def credMaster(self):
        with open(realPath + "/master.dat") as f:
            line = f.readline()
            usr, psw = line.split(",")

        return (usr, psw)

    def credClients(self):
        client = []
        with open(realPath + "/clients.dat") as f:
            for line in f.readlines():
                usr, psw = line.split(',')
                client.append([usr, psw])

        return client

class algorithm:
    def __init__(self):
        self.PATH = ""

        with open(realPath + "/driver_dir.txt") as f:
            self.PATH = f.readline()

        self.driver = webdriver.Chrome(self.PATH)
        
        self.driver.get("https://new.hollywoodbets.net/?__cf_chl_captcha_tk__=pmd_5nWdc0A3aQVIwNdr3aSuxSrJgjcBUtm2Hr9T9QKfORA-1632636841-0-gqNtZGzNArujcnBszQ09")
        self.linkManager = linkManager()

    #Master & Client login [START]
    def login(self, masterLogin, masterPassword):
        # logiin
        btnlogin = self.driver.find_element(
            By.XPATH, self.linkManager.btnLogin_xpath)
        btnlogin.click()

        # username
        txtLogin = WebDriverWait(self.driver, 30).until(
            ec.visibility_of_element_located((By.XPATH, self.linkManager.loginInput_xpath)))
        txtLogin.send_keys(masterLogin)

        # password
        txtPassword = self.driver.find_element(
            By.XPATH, self.linkManager.passwdInput_xpath)
        txtPassword.send_keys(masterPassword)

        # textbox terms & conditions
        txtBox = self.driver.find_element(
            By.XPATH, self.linkManager.txtBox_xpath)
        txtBox.click()

        # textBox
        btnlogin2 = self.driver.find_element(
            By.XPATH, self.linkManager.btnlogin2_xpath)
        btnlogin2.click()

        pass

    def clientLogin(self, cLogin, cPasswd):
        cPasswd = cPasswd.strip("\n")

        try:
            self.driver.find_element(By.XPATH, '//*[@id="ctl00_HeadLoginView_HeadLoginStatus"]').click()
        except:
            self.driver.get("https://m.hollywoodbets.net/")

        # username
        txtLogin = WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((By.XPATH, self.linkManager.mUsername)))
        txtLogin.send_keys(cLogin)

        time.sleep(1)

        # password
        txtPassword = self.driver.find_element(
            By.XPATH, self.linkManager.mPassword)
        txtPassword.send_keys(cPasswd)

        time.sleep(1)

        # textbox terms & conditions
        btnlogin2 = self.driver.find_element(
            By.XPATH, self.linkManager.TnC)
        btnlogin2.click()

        time.sleep(1)

        # Button Login
        btnLogin = self.driver.find_element(
            By.XPATH, self.linkManager.bLogin)
        btnLogin.click()
    #Master & Client login [END]

    #####################################################################################
    #Collect data from master account [Start]
    def getPendingBets(self, ticket_No):
        bets = []
        # navigate to bets table
        try:
            WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, self.linkManager.recentBets_xpath))).click()
        except:
            WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                (By.XPATH, self.linkManager.recentBets_xpath))).click()

        element = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(
            (By.XPATH, self.linkManager.recentBetsTableBody_xpath)))

        #Bet slips [table rows]
        for el in element.find_elements(By.TAG_NAME, "tr"):
            el.click()

            slip_table = WebDriverWait(element, 30).until(
                ec.visibility_of_element_located((By.CLASS_NAME, "transaction-details")))

            #[table columns]
            for row in slip_table.find_elements(By.TAG_NAME, "tr"):
                if row.get_attribute("class") == "p-20 bg-warning":
                    continue
                
                elif "Paid Out" in el.find_elements(By.TAG_NAME, "td")[7].text or "Losing" in el.find_elements(By.TAG_NAME, "td")[7].text:
                    continue

                elif ticket_No not in el.find_elements(By.TAG_NAME, "td")[2].text:
                    continue

                else:
                    ticket_No = el.find_elements(By.TAG_NAME, "td")[1].text
                    stake = el.find_elements(By.TAG_NAME, "td")[4].text

                    arrRow = [ticket_No, stake]
                    row_meta = []

                    for cell in row.find_elements(By.TAG_NAME, "td"):
                        row_meta.append(cell.text)

                    arrRow.append(row_meta)
                    bets.append(arrRow)

            el.click()
        return bets
    #Collect data from master account [End]

    def stakeCompare(self, stake):
        intStake = float(stake)
        bal = self.driver.find_element(By.XPATH, '//*[@id="lblBal"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", bal)
        inBal = float(bal.text.strip("R "))

        if intStake > inBal:
            return str(int(inBal))
        
        return str(int(intStake))

    #Login to client & place master's bets [Start]
    def placeBets(self, bets, clientLogin, clientPassword, stake):
        prevTicket = ""
        
        self.clientLogin(clientLogin, clientPassword)

        #For each and every ticket
        for bet in bets:
            ticket_no, stake, betDetails = bet
            stake = stake

            try:
                stake = self.stakeCompare(stake)
            except:
                time.sleep(1)
                self.placeBets(bets,clientLogin, clientPassword, stake)

            self.driver.get("https://m.hollywoodbets.net/Menu/Betting/SportNew.aspx#Countries?sportId=1&sportName=Soccer")

            if ticket_no != prevTicket and not(prevTicket == ""):
                self.submitTicket(stake)
                
            if ticket_no != prevTicket:
                print(clientLogin, ticket_no, stake)

            # Navigate to countries of soccer leagues
            

            self.driver.maximize_window()

            country, league = betDetails[2].split(" - ")
            leg = betDetails[0]
            EventDate = betDetails[1]
            event = betDetails[3]

            l =  betDetails[4].split(" - ")

            if len(l) == 3:
                mType, Market = (l[0] + " - " + l[1]), (l[2])
            else:
                mType, Market = l[0], l[1]
            
            status = betDetails[6]

            try:
                Countryparent = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                    (By.XPATH, "/html/body/form/main/div[1]/div[3]/div[2]/div[3]/ul")))
            except:
                self.driver.get("https://m.hollywoodbets.net/Menu/Betting/SportNew.aspx#Countries?sportId=1&sportName=Soccer")
                Countryparent = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                    (By.XPATH, "/html/body/form/main/div[1]/div[3]/div[2]/div[3]/ul")))


            for _country in Countryparent.find_elements(By.TAG_NAME, "li"):
                self.driver.execute_script("arguments[0].scrollIntoView();", _country)
                if country in _country.text:
                    time.sleep(0.5)
                    _country.find_elements(By.TAG_NAME, "div")[0].click()
                    leagueParent = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                        (By.XPATH, "/html/body/form/main/div[1]/div[3]/div[3]/div[3]/ul")))
                    for _tournament in leagueParent.find_elements(By.TAG_NAME, "li"):
                        if league in _tournament.text:
                            self.driver.execute_script("arguments[0].scrollIntoView();", _tournament)
                            _tournament.click()
                            matchesParent = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                                (By.XPATH, '/html/body/form/main/div/div/div/div/div[3]/table/tbody')))

                            for row in matchesParent.find_elements(By.TAG_NAME, "tr"):
                                if event in row.text:
                                    self.driver.execute_script("arguments[0].scrollIntoView();", row)
                                    row.find_elements(By.TAG_NAME, "a")[0].click()
                                    
                                    try:
                                        betTypeContainer = self.driver.find_element(By.XPATH, "/html/body/form/main/div[1]/div[3]/div[6]/div[2]/ul")
                                    except:
                                        self.driver.refresh()
                                        time.sleep(1)
                                        betTypeContainer = self.driver.find_element(By.XPATH, "/html/body/form/main/div[1]/div[3]/div[6]/div[2]/ul")

                                    betTypes = betTypeContainer.find_elements(By.TAG_NAME, "li")
                                    for betType in betTypes:
                                        if mType in betType.text:
                                            self.driver.execute_script("arguments[0].scrollIntoView();", betType)
                                            betType.click()
                                            markets = WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
                                            (By.XPATH, "/html/body/form/main/div[1]/div[3]/div[7]/div[4]/ul")))

                                            for market in markets.find_elements(By.TAG_NAME, "li"):
                                                if Market in market.text:
                                                    market.click()
                                                    
                                                    AddToBetslip = self.driver.find_element(By.XPATH, '//*[@id="btnAddToBetSlipMatchPlay"]')
                                                    AddToBetslip.click()
                                                    break
                                    break
                            break
                    break
            
            prevTicket = ticket_no
        self.submitTicket(stake)
        return
    #login to client & place master's bets [END]

    def submitTicket(self, stake):
        #redirect to main soccer page
        self.driver.get("https://m.hollywoodbets.net/Menu/Betting/SportNew.aspx#Countries?sportId=1&sportName=Soccer")

        #Submit BetSlip
        self.driver.find_element(By.XPATH, '//*[@id="mainBetSlipBtn"]').click()

        multiBetInput = self.driver.find_element(By.XPATH, '//input[@id="inputStake"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", multiBetInput)
        time.sleep(2)
        self.driver.execute_script("arguments[0].scrollIntoView();", multiBetInput)
        multiBetInput.clear()
        multiBetInput.send_keys(stake)

        btnBetSubmit = self.driver.find_element(By.XPATH, '//*[@id="btnMultiple"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", btnBetSubmit)
        btnBetSubmit.click()

        self.driver.get("https://m.hollywoodbets.net/Menu/Betting/SportNew.aspx#Countries?sportId=1&sportName=Soccer")

        logout = self.driver.find_element(By.XPATH, '//*[@id="ctl00_HeadLoginView_HeadLoginStatus"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", logout)
        logout.click()

    #Master & Client Logout [START]
    def clientLogout(self):
        btnLogout = self.driver.find_element(By.XPATH, "/html/body/form/nav/div/div/div[2]/a[2]")
        time.sleep(1)
        self.driver.execute_script("arguments[0].scrollIntoView();", btnLogout)
        btnLogout.click()

    def logout(self):
        self.driver.find_element(By.XPATH, self.linkManager.myAcc).click()
        WebDriverWait(self.driver, 30).until(ec.visibility_of_element_located(
            (By.XPATH, self.linkManager.btnLogout))).click()
        pass
    #Master & Client Logout [END]

######################################################################
###################### Program Start #################################
######################################################################
def startBetting(self):
    #start copy bet algorithm
    ticket_No = ""
    try:
        ticket_No = simpledialog.askstring("Ticket_Number", "Enter Ticket Number:", parent=window)
        stake = simpledialog.askstring("Stake_Amount", "Clients' Bet Stake:", parent=window)
        
        main = algorithm()
        credentials = credentialManager()
    except Exception as e:
        messagebox.showerror("Failed to start Copy-Bet-Algorithm", e.message)

    #login into master account & collect bets
    try:
        username, passwd = credentials.credMaster()
        main.login(username, passwd)
        bets = main.getPendingBets(ticket_No)
    except Exception as e:
        messagebox.showerror("Failed to login to/collect master account bets", e.message)

    #logout of master account
    try:
        main.logout()
    except Exception as e:
        messagebox.showerror("Log out of the master account", e.message)

    #login and bet per client
    for client in credentials.credClients():
        cLog, cPsw = client
        main.placeBets(bets, cLog, cPsw, stake)

    main.driver.quit()

    # master login
    messagebox.showinfo("Success", "Successfully done")
######################################################################
####################### Program End ##################################
######################################################################
def editMasterDetails(self):
    try:
        os.system("notepad " + realPath + "/master.dat")
    except:
        os.system("gedit " + realPath + "/master.dat")

def editClientDetails(self):
    try:
        os.system("notepad " + realPath + "/clients.dat")
    except:
        os.system("gedit " + realPath + "/clients.dat")

#window initiated @ top
window.geometry("400x200")

intro = tk.Label(text="Soccer Betting Automation")
intro.pack()

btnHolder = tk.Frame(window)

editMaster = tk.Button(btnHolder, text="Edit Master's details")
editMaster.pack()

editClients = tk.Button(btnHolder, text="Edit Client details")
editClients.pack()

btnStartCopyBet = tk.Button(btnHolder, text="Start Copy Betting")
btnStartCopyBet.pack()

btnHolder.pack(side = BOTTOM)

editMaster.bind("<Button-1>", editMasterDetails)
editClients.bind("<Button-1>", editClientDetails)
btnStartCopyBet.bind("<Button-1>", startBetting)

window.mainloop()

#print(realPath)
