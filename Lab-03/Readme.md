# Exercises

In this lab you will perform steps of an assessment:
* Gather Information: e.g., about a company, range of IP addresses, etc.
* Scan IP addresses: e.g., what services are running on the associated IP addresses
* Fingerprinting: e.g., what web servers, accounts, etc.
* Reporting: summarise the gathered intel

# Preconditions: Installed VMs
* [x] Linux Metasploitable3
* [x] Windows Metasploitable3

# Finding information with whois `TODO` 
1. Try to gather information on SDU with whois.
2. Try whois on the \emph{IP address} of www.sdu.dk .
3. †What do you learn about SDU’s network? In the protocol, note the IP
range.
4. Are there other Networking-Services @SDU which you could try?
5. †What is the whois information for nextcloud.sdu.dk ? What do you observe
in comparison to the whois-information you gathered for www.sdu.dk.
6. Important: You can also perform whois on domains, for example sdu.dk,
but -- depending on the implementation -- only on the registered domain, not any hosts in it. But you can use whois on the IP addresses associated
to the hosts.

# Question: nmap
Nmap scans can be set up to evade firewalls. Which tags would you use for:
* †Send packets with specified ip options
  * `--ip-options <options>`
* †Spoof your MAC address
  * `--spoof-mac` 

# Scanning the Metasploitable VMs
Use Nmap, to scan and find out information about Metasploitable-3, both Windows and Ubuntu. 
In your use of Nmap compare your SYN scan vs the Connect scan vs the scan with the tag that enables OS detection, version detection, script scanning.  
Take notes of the results for all three and discuss differences and pros and cons based on your observation.

**Nmap flags**  
Syn scan = `-sS`  
Connect scan = `-sT`    
OS and version detection = `-O -sV`

## Linux
### Syn scan 
```console
berkankutuk@kali:~$ nmap -sS 10.0.2.4 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 00:39 CEST
Nmap scan report for 10.0.2.4
Host is up (0.00069s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE
21/tcp   open   ftp
22/tcp   open   ssh
80/tcp   open   http
445/tcp  open   microsoft-ds
631/tcp  open   ipp
3000/tcp closed ppp
3306/tcp open   mysql
8080/tcp open   http-proxy
8181/tcp closed intermapper
MAC Address: 08:00:27:42:51:79 (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 4.94 seconds
```

### Connect scan
```console
berkankutuk@kali:~$ nmap -sT 10.0.2.4 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 00:46 CEST
Nmap scan report for 10.0.2.4
Host is up (0.0011s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE
21/tcp   open   ftp
22/tcp   open   ssh
80/tcp   open   http
445/tcp  open   microsoft-ds
631/tcp  open   ipp
3000/tcp closed ppp
3306/tcp open   mysql
8080/tcp open   http-proxy
8181/tcp closed intermapper
MAC Address: 08:00:27:42:51:79 (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 4.86 seconds
```

### OS and version detection
```console
berkankutuk@kali:~$ nmap -O -sV 10.0.2.4 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 00:51 CEST
Nmap scan report for 10.0.2.4
Host is up (0.0010s latency).
Not shown: 991 filtered tcp ports (no-response)
PORT     STATE  SERVICE     VERSION
21/tcp   open   ftp         ProFTPD 1.3.5
22/tcp   open   ssh         OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
80/tcp   open   http        Apache httpd 2.4.7 ((Ubuntu))
445/tcp  open   netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
631/tcp  open   ipp         CUPS 1.7
3000/tcp closed ppp
3306/tcp open   mysql       MySQL (unauthorized)
8080/tcp open   http        Jetty 8.1.7.v20120910
8181/tcp closed intermapper
MAC Address: 08:00:27:42:51:79 (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop
Service Info: Host: UBUNTU; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Nmap done: 1 IP address (1 host up) scanned in 12.99 seconds
```

## Windows
### Syn scan 
```console
berkankutuk@kali:~$ nmap -sS 10.0.2.5 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 01:09 CEST
Nmap scan report for 10.0.2.5
Host is up (0.00086s latency).
Not shown: 982 closed tcp ports (reset)
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3306/tcp  open  mysql
3389/tcp  open  ms-wbt-server
4848/tcp  open  appserv-http
7676/tcp  open  imqbrokerd
8080/tcp  open  http-proxy
8181/tcp  open  intermapper
8383/tcp  open  m2mservices
9200/tcp  open  wap-wsp
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
MAC Address: 08:00:27:60:56:1B (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 1.55 seconds
```

