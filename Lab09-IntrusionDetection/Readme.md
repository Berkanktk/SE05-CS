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


# Extended Firewall-Logging


# Service Protection with sshguard


# Suricata


# First test case


# A simple rule for detecting pings


# How to use suricata’s output?


# Outlook: Security Information and Event Management


