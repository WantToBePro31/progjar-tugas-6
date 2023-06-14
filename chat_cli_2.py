import socket
import json
import base64
import os

class ChatClient:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (ip, port)
        self.sock.connect(self.server_address)
        self.token_id = ""

    def proses(self, cmdline):
        j = cmdline.split(" ")
        try:
            command = j[0].strip()
            ## AUTH ##
            if (command == 'auth'):
                username= j[1].strip()
                password= j[2].strip()
                return self.login_user(username, password)
            elif (command == 'register'):
                username = j[1].strip()
                password = j[2].strip()
                name = j[3].strip()
                country = "Indonesia" if len(j) != 5 else j[4].strip()
                return self.register_user(username, password, name, country)
            elif (command == 'logout'):
                return self.logout_user()
            
            ## INTERNAL SERVER ##
            # PRIVATE
            elif (command == 'sendprivate'):
                receiver = j[1].strip()
                message = ""
                for w in  j[2:]:
                    message="{} {}" . format(message, w)
                return self.send_private_message(receiver, message)
            
            # GROUP
            elif (command == 'sendgroup'):
                group_receiver = j[1].strip()
                message = ""
                for w in  j[2:]:
                    message="{} {}" . format(message, w)
                return self.send_group_message(group_receiver, message)
            
            #INBOX
            elif (command == 'inbox'):
                return self.inbox()            
            
            
            ## EXTERNAL SERVER ##
            # INITIALIZE
            elif (command == 'addrealm'):
                realm_id = j[1].strip()
                realm_address_to = j[2].strip()
                realm_port_to = j[3].strip()
                return self.add_realm(realm_id, realm_address_to, realm_port_to)
                
            # PRIVATE
            elif (command == 'sendprivaterealm'):
                realm_id = j[1].strip()
                receiver = j[2].strip()
                message = ""
                for w in  j[3:]:
                    message = "{} {}".format(message, w)
                return self.send_private_message_realm(realm_id, receiver, message)
            
            # GROUP
            elif (command == 'sendgrouprealm'):
                realm_id = j[1].strip()
                group_receiver = j[2].strip()
                message=""
                for w in  j[3:]:
                    message="{} {}" . format(message, w)
                return self.send_group_message_realm(realm_id, group_receiver,message)

            # INBOX
            elif (command == 'inboxrealm'):
                realm_id = j[1].strip()
                return self.inbox_realm(realm_id)
            
            
            ### INFO ## 
            elif (command == 'logininfo'):
                return self.login_info()
            else:
                return "*Maaf, command tidak benar"
        except IndexError:
            return "-Maaf, command tidak benar"


    ## UTIL ##
    def sendstring(self,string):
        try:
            self.sock.sendall(string.encode())
            msg = ""
            while True:
                data = self.sock.recv(1024)
                print("diterima dari server",data)
                if (data):
                    msg = "{}{}" . format(msg,data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
                    if msg[-4:]=='\r\n\r\n':
                        print("end of string")
                        return json.loads(msg)
        except:
            self.sock.close()
            return { 'status' : 'ERROR', 'message' : 'Gagal'}

    def login_info(self):
        string = "logininfo \r\n"
        result = self.sendstring(string)
        if result['status'] == 'filled':
            return "login user: {}" . format(result['message'])
        else:
            return "tidak ada user yang login"


    ## AUTH ##
    def login_user(self, username, password):
        string = "auth {} {} \r\n" . format(username, password)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.token_id = result['token_id']
            self.username = username
            return "username {} berhasil masuk, token {}" . format(username, self.token_id)
        else:
            return "Error, {}" . format(result['message'])
    
    def register_user(self, username, password, name, country):
        string = "register {} {} {} {} \r\n" . format(username, password, name, country)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "username {} berhasil terdaftar" . format(username)
        else:
            return "Error, {}" . format(result['message'])

    def logout_user(self):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "logout {} \r\n" . format(self.token_id)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            self.token_id = ""
            return "user berhasil keluar"
        else:
            return "Error, {}" . format(result['message'])


    ## INTERNAL SERVER ##
    # PRIVATE
    def send_private_message(self, receiver="xxx", message="xxx"):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "sendprivate {} {} {} \r\n" . format(self.token_id, receiver, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "pesan berhasil dikirim ke {}" . format(receiver)
        else:
            return "Error, {}" . format(result['message'])

    # GROUP
    def send_group_message(self, group_receiver="xxx",message="xxx"):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "sendgroup {} {} {} \r\n" . format(self.token_id, group_receiver, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "pesan berhasil dikirim ke grup {}" . format(group_receiver)
        else:
            return "Error, {}" . format(result['message'])
    
    # INBOX
    def inbox(self):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "inbox {} \r\n" . format(self.token_id)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{}" . format(json.dumps(result['messages']))
        else:
            return "Error, {}" . format(result['message'])
    
    
    ## EXTERNAL SERVER ##
    # INITIALIZE
    def add_realm(self, realm_id, realm_address_to, realm_port_to):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "addrealm {} {} {} \r\n" . format(realm_id, realm_address_to, realm_port_to)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "realm {} berhasil dibuat" . format(realm_id)
        else:
            return "Error, {}" . format(result['message'])
        
    # PRIVATE
    def send_private_message_realm(self, realm_id, receiver, message):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "sendprivaterealm {} {} {} {} \r\n" . format(self.token_id, realm_id, receiver, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "pesan berhasil dikirim ke {} di realm {}" . format(receiver, realm_id)
        else:
            return "Error, {}" . format(result['message'])
        
    # GROUP
    def send_group_message_realm(self, realm_id, group_receiver, message):
        if self.token_id == "":
            return "Error, not authorized"
        
        string = "sendgrouprealm {} {} {} {} \r\n" . format(self.token_id, realm_id, group_receiver, message)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "pesan berhasil dikirim ke grup {} di realm {}" . format(group_receiver, realm_id)
        else:
            return "Error {}" . format(result['message'])

    # INBOX
    def inbox_realm(self, realm_id):
        if (self.token_id == ""):
            return "Error, not authorized"
        
        string = "inboxrealm {} {} \r\n" . format(self.token_id, realm_id)
        result = self.sendstring(string)
        if result['status'] == 'OK':
            return "{} di realm {}" . format(result['messages'], realm_id)
        else:
            return "Error, {}".format(result['message'])
    

if __name__=="__main__":
    cc = ChatClient("172.16.16.102", 8889)
    while True:
        cmdline = input("Command {}:" . format(cc.token_id))
        print(cc.proses(cmdline))