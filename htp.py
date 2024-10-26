#!/usr/bin/env python3

import sys
import json
import os
import urllib.request
import urllib.error
import urllib.parse
import argparse
from typing import Optional, Dict, Any
from urllib.parse import urlparse

documentation = """
# Cheatsheet

- **Set Base URL:** `./htp.py set-base-url --base-url http://localhost:8000/api/v1`
- **Log In:** `./htp.py login --username admin --password secret`
- **Log In Direct URL** `./htp.py login --url http://localhost:8888/login --username myuser --password mypass`
- **Send GET Request:** `./htp.py req GET /users`
- **Send GET Request to anywhere (like curl):** `./htp.py req GET --url http://localhost:8888/get-something`
- **Send POST Request & Extract JSON Fields:** `./htp.py req POST /jsonshit --fields username,user_id`
- **Send POST Request w/ JSON data:** `./htp.py req POST --url http://localhost:8888/login --data username=shit password=notshit`

"""

class HttpClient:
    def __init__(self, base_url: Optional[str] = None, login_path: str = "/login"):
        self.config_dir = ".htp"
        self.ensure_config_directory()
        self.base_url = base_url or self.read_config_file("base_url.env")
        self.token = self.read_config_file("auth_token.env")
        self.login_path = login_path

    def ensure_config_directory(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def read_config_file(self, filename: str) -> Optional[str]:
        filepath = os.path.join(self.config_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read().strip()
        return None

    def write_config_file(self, filename: str, content: str):
        filepath = os.path.join(self.config_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)

    def parse_key_value_pairs(self, pairs: list) -> Dict[str, Any]:
        result = {}
        for pair in pairs:
            key, value = pair.split('=', 1)
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                pass
            result[key] = value
        return result

    def login(self, username: str, password: str, direct_url: Optional[str] = None):
        url = direct_url if direct_url else f"{self.base_url}{self.login_path}"
        
        if not url:
            print("No URL specified. Use either --url or --base-url")
            sys.exit(1)

        data = json.dumps({"username": username, "password": password}).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as response:
                if "Authorization" in response.headers:
                    auth_header = response.headers["Authorization"]
                    self.write_config_file("auth_token.env", auth_header)
                    print("Login success. saved token")
                else:
                    print("login failed-> no auth header?")
                    sys.exit(1)
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} {e.reason}")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
            sys.exit(1)

    def send_request(self, request_type: str, endpoint_path: Optional[str] = None, 
                    data_pairs: Optional[list] = None, fields: Optional[str] = None, 
                    direct_url: Optional[str] = None):
        if direct_url:
            url = direct_url
        elif self.base_url and endpoint_path:
            url = f"{self.base_url}{endpoint_path}"
        else:
            print("No valid URL specified. Use either --url or (--base-url with path)")
            sys.exit(1)

        headers = {"Content-Type": "application/json"}
        
        if self.token:
            headers["Authorization"] = self.token

        data = None
        if request_type.upper() == "POST" and data_pairs:
            json_body = self.parse_key_value_pairs(data_pairs)
            data = json.dumps(json_body).encode("utf-8")

        req = urllib.request.Request(url, headers=headers, method=request_type.upper(), data=data)

        try:
            with urllib.request.urlopen(req) as response:
                response_text = response.read().decode("utf-8")
                try:
                    response_data = json.loads(response_text)
                    if fields:
                        field_list = fields.split(',')
                        if isinstance(response_data, list):
                            extracted_data = [{field: item.get(field) for field in field_list} for item in response_data]
                        else:
                            extracted_data = {field: response_data.get(field) for field in field_list}
                        print(json.dumps(extracted_data, indent=2))
                    else:
                        print(json.dumps(response_data, indent=2))
                except json.JSONDecodeError:
                    print(response_text)
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} {e.reason}")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='htp api client')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    url_group = argparse.ArgumentParser(add_help=False)
    url_args = url_group.add_argument_group('URL arguments')
    url_args.add_argument('--base-url', help='Override base URL for this request')
    url_args.add_argument('--url', help='Use complete URL (ignores base URL)')

    set_base_parser = subparsers.add_parser('set-base-url', help='Set the base url', parents=[url_group])
    set_base_parser.add_argument('url', nargs='?', help='base url for the api')

    login_parser = subparsers.add_parser('login', help='login to api', parents=[url_group])
    login_parser.add_argument('--username', required=True, help='Username')
    login_parser.add_argument('--password', required=True, help='Password')
    login_parser.add_argument('--login-path', default='/login', help='Custom login endpoint path')

    req_parser = subparsers.add_parser('req', help='Send a request', parents=[url_group])
    req_parser.add_argument('method', help='HTTP method (GET, POST, etc.)')
    req_parser.add_argument('path', nargs='?', help='api endpoint path')
    req_parser.add_argument('--data', nargs='+', help='Data in key=value format')
    req_parser.add_argument('--fields', help='comma separated list of fields to extract')

    subparsers.add_parser('doc', help='Shows Documentation', parents=[])

    args = parser.parse_args()
    
    client = HttpClient(
        base_url=args.base_url if hasattr(args, 'base_url') else None,
        login_path=args.login_path if hasattr(args, 'login_path') else '/login'
    )

    if args.command == 'set-base-url':
        url_to_set = args.base_url if args.base_url else args.url
        if not url_to_set:
            print("Must provide either url positional argument or --base-url")
            sys.exit(1)
        client.write_config_file('base_url.env', url_to_set)
        print(f"Base url set to: {url_to_set}")
    
    elif args.command == 'login':
        client.login(args.username, args.password, direct_url=args.url)
    
    elif args.command == 'req':
        if args.url:
            client.send_request(args.method, direct_url=args.url, data_pairs=args.data, fields=args.fields)
        elif (args.base_url or client.base_url) and args.path:
            client.send_request(args.method, args.path, args.data, args.fields)
        else:
            print("Must provide either --url or (--base-url/configured base URL with path)")
            sys.exit(1)
    elif args.command == 'doc':
      print(documentation)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
