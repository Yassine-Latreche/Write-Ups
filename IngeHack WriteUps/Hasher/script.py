import subprocess
import os
import hashlib
import re
ALPHABET = """{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_ '-"*/\_+="""
alphabet_hashes = dict()
for i in ALPHABET:
    alphabet_hashes[i] = hashlib.sha256(hashlib.md5( i.encode()).hexdigest().encode()).hexdigest()

flag = """=="""

cpt = 0
while True:
    MyOut = subprocess.Popen(['ltrace', './hasher'], 
            stdout=subprocess.PIPE, 
            stdin=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    stdout_data, stderr = MyOut.communicate(input=bytes(flag[1:1+cpt+1], 'utf-8'))
    last_cmp = [x for x in stdout_data.decode("utf-8").split("\n") if "strcmp(" in x][-1]
    if last_cmp[-1] != "0":
        oldflag = flag
        for j in alphabet_hashes:
            if last_cmp[47:47+32] in alphabet_hashes[j]:
                flag = flag + j
        if flag == oldflag:
            flag = flag + "_"
    else:
        flag = flag + "_"
    if flag[-1] == "}":
        break
    print(flag)
    cpt += 1
print(flag)
