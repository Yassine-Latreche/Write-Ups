# TWITTER
## Introduction:
This challenge was a misc challenge, titled `Twitter`, and a suspicious quote said by `Nicola Tisla`.
## Deep in the challenge:
Searching for `Nicola Tisla` in twitter, we find this account: [@nicola_tisla](https://twitter.com/nicola_tisla).
The account description says `1337`, which means we are on the right track.
In this acount, we find two tweets:
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">nice tool <a href="https://t.co/WWnI1QeF0i">https://t.co/WWnI1QeF0i</a></p>&mdash; Nicola Tisla (@nicola_tisla) <a href="https://twitter.com/nicola_tisla/status/1399682409449332739?ref_src=twsrc%5Etfw">June 1, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<br>

<blockquote class="twitter-tweet"><p lang="und" dir="ltr"><a href="https://t.co/zznFIheHyI">pic.twitter.com/zznFIheHyI</a></p>&mdash; Nicola Tisla (@nicola_tisla) <a href="https://twitter.com/nicola_tisla/status/1399679573961363459?ref_src=twsrc%5Etfw">June 1, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
<br>

 - The first one is about a tool with its link in github: [tweetable-polyglot-png](https://github.com/DavidBuchanan314/tweetable-polyglot-png)

 - The second one is a picture.

The picture extension was `.png`, so using the given tool on the picture gives us a zip file with same name as the picture.

Trying to unzip the zip file requires us to enter a password, which we don't have.

After brute-forcing the zip file password with `rockyou.txt` password list, we find that the password is `nicole`.

Opening the text file included in the zip file give us the following link: https://nicola-tisla.vercel.app/

Entering the link we find a brand new website made with `Next.js`.

If we take a look into the `robots.txt` file, we find our flag:
```
IngeHack{50M3_5up3R_D33p_53Cr375_1n_7w1773R}
```