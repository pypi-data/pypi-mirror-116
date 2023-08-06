# NTP Project

## About 

In this project, we created a NTP Project and use Golang(Go) for NTP Server side and Python for NTP Client side. 

This Project Client connect to the Server with Host and Port informations and get date and time from Server.

Also Client computer can sets the Date/Time from NTP Server date/time.

## Build-With

### Server
* GOLANG (Go)

### Client
* Python

## Installitation

### Clone repo 

    git clone https://github.com/yvsKaan/ntpserver.git

## Run 

* You need to start server side first.

        go run server.go

* When your server working, you can start your client.

        python ntpclient.py

    * You need to enter host and port values.
        
        * You can use Localhost HOST : 127.0.0.1 PORT : 1234
        * Or you can change the server host and port address from server.go file 
          
          You Can See Your Ntp Servers 
          
                ss -tulpn | grep ":123"
    
    * Also you can enter your host and port value from console. 

            python ntpclient.py --host HOST_ADDRESS --port PORT_ADDRESS 

    * After That You need to enter your command and system will response.
        ##### Command Examples
        
        * time => Get the Server Time and Date
        
        * exit => Close the NTP Client