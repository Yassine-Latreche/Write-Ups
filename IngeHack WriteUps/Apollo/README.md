# Apollo:

## Introduction:
This is a web challenge, opening the link we were given shows us a page titled `Ugly Colors Palette`, with a group of collors changing.

## Deep in the challenge:
Opening the network tab under `Inspect` on the browser and reloading the page shows us that the website is sending post request to `http://web.ingehack.ingeniums.club:3000/api/96b97cfae94f1e5deeb3f086aa34f45e/graphql`
with the following request body:
```
query: "{ colors { name, hex } }"
```
From this request, the url we are sending to and the name of the challenge, we find that it's a `Apollo GraphQL` backend.

Trying to send our own requests using `postman` to the same url, with the following body: 
```
query: "{ flag  }"
```
we get the following response:
```
{
    "errors": [
        {
            "message": "Cannot query field \"flag\" on type \"Query\". Did you mean \"fl4g\"?",
            "locations": [
                {
                    "line": 1,
                    "column": 3
                }
            ],
            "extensions": {
                "code": "GRAPHQL_VALIDATION_FAILED"
            }
        }
    ]
}
```

and from its message, we know that the correct query should contain `fl4g`.
So, let's try the following query:
```
{"query":"{ fl4g { flag } }"}
```

and the response was again the same as the previous one, and changing it to :
```
{"query":"{ fl4g { fl4g } }"}
```
we get:
```
{
    "data": {
        "fl4g": [
            {
                "fl4g": "SW5nZUhhY2t7SV9zaDB1bGRfUzNjdXIzX015X0dyNHBoUWxfUzNydjNyXzopKSkpKX0="
            }
        ]
    }
}
```

So it's a `base64` encoded text, and decoding it give us the flag:
```
IngeHack{I_sh0uld_S3cur3_My_Gr4phQl_S3rv3r_:)))))}
```