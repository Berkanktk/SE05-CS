# Exercises

This essentially calls for monitoring of your system and includes different types of
information. Examples are:
* an inventory of your network: which machines are part of it, how is the traffic flow,
e.g., scanning with arpwatch, using network authentication with 802.1X, etc.;
* an inventory of your services: which services are running, which ports are open,
e.g., scanning with nmap, nessus, or gvm, etc.;
* an inventory of traffic in your network, e.g., controlling & logging traffic with
firewalls, or (Network) Intrusion Detection Systems.

All of these activities include the collection of specific information, which is worthless, if
the collected information is not analysed and not acted upon. Automating the analysis
with Intrusion Detection Systems (IDS), and potentially with Intrusion Protection
Systems (IPS) for rule based initiation of defence mechanisms, is therefore a corenerstone
of good operation.

# Preparations
Please install the following tools in preparation of today’s exercise:

```console
berkankutuk@kali:~$ apt install postfix bsd-mailx logcheck sshguard suricata
```

When asked for the role of your postfix mail server, please answer “local only”.

# Logcheck
Logcheck is simple tool for sorting the relevance of messages: what can be
ignored, what needs to be warned about. It does the by filtering log messages via regular
expressions and sending the remaining information out via e-mail. This should ideally
happen periodically, e.g., via cron jobs or systemd.

Edit `/etc/logcheck/logcheck.conf`. Check the REPORTLEVEL setting and change SENDMAILTO
to root.

```console
berkankutuk@kali:~$ sudo nano /etc/logcheck/logcheck.conf
...
# Controls the address mail goes to:
# *NOTE* the script does not set a default value for this variable!
# Should be set to an offsite "emailaddress@some.domain.tld"

SENDMAILTO="root"
...
```


```console
berkankutuk@kali:~$ sudo systemctl start postfix
berkankutuk@kali:~$ sudo systemctl enable postfix
berkankutuk@kali:~$ sudo systemctl start ssh
berkankutuk@kali:~$ sudo -u logcheck logcheck -m root
berkankutuk@kali:~$ mail
```

Then check your mail with the mail tool:
```console
berkankutuk@kali:~$ mail
```

Now perform a set of ssh logins, and check again:
```console
berkankutuk@kali:~$ ssh kali@localhost
berkankutuk@kali:~$ sudo -u logcheck logcheck -m root
berkankutuk@kali:~$ mail
```

**Which information does logcheck provide?**  

**Why do we need a mail service?**

**Is the tool helpful?**  

**How can you improve the rules? Check man regex and look into, e.g., `/etc/logcheck/ignore.d.server/ssh.`**  

**Which dangers do you see with the application of logcheck?**  

# Extended Firewall-Logging
You might think that this should be the exercise’s part one, but think about it. :-)
Check the logs continuously with

