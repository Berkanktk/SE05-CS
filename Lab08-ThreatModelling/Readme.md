# Exercises
## Exercise 8.1: A simple Data Flow Diagram
Read the ACME case in “Literature” on itslearning. In groups of ≈ 3, develop a data flow diagram for 
* An android health-app
* Login using username & password 
* The app will be used to manually enter and edit/add/delete, e.g., height, weight, activity, and diet data. 
* Data is stored locally 

Make assumptions as needed, e.g., mobile platform, native framework, . . . 

**Answers**
* Single-factor is not sufficient
* Encryption challenges
* Platform specific vulnerabilities
* Insecure client-side data storage 

![First version](/Lab08-ThreatModelling/Diagrams/FirstVersion.png)

## Exercise 8.2: Formulate Stride 
For the Android App, formulate
* Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege
* For each category describe threats
* Use the ACME case & the game cards as a guide

Answers
| Threat | Violated property | Threat description |
|:---:|:---:|:---:|
| Spoofing | Authentication | Using user authentication to access sensitive medical data.  |
| Tampering | Integrity | Attackers can modify the application source code for malicious purposes, including sending confidential data outside the intended datastore. Code-signing of the application can help the user authenticate the app’s integrity. |
| Repudiation | Non-repudiation | Users data changes are not properly logged, thus permitting malicious manipulation. |
| Information disclosure | Confidentiality | It’s a local datastore. The confidentiality relies mostly on the device’s security, including hardware and software security. Data-at-rest encryption for instance. |
| Denial of Service | Availability | Attacker DDoS’ing the login server  |
| Elevation of privilege | Authorization | Attackers exploit a weakness in the app to gain elevated privileges in order to manipulate the mobile system. |

## Exercise 8.3: Discuss your Data Flow Diagram & STRIDE 
**Discuss exercises 8.1 & 8.2, ideally with another group. Try to complete your diagram &STRIDE.**  
Done

**† Please include your flow diagram with a description of the essential parts; provide list or table which details your findings using STRIDE.**   
See 8.1 and 8.3

## Exercise 8.4: Update Flow Diagram & STRIDE 
Update the data flow diagram & STRIDE for the case that the app becomes more of a fitness tracker
* Collect data from third party devices, e.g., via Bluetooth
* Data includes fitness-related metrics, e.g., steps taken, miles, calories burnt, activities, sleeping times
* The app cleans data and performs necessary computations
* No modification of data by users
* Data is stored on-device and in a cloud

![Second version](/Lab08-ThreatModelling/Diagrams/SecondVersion.png)

**† Please include your updated flow diagram with a description of the essential parts; provide list or table which details your findings using STRIDE.**  
|    <br>Threat    | Violated property    | Threat description    |
|---|---|---|
| Spoofing | Authentication | Using user authentication to access sensitive   medical data. <br>   <br>Possible MITM attacks<br>   <br>Brute force attacks<br>   <br>Phishing attacks (human)    |
| Tampering | Integrity | Attackers can modify the application source code for malicious purposes, including sending confidential data outside the intended datastore.<br>   <br>Code-signing of the application can help the user authenticate the app’s integrity.    |
| Repudiation    | Non-repudiation    | Users' data changes are not properly logged, thus permitting malicious manipulation. |
| Information disclosure  | Confidentiality | It’s a local datastore. The confidentiality relies mostly on the device’s security, including hardware and software security.   Data-at-rest encryption for instance.<br><br>Sniffing, eavesdropping clear text<br>   <br>Improper encryption |
| Denial of Service | Availability | Attacker DDoS’ing the login server or the cloud server<br>   <br>Jamming sensor signals. |
| Elevation   of privilege    | Authorization    | Attackers exploit a weakness in the app to gain   elevated privileges in order to manipulate the mobile/cloud system.    |
