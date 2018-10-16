# Special Challenge Solution (HC 0x0e) from [The Morpheus Tutorials](https://the-morpheus.de)

### 1. System nach Interesannten Dateien durchsuchen.
Nachdem man durch die file inclusion Shell Access auf das System hat, findet man im Ordner `/var/backups` die Datei `shadow.bak` mit dem Inhalt:
```
...
user:$1$a7H2Sh$FtnHGImcOSwZH33L9ZeaK.:17790:0:99999:7:::
```

Außerdem finden wir in die Datei `/tmp/need_help_?.txt` mit dem Inhalt:
```
Special Challenge: TMT{user_password}
```

### 2. Knacken des Passwords mit Hashcat
Aufbau des Hashes verstehen ($ verfahren $ salt $ password)  
In der Helppage den benötigten Mode (**1**) finden: 500
```
$ hashcat -h
...
 500 | md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)        | Operating Systems
3200 | bcrypt $2*$, Blowfish (Unix)                     | Operating Systems
7400 | sha256crypt $5$, SHA256 (Unix)                   | Operating Systems
1800 | sha512crypt $6$, SHA512 (Unix)                   | Operating Systems
 122 | macOS v10.4, MacOS v10.5, MacOS v10.6            | Operating Systems
...
```
```
$ echo '$1$a7H2Sh$FtnHGImcOSwZH33L9ZeaK' > 0x0e.hash
$ hashcat -m 500 -a 0 0x0e.hash rockyou.txt
hashcat (v4.1.0) starting...

* Device #1: WARNING! Kernel exec timeout is not disabled.
             This may cause "CL_OUT_OF_RESOURCES" or related errors.
             To disable the timeout, see: https://hashcat.net/q/timeoutpatch
OpenCL Platform #1: NVIDIA Corporation
======================================
* Device #1: GeForce GTX 1060 3GB, 751/3005 MB allocatable, 9MCU

...

Dictionary cache hit:
* Filename..: /opt/wordlists/rockyou.txt
* Passwords.: 14344384
* Bytes.....: 139921497
* Keyspace..: 14344384

$1$a7H2Sh$FtnHGImcOSwZH33L9ZeaK.:golf1346798520  

Session..........: hashcat
Status...........: Cracked
Hash.Type........: md5crypt, MD5 (Unix), Cisco-IOS $1$ (MD5)
Hash.Target......: $1$a7H2Sh$FtnHGImcOSwZH33L9ZeaK.
Time.Started.....: Sun Sep 16 13:18:46 2018 (6 secs)
Time.Estimated...: Sun Sep 16 13:18:52 2018 (0 secs)
Guess.Base.......: File (/opt/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.Dev.#1.....:  1261.1 kH/s (13.27ms) @ Accel:256 Loops:250 Thr:32 Vec:1
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 7888896/14344384 (55.00%)
Rejected.........: 0/7888896 (0.00%)
Restore.Point....: 7815168/14344384 (54.48%)
Candidates.#1....: goooo3 -> gianavie
HWMon.Dev.#1.....: Temp: 46c Fan: 58% Util: 81% Core:1860MHz Mem:3802MHz Bus:16
```
Das Passwort lautet also `golf1346798520`. Somit lautet die Flag für die  Special Challenge: `TMT{golf1346798520}`