```console
berkankutuk@kali:~$ tail -f /var/log/syslog
````

Now perform a standard scan nmap -sT localhost

**What can you observe in the logs?**  
3 entries
```
Dec  9 11:40:27 kali postfix/smtpd[272220]: connect from unknown[unknown]
Dec  9 11:40:27 kali postfix/smtpd[272220]: lost connection after CONNECT from unknown[unknown]
Dec  9 11:40:27 kali postfix/smtpd[272220]: disconnect from unknown[unknown] commands=0/0
```

**And what will happen, if you increase the scanner’s stealth by using a SYN scan?**  
Nothing new shows up

**What is the issue here?**  
That no entries is shown when using a stealth scan

[x] **Remark: make sure that postfix is running before trying to answer these questions.**  

Let’s increase the log level by issuing the following commands:  
iptables -I INPUT -j LOG  
iptables -I FORWARD -j LOG  
iptables -I OUTPUT -j LOG  

> THE REST IS SKIPPED

# Service Protection with sshguard
sshguard extends beyond passive log checking to acting on logs. A similar tool is, e.g.,
fail2ban, but supposedly simpler and more lightweight.

Staying with the example of somebody brute-forcing our ssh server, sshguard can be
used to detect and block an ongoing attack, interfacing with the firewall. It therewith
forms a very simple working example for an Intrusion Prevention System, blocking a
port scan early on.

sshguard plugs between your logs and your firewall. sshguard supports different ways of
attaching to your system logs, allowing to be used with many different logging services,
understanding more than just ssh messages and furthermore interfacing with many
different firewall systems
 
Enable the sshguard service: `systemctl start sshguard`  
Monitor the sshguard logs with: `journalctl -fu sshguard`

For a more comprehensive view of logs, showing ssh as well as sshguard logs, you can
also:  
`tail -f /var/log/auth.log` or `journalctl -f -u sshguard -u ssh`

Now try to connect via ssh with wrong user names and/or password. For this test, you do
not need to perform a high-performance brute-force attack with hydra, just failing to log
in manually will be sufficient. Important is that you do not connect to localhost/127.0.0.1,
as that address is whitelisted and will not provide any relevant change in behaviour.

**Which behaviour is sshguard/the system showing?**

**What happens when several attacks are detected?**  

**Check the configuration in \*/etc/shguard/sshguard.conf+: Configuration options include whitelists, time outs and thresholds, i.e., how many attacks over which time frame are required to constitue an attack?**  

**What are the caveats for this kind of protective service with the parameters available?**  

**How does sshguard block incoming traffic? Use nft list ruleset to observe changes to the nftables Linux firewall configuration. Can you read the output?**  

# Suricata
The tools presented until now are rather simple-minded. And while very helpful with
small machines, they do not offer the possibility to perfom proper analysis of network
traffic.

With suricata, we will look at a system that does exactly that: it uses network capture to
find out what is really going on in a network. This goes beyond log coverage at firewall
level, that will typically collect information that passes a network boundary on a gateway
or router.

Suricata furthermore has the option to be a building block in a larger tool chain, an
Security Information and Event Management, which goes far beyond a simple intrusion
detection system and might use suricata to provide information about security relevant
events, together with other sources of information, for example from your firewalls.

> THE REST IS SKIPPED

# First test case
The configuration as created will provide logging to, amongst other interfaces,
`/var/log/suricata/fast.log`, which we will monitor during our first test:

Monitor suricata operation    
`tail -f /var/log/suricata/fast.log`

Test mode run in another terminal  
`curl http://testmynids.org/uid/index.html`

**What is testmyndis.org?**  

**What does this test cover?**  

**Why would we want a NIDS to react to this test?**  

# A simple rule for detecting pings
If you have a possibility to connect to your kali VM from another machine, then you can
use this test do pick up on local network activity.

Create a file /etc/suricata/rules/local.rules with the following contents:

```
alert icmp any any -> any any (msg:"ICMP ping detected"; sid:1; rev:1;)
```

This rule will alert over icmp packages irrespective of source and destination end points,
warning with the specified message.

We now add our own rule file to suricata.yaml in the rule-files section as
rule-files
`/etc/suricata/rules/local.rules`

Then we restart suricata with `systemctl restart suricata` and can perform a ping
over the captured network interfaces.

**Will you be able to pick up on a host-local ping?**

# How to use suricata’s output?
You will have noticed that all alerts result in log file entries, either as plain text entries
in fast.log, or as json records in eve.json. Of course, we could set up logcheck to also
investigate our suricata output, but this seems pointless, as suricata is supposed to
provide security relavant output.

So where to go next?

# Outlook: Security Information and Event Management
Essentially, you want to be able to always paint a picture about what is going on,
collecting the information and allowing you to make informed decisions.

Tools like suricata are Network Intrusion Detection Systems (NIDSs), analysing network
traffic in life systems or from recorded traffic. For a more complete impression, you
will want to include other sources of information and set a system on top of this fused
information landscape.

Essentially, the structured eve.json is ideally suited for consumption by other systems,
for example logstash or jq. Furthermore, suricata can even transmit the logs over the
network.

