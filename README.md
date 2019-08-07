# 1. App for Experimental Protocol on Git
Application for tutorial experiments with oTree

1. Download Gitbash for giving the command line instructions and follow custom configurations within the Gitbash app terminal
```
https://gitforwindows.org/
git --config --global user.email "sarah_joseph@live.com"
git --config --global user.name "Sarah"
```

2. Get remote branch to local directory:
```
git clone https://github.com/SJ-SCM/oTree-Decision-Experiments
```
3. Make the changes locally, and navigate to otree-decision-experiments in GitBash and give command
```
git init
```
(3.1) This code is only needed during the first setup, otherwise skip to the next lines
```
git remote add origin https://github.com/SJ-SCM/oTree-Decision-Experiments
```
4. Finally commit and push back all changes to the remote branch:
```
git add .
git commit . -m "change description"
git push origin master
```
5. If you are not up to date with the branch here then you can either pull the repository from here or:
```
git pull
git push -f origin master
```


# 2. App for Experimental Protocol with oTree

**A. For testing:**

1. Navigate in the windows command prompt to the folder with the settings.py file
2. Deploy locally with:
```
otree devserver
```
3. go to localhost:8000 in the browser

**B. For deploying in a local area network:**

B.1 Configure firewall

1. Open the Windows Firewall
2. Go to “Inbound Rules”
3. Click “New Rule”
4. Select “Port” to make a port rule
5. Under “Specific local ports”, enter 80 and 8000
6. Select “Allow the connection”
7. Click “next” then choose a name for your rule (e.g. “oTree”).

B.2 Get the machine IP by entering the following in the windows command terminal
```
ipconfig
```
The IPV4 address is the one you will need, it may will look something like 10.0.1.3, or could also start with 172 or 192.

B.3 Deploy the server from a local network:
In the browser you can start the server with your IP address and port 8000, e.g. otree devserver 10.0.1.3:8000

B.4 Allocation of participant:
The session wide link allocates participants, they cannot access via the IP and port URL address