### Connect scan
```console
berkankutuk@kali:~$ nmap -sT 10.0.2.5 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 01:07 CEST
Nmap scan report for 10.0.2.5
Host is up (0.0015s latency).
Not shown: 982 closed tcp ports (conn-refused)
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
80/tcp    open  http
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
3306/tcp  open  mysql
3389/tcp  open  ms-wbt-server
4848/tcp  open  appserv-http
7676/tcp  open  imqbrokerd
8080/tcp  open  http-proxy
8181/tcp  open  intermapper
8383/tcp  open  m2mservices
9200/tcp  open  wap-wsp
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
MAC Address: 08:00:27:60:56:1B (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 6.80 seconds
```

### OS and version detection
```console
berkankutuk@kali:~$ nmap -O -sV 10.0.2.5 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-09-26 01:09 CEST
Nmap scan report for 10.0.2.5
Host is up (0.0016s latency).
Not shown: 982 closed tcp ports (reset)
PORT      STATE SERVICE              VERSION
21/tcp    open  ftp                  Microsoft ftpd
22/tcp    open  ssh                  OpenSSH 7.1 (protocol 2.0)
80/tcp    open  http                 Microsoft IIS httpd 7.5
135/tcp   open  msrpc                Microsoft Windows RPC
139/tcp   open  netbios-ssn          Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds         Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3306/tcp  open  mysql                MySQL 5.5.20-log
3389/tcp  open  ms-wbt-server?
4848/tcp  open  ssl/http             Oracle Glassfish Application Server
7676/tcp  open  java-message-service Java Message Service 301
8080/tcp  open  http                 Sun GlassFish Open Source Edition  4.0
8181/tcp  open  ssl/intermapper?
8383/tcp  open  http                 Apache httpd
9200/tcp  open  wap-wsp?
49152/tcp open  msrpc                Microsoft Windows RPC
49153/tcp open  msrpc                Microsoft Windows RPC
49154/tcp open  msrpc                Microsoft Windows RPC
49155/tcp open  msrpc                Microsoft Windows RPC
2 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port8181-TCP:V=7.92%T=SSL%I=7%D=9/26%Time=6330DFD3%P=x86_64-pc-linux-gn
SF:u%r(GetRequest,128C,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sun,\x2025\x20S
SF:ep\x202022\x2023:10:34\x20GMT\r\nContent-Type:\x20text/html\r\nConnecti
SF:on:\x20close\r\nContent-Length:\x204626\r\n\r\n<!DOCTYPE\x20HTML\x20PUB
SF:LIC\x20\"-//W3C//DTD\x20HTML\x204\.01\x20Transitional//EN\">\n<html\x20
SF:lang=\"en\">\n<!--\nDO\x20NOT\x20ALTER\x20OR\x20REMOVE\x20COPYRIGHT\x20
SF:NOTICES\x20OR\x20THIS\x20HEADER\.\n\nCopyright\x20\(c\)\x202010,\x20201
SF:3\x20Oracle\x20and/or\x20its\x20affiliates\.\x20All\x20rights\x20reserv
SF:ed\.\n\nUse\x20is\x20subject\x20to\x20License\x20Terms\n-->\n<head>\n<s
SF:tyle\x20type=\"text/css\">\n\tbody{margin-top:0}\n\tbody,td,p,div,span,
SF:a,ul,ul\x20li,\x20ol,\x20ol\x20li,\x20ol\x20li\x20b,\x20dl,h1,h2,h3,h4,
SF:h5,h6,li\x20{font-family:geneva,helvetica,arial,\"lucida\x20sans\",sans
SF:-serif;\x20font-size:10pt}\n\th1\x20{font-size:18pt}\n\th2\x20{font-siz
SF:e:14pt}\n\th3\x20{font-size:12pt}\n\tcode,kbd,tt,pre\x20{font-family:mo
SF:naco,courier,\"courier\x20new\";\x20font-size:10pt;}\n\tli\x20{padding-
SF:bottom:\x208px}\n\tp\.copy,\x20p\.copy\x20a\x20{font-family:geneva,helv
SF:etica,arial,\"lucida\x20sans\",sans-serif;\x20font-size:8pt}\n\tp\.copy
SF:\x20{text-align:\x20center}\n\ttable\.grey1,tr\.grey1,td\.g")%r(HTTPOpt
SF:ions,7A,"HTTP/1\.1\x20405\x20Method\x20Not\x20Allowed\r\nAllow:\x20GET\
SF:r\nDate:\x20Sun,\x2025\x20Sep\x202022\x2023:10:34\x20GMT\r\nConnection:
SF:\x20close\r\nContent-Length:\x200\r\n\r\n")%r(RTSPRequest,76,"HTTP/1\.1
SF:\x20505\x20HTTP\x20Version\x20Not\x20Supported\r\nDate:\x20Sun,\x2025\x
SF:20Sep\x202022\x2023:10:34\x20GMT\r\nConnection:\x20close\r\nContent-Len
SF:gth:\x200\r\n\r\n");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port9200-TCP:V=7.92%I=7%D=9/26%Time=6330DFC7%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,194,"HTTP/1\.0\x20200\x20OK\r\nContent-Type:\x20application/js
SF:on;\x20charset=UTF-8\r\nContent-Length:\x20317\r\n\r\n{\r\n\x20\x20\"st
SF:atus\"\x20:\x20200,\r\n\x20\x20\"name\"\x20:\x20\"Black\x20Tom\x20Cassi
SF:dy\",\r\n\x20\x20\"version\"\x20:\x20{\r\n\x20\x20\x20\x20\"number\"\x2
SF:0:\x20\"1\.1\.1\",\r\n\x20\x20\x20\x20\"build_hash\"\x20:\x20\"f1585f09
SF:6d3f3985e73456debdc1a0745f512bbc\",\r\n\x20\x20\x20\x20\"build_timestam
SF:p\"\x20:\x20\"2014-04-16T14:27:12Z\",\r\n\x20\x20\x20\x20\"build_snapsh
SF:ot\"\x20:\x20false,\r\n\x20\x20\x20\x20\"lucene_version\"\x20:\x20\"4\.
SF:7\"\r\n\x20\x20},\r\n\x20\x20\"tagline\"\x20:\x20\"You\x20Know,\x20for\
SF:x20Search\"\r\n}\n")%r(HTTPOptions,4F,"HTTP/1\.0\x20200\x20OK\r\nConten
SF:t-Type:\x20text/plain;\x20charset=UTF-8\r\nContent-Length:\x200\r\n\r\n
SF:")%r(RTSPRequest,4F,"HTTP/1\.1\x20200\x20OK\r\nContent-Type:\x20text/pl
SF:ain;\x20charset=UTF-8\r\nContent-Length:\x200\r\n\r\n")%r(FourOhFourReq
SF:uest,A9,"HTTP/1\.0\x20400\x20Bad\x20Request\r\nContent-Type:\x20text/pl
SF:ain;\x20charset=UTF-8\r\nContent-Length:\x2080\r\n\r\nNo\x20handler\x20
SF:found\x20for\x20uri\x20\[/nice%20ports%2C/Tri%6Eity\.txt%2ebak\]\x20and
SF:\x20method\x20\[GET\]")%r(SIPOptions,4F,"HTTP/1\.1\x20200\x20OK\r\nCont
SF:ent-Type:\x20text/plain;\x20charset=UTF-8\r\nContent-Length:\x200\r\n\r
SF:\n");
MAC Address: 08:00:27:60:56:1B (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Microsoft Windows 7|2008|8.1
OS CPE: cpe:/o:microsoft:windows_7::- cpe:/o:microsoft:windows_7::sp1 cpe:/o:microsoft:windows_server_2008::sp1 cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_8 cpe:/o:microsoft:windows_8.1
OS details: Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, Windows Server 2008 R2, Windows 8, or Windows 8.1 Update 1
Network Distance: 1 hop
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows

Nmap done: 1 IP address (1 host up) scanned in 111.78 seconds
```

# Scanning with Legion
