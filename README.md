# Experimental Protocol Application

<br/>
Summary: Open-source application within behavioural decision experiments of K.U.L academic research. <br/>
<br/>
Authorization: The repository is allowed to be used and changed for research within the Euthority group. <br/>
<br/>
Usage: The repository can be referenced via "Nicolas Lampach, Sarah Joseph, Applications of Experimental Protocol, (2019), Repository, https://github.com/SJ-SCM/oTree-Decision-Experiments" <br/>
<br/>
References: <br/>
1. Daniel L. Chen et al., (2016), oTree—An open-source platform for laboratory, online, and field experiments. Journal of Behavioral and Experimental Finance. <br/>
2. Felix Holzmeister, (2018), Repository, https://github.com/JBEF/oTree_MPL <br/>
<br/>

# 1. Installation of Git SCM

1. Download Gitbash for giving the command line instructions and follow custom configurations within the Gitbash app terminal
```
https://gitforwindows.org/
git config --global user.email "email"
git config --global user.name "firstname"
```

2. Get remote branch to local directory:
```
git clone https://github.com/timothy2799/oTree-Decision-Experiments
```
3. Make the changes locally, and navigate to otree-decision-experiments in GitBash and give command
```
git init
```
_(3.1) This command is only needed during the first setup, otherwise skip._
```
git remote add origin https://github.com/timothy2799/oTree-Decision-Experiments
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
<br/>
<br/>

# 2. Installation and Deployment of oTree

<br/>

## **Install the Following**
1. Python
2. pip
3. Microsoft Visual C++
4. oTree

<br/>
## **A. For testing**

1. Navigate in the windows command prompt to the folder with the settings.py file
2. Deploy locally with:
```
otree devserver
```
3. go to localhost:8000 in the browser

<br/>

## **B. For deploying in a local area network**

- [ ] B.1 Configure firewall

1. Open the Windows Firewall
2. Go to “Inbound Rules”
3. Click “New Rule”
4. Select “Port” to make a port rule
5. Under “Specific local ports”, enter 80 and 8000
6. Select “Allow the connection”
7. Click “next” then choose a name for your rule (e.g. “oTree”).

- [ ] B.2 Get the machine IP by entering the following in the windows command terminal
```
ipconfig
```
The IPV4 address is the one you will need, it may will look something like 10.0.1.3, or could also start with 172 or 192.

- [ ] B.3 Deploy the server from a local network:
In the browser you can start the server with your IP address and port 8000, e.g. otree devserver 10.0.1.3:8000

- [ ] B.4 Allocation of participant:
The session wide link allocates participants, they cannot access via the IP and port URL address
