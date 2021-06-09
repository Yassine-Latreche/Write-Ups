# CATaaS:

## Introduction:
The name of this challenge `CATaaS` giv us the intuition that is about reading files.
## Deep in the challenge:
 and if we read its source code, we notice that:

 - The listning path is `/read_file/{file}`.
 - The code executes a series of tests for our path:
  ```
    try:
        if not os.path.exists(file_path):
            return {"error": "File not found 😅"}
        if not file_path.startswith('/'):
            return {"error": "Not the right way 🥲"}
        if not os.path.isfile(file_path):
            return {"error": "Not a file 😕"}
        if 'ingehack' in file_path:
            return {"error": "No way 🙂"}
        try:
            return FileResponse(file_path)
        except:
            return {"error": "Failed"}
    except:
        return {"error": "Something went wrong"}
```


So our path should have the following criteria:

 - It Should exist.
 - It should be absolute.
 - It should be a path of a file.
 - It shouldn't contain the word : `ingehack`

 > Reading the `docker-compose.yaml` file, we know that the flag is in the `app` directory, and it's path is : `/home/ingehack/app`.

The forth test forces us to not use the path `/home/ingehack/app/flag.txt/`, so we must find another way to go to that path.

As we know, in Linux, each process has its own directory in the `/proc` folder, so one way to access the `app` directory is to go to `/proc/{pid}/cwd/`, so let's try `/proc/self/cwd/flag.txt`:
```
http://misc-chall.ingehack.ingeniums.club:6003/read_file//proc/self/cwd/flag.txt
```
And we get the flag:
```
IngeHack{175_alwAY5_g00D_70_Kn0W_50M3_l1Nux_7r1cX}
```