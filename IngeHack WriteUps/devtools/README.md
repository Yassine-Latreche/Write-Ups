# devtools:

## Introduction:
This is a web challenge, and from its name, we get the intuition that it's a challenge about one of the frameworks devtool.

## Deep in the challenge:
Opning the `Inspect` tool and reading names of the folders we have, we deduce that it's made with `Next.js`.

And as we know, `Next.js` is like a child of `React.js`, so let's install `React JS Devtools` in our chrome browser.

Reopening the `Inspect` tool and checking under `Components` section, we find a list of components, and in the `_0x186e7e` component, we find the following:
```
{
  "s3cr3t": "SW5nZUhhY2t7dzMzYl9kM3ZfZ3VydX0="
}
```
and decoding the string we found with `base64decoder` we find our flag:
```
IngeHack{w33b_d3v_guru}
```