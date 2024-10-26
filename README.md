# HTP 

Simple and efficient ergonomic (at least for me) http client written in python.

Similar to `curl` or `httpie` but they didn't have features I wanted by default
so I made my own toned-down version for common use cases.

Features:

- Automatically include authentication token in headers
- Set a base url for the api so you can send requests to `/endpoint` rather than
  `http://localhost:8000/api/v1/endpoint`
- Send requests with json data (body) by using `--data key1=value1 key2=value2`
  rather than doing some scuffed `'{"key1": "value1", "key2": "value2"...}'` and
  so on.
- Extract specific fields from the json response body using `--fields
  field1,field2` rather than using `jq`'s scuffed syntax to filter through the
  json response.
- Log in / Do some Authentication with a username & password and the
  `Authorization` header will be saved and used for all other requests.
- Send requests to any URL by using the `--url` flag just like how you would
  with `curl` or `httpie`. 
- And some other cool shit.

> **Note**: This tool is built as per my preferences and ergonomics so you
> probably dont wanna bother using it since it could/will be confusing. I've
> been using this script (now updated with some more features) for a long time
> and its annoying having to use my dotfiles for it which is why I've made this
> public repo. The code is public so if you wanna see how it works, its here-
> but dont't expect me to accept pull requests or issues since I've built this
> for myself and it just happens to be public. 

<!--toc:start-->
- [HTP](#htp)
- [Installation](#installation)
- [Docs](#docs)
  - [Brief](#brief)
  - [Cheatsheet](#cheatsheet)
- [Usage](#usage)
    - [Setting the Base URL](#setting-the-base-url)
    - [Logging In](#logging-in)
    - [Sending Requests](#sending-requests)
<!--toc:end-->

There are 2 places to find the documentation. One is here in the readme (which
is incomplete and will stay that way) and the other is by passing the `doc`
argument to the script like so:

```shell 
htp doc
```

Which will pretty much display the same content as the [doc](#doc) or
[cheatsheet](#cheatsheet) section on this readme.

Why are the docs inside the script itself ? *everywhere at the end of time
starts playing... 🫠*

# Installation

You can install this script by either directly downloading the `htp.py` file
with curl/wget (or others) or by cloning the repo and using the `./Makefile`.

Requirements: 

- Python3 

Optional requirements:

- `curl` if you want to install with curl 
- `wget` if you want to install with wget
- `git` and `make` if you want to clone the repo and install with make 

Install with curl (requires elevated privileges):

```bash
sudo curl -L -o /usr/local/bin/htp https://raw.githubusercontent.com/fluffysnowman/htp/master/htp.py && sudo chmod +x /usr/local/bin/htp
# or replace /usr/local/bin/htp with any directory/file in your $PATH
```

Install with wget (requires elevated privileges):

```bash
sudo wget -O /usr/local/bin/htp https://raw.githubusercontent.com/fluffysnowman/htp/master/htp.py && sudo chmod +x /usr/local/bin/htp
# or replace /usr/local/bin/htp with any directory/file in your $PATH
```

Install with git & make:

```bash
git clone https://github.com/FluffySnowman/htp 
cd htp 
# this will make the script executable and copy the script to /usr/local/bin/htp
make install 
```


# Docs 

Below are the docs for the `htp` script (also embedded into the script itself)

## Brief

This script is meant to make it easier to interact with APIs that have dynamic
data (i.e. authentication tokens) that need to be passed with each request.

Most of the time, you will need to set the base URL for the API after which you
can simply send requests to each endpoint by using the path
`/api/v1/my-endpoint` rather than having to do the whole
`http://localhost:8000/api/v1/my-endpoint` every time and including headers and
writing json data to send in the request body and then using `jq`'s scuffed
syntax to filter through it.

This script also allows you to log in to the API to obtain an authentication
token which is then sent with all requests.

## Cheatsheet

- Set Base URL

`htp set-base-url --base-url http://localhost:8000/api/v1`

- Log In 

`htp login --username admin --password secret`

- Log In Direct URL 

`htp login --url http://localhost:8888/login --username myuser --password mypass`

- Send GET Request 

`htp req GET /users`

- Send GET Request to anywhere (like curl) 

`htp req GET --url http://localhost:8888/get-something`

- Send POST Request & Extract JSON Fields 

`htp req POST /jsonshit --fields username,user_id`

- Send POST Request w/ JSON data

`htp req POST --url http://localhost:8888/login --data username=shit password=notshit`

<br /> 
<hr /> 
<br />
<hr /> 

The docs below are incomplete and will not be completed since I'm the only guy who's
gonna use this.

# Usage 

### Setting the Base URL

Set the base URL for the API:

```sh
htp set-base-url --base-url http://localhost:8000/api/v1
```

This will create a `.htp/` directory in the current directory that you are in.
Remember to add this directory to your `.gitignore` or `.dockerignore` etc.

The base url will be save to the `.htp/base_url.env` file.

### Logging In

Log in to the API to obtain an authentication token:

```sh
htp login --username your_username --password your_password
```

By default this will send a POST request to `${base_url}/login` and will save
the contents of the `Authorization` header to `.htp/auth_token.env` file.

You can also manually specify the endpoint to send the login request to:

```sh
htp login --url http://localhost:8888/login --username myuser --password mypass
```

Which will also save the contents of the `Authorization` header to
`.htp/auth_token.env` file (even if empty).

### Sending Requests

Each request will automatically include the authentication token in the headers.
If you wish to manually specify a url to send a request to then the `--url` flag
can be used just like how you would with curl, httpie etc.

Send a GET request to an endpoint:

```sh
# Send a GET request to ${base_url}/endpoint 
htp req GET /endpoint
# Send a GET request to http://localhost:8000/api/v1/endpoint 
htp req GET ...
```

**THIS DOCUMENTATION IS INCOMPLETE AND WILL PROBABLY NOT BE UPDATED** since I
can't be arsed writing documentation for something only I will use. Hence
there's a cheatsheet.

<!-- AI GENERATED SLOP BELOW -->
<!-- AI GENERATED SLOP BELOW -->
<!-- AI GENERATED SLOP BELOW -->
<!-- Send a POST request with data: -->

<!-- ```sh -->
<!-- ./htp.py req POST /endpoint --data key1=value1 key2=value2 -->
<!-- ``` -->

<!-- Extract specific fields from the response: -->

<!-- ```sh -->
<!-- ./htp.py req GET /endpoint --fields field1,field2 -->
<!-- ``` -->

<!-- ### Examples -->

<!-- 1. **Set the Base URL** -->

<!--     ```sh -->
<!--     ./htp.py set-base-url --base-url http://api.example.com -->
<!--     ``` -->

<!-- 2. **Log In** -->

<!--     ```sh -->
<!--     ./htp.py login --username admin --password secret -->
<!--     ``` -->

<!-- 3. **Send a GET Request** -->

<!--     ```sh -->
<!--     ./htp.py req GET /users -->
<!--     ``` -->

<!-- 4. **Send a POST Request with Data** -->

<!--     ```sh -->
<!--     ./htp.py req POST /users --data name=John age=30 -->
<!--     ``` -->

<!-- 5. **Extract Specific Fields from the Response** -->

<!--     ```sh -->
<!--     ./htp.py req GET /users --fields id,name -->
<!--     ``` -->

<!-- ### Cheatsheet -->

<!-- - **Set Base URL:** `./htp.py set-base-url --base-url <URL>` -->
<!-- - **Log In:** `./htp.py login --username <USERNAME> --password <PASSWORD>` -->
<!-- - **Send GET Request:** `./htp.py req GET <ENDPOINT>` -->
<!-- - **Send POST Request:** `./htp.py req POST <ENDPOINT> --data <KEY=VALUE>...` -->
<!-- - **Extract Fields:** `./htp.py req <METHOD> <ENDPOINT> --fields <FIELD1,FIELD2,...>` -->

<!-- """ -->


