# BITWISER: Reverse Engineering:

## Introduction:
This challenge is a Reverse Engineering challenge, and from its name, we get the intuition that it involoves bit manipulation.

## First Execution:
The first time we open the program, it writes the following:
```
░▒▓█ 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕥𝕠 𝕄𝕦𝕝𝕥𝕚𝕡𝕝𝕚𝕔𝕒𝕥𝕚𝕧𝕖 𝕔𝕙𝕒𝕝𝕝𝕖𝕟𝕘𝕖 █▓▒░
░▒▓█ 𝔾𝕚𝕧𝕖 𝕞𝕖 𝕥𝕙𝕖 𝕞𝕒𝕘𝕚𝕔 𝕟𝕦𝕞𝕓𝕖𝕣: 
```
... and it askes for a `magic number`.

## Static code analysis:
Using Ghidra, we can examine our program.

### The Main function:
After opening the program, and analysing it, we find the next code for the main function:

```
void main(void)

{
  ulong local_10;
  
  puts(&DAT_00102008);
  printf(&DAT_001020a8);
  fflush(stdout);
  __isoc99_scanf(&DAT_0010210c,&local_10);
  if (((-local_10 & local_10) == local_10) && ((long)local_10 >> 0x32 == 1)) {
    puts(&DAT_00102110);
    printFlag("flag.txt");
    fflush(stdout);
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  printf(&DAT_00102180);
  fflush(stdout);
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

... so we find that our program only uses one variable, and also uses `puts` and `printf` to write into our screen, from the first execution, we know that the two functions are just to print what should we enter.
and then it uses `scanf` to read the magic number, and puts it in the variable `local_10`.

The next part is where our program tests our number:

 - The first test: `(-local_10 & local_10) == local_10`
 - The second test: `(long)local_10 >> 0x32 == 1`

If we analyse the second test, we find that our program is casting our number as a `long` and then shifting it to the left by `0x32` times, which means `50` in decimal, and tests if the result is `1`.

From this, we can make our number, so we know it should end with `1`, followed by 64 `0`.

A one line python code can give it:

```
>>> int("1"+"0"*50, 2)
1125899906842624
```

So the magic number is `1125899906842624`.
Giving it to our progrum returns:
```
★彡 ℂ𝕠𝕟𝕘𝕣𝕒𝕥𝕦𝕝𝕒𝕥𝕚𝕠𝕟𝕤. 𝕪𝕠𝕦 𝕨𝕠𝕟 彡★
```

So it is correct.

## Getting the flag:
Opening a connection to `rev.ingehack.ingeniums.club 5000` with `nc` and entring the magic number give us the following flag:
```
IngeHack{17_d032n7_M4773r_1F_J00_BR0K3_17_0r_50LV3d_17_4LL_7h472_M4773R_12_j00_907_17}
```