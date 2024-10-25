#!/usr/bin/env python3

import sys
import json
import os
import urllib.request
import urllib.error
import urllib.parse
import argparse
from typing import Optional, Dict, Any

class HttpClient:
    def __init__(self):
        self.config_dir = ".htp"
        self.ensure_config_directory()
        self.base_url = self.read_config_file("base_url.env")
        self.token = self.read_config_file("auth_token.env")

    def ensure_config_directory(self):
        """Create .htp directory if it doesnt exist"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def read_config_file(self, filename: str) -> Optional[str]:
        """Read config  from file"""
        filepath = os.path.join(self.config_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read().strip()
        return None

    def write_config_file(self, filename: str, content: str):
        """Write configuration to file"""
        filepath = os.path.join(self.config_dir, filename)
        with open(filepath, 'w') as f:
            f.write(content)

    def parse_key_value_pairs(self, pairs: list) -> Dict[str, Any]:
        """Convert key value pairs to json"""
        result = {}
        for pair in pairs:
            key, value = pair.split('=', 1)
            # trynna convert to int/number
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                # keep string if it cant do quik mafs with numbers
                pass
            result[key] = value
        return result

    def login(self, username: str, password: str):
        """Handle login and token storage"""
        if not self.base_url:
            print("base url not set. Set it using --set-base-url")
            sys.exit(1)

        url = f"{self.base_url}/login"
        data = json.dumps({"username": username, "password": password}).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as response:
                if "Authorization" in response.headers:
                    auth_header = response.headers["Authorization"]
                    self.write_config_file("auth_token.env", auth_header)
                    print("Login success.saved token")
                else:
                    print("login failed-> no auth header?")
                    sys.exit(1)
        except urllib.error.HTTPError as e:
            print(f"HTTPError: {e.code} {e.reason}")
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
            sys.exit(1)

    def send_request(self, request_type: str, endpoint_path: str, data_pairs: Optional[list] = None, fields: Optional[str] = None):
        """send http request with optional data and field filtering"""
        if not self.base_url:
            print("base url not set. Set it using --set-base-url")
            sys.exit(1)

        if not self.token:
            print("auth  token not found. login first")
            sys.exit(1)

        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

        url = f"{self.base_url}{endpoint_path}"
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
    parser = argparse.ArgumentParser(description='htp api shit')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # set base url cmd
    set_base_parser = subparsers.add_parser('set-base-url', help='Set the base url')
    set_base_parser.add_argument('url', help='base url for the api')

    # login cmd
    login_parser = subparsers.add_parser('login', help='login to api')
    login_parser.add_argument('--username', required=True, help='Username')
    login_parser.add_argument('--password', required=True, help='Password')

    # req cmd (actually sending the req)
    req_parser = subparsers.add_parser('req', help='Send a request')
    req_parser.add_argument('method', help='HTTP method (GET, POST, etc.)')
    req_parser.add_argument('path', help='api endpoint path')
    req_parser.add_argument('--data', nargs='+', help='Data in key=value format')
    req_parser.add_argument('--fields', help='comma separated list of fields to extract')

    args = parser.parse_args()
    client = HttpClient()

    if args.command == 'set-base-url':
        client.write_config_file('base_url.env', args.url)
        print(f"Base url set to: {args.url}")
    elif args.command == 'login':
        client.login(args.username, args.password)
    elif args.command == 'req':
        client.send_request(args.method, args.path, args.data, args.fields)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()