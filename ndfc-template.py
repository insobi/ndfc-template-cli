import requests
import os
from urllib3.exceptions import InsecureRequestWarning
import click
from prettytable import PrettyTable

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ndfcTemplate(object):
    def __init__(self):
        self.base_url = ""
        self.username = ""
        self.password = ""
        self.domain = ""
        self.ssl_verify = False
        self.headers = {"Content-Type": "text/plain"}

    def login(self, user, pw, url, domain='local'):
        self.base_url = url
        self.username = user
        self.password = pw
        self.domain = domain
        payload = f'{{ "userName": "{self.username}", "userPasswd": "{self.password}", "domain": "{self.domain}" }}'
        response = requests.request(
            'POST',
            f'{self.base_url}/login',
            headers=self.headers,
            data=payload,
            verify=self.ssl_verify
        )
        if response.status_code == 200:
            self.headers["Cookie"] = f'AuthCookie={response.json()["jwttoken"]}'
        else:
            print("Login Failed.")
            exit(1)

    def list(self, name:str) -> list:
        template_list = []
        response = requests.request(
            "GET",
            f'{self.base_url}/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/{name}',
            headers=self.headers,
            verify=self.ssl_verify
        )
        if response.status_code == 200:
            if name == '':
                for item in response.json():
                    template_list.append(item)
            else:
                template_list.append(response.json())
        return template_list

    def get(self, template_name: str, path: str) -> None:
        response = requests.request(
            "GET",
            f'{self.base_url}/appcenter/cisco/ndfc/api/v1/configtemplate/rest/config/templates/{template_name}',
            headers=self.headers,
            verify=self.ssl_verify
        )
        content = response.json()["content"]
        with open(f"{path}/{template_name}.template", "w") as f:
            f.write(content)

@click.group()
@click.pass_context
def ndfc_template(ctx):
    '''
    Command Line Interface for managing Cisco NDFC Template
    '''
    if "NDFC_USERNAME" not in os.environ or "NDFC_PASSWORD" not in os.environ or "ND_URL" not in os.environ:
        click.secho(
            "ERROR: You must specify NDFC_USERNAME and NDFC_PASSWORD and ND_URL as environment variables.",
            fg="red"
        )
        exit(1)

    obj = ndfcTemplate()
    obj.login(
        user=os.environ['NDFC_USERNAME'],
        pw=os.environ['NDFC_PASSWORD'],
        url=os.environ['ND_URL'],
        domain=os.environ['ND_DOMAIN']
    )
    ctx.obj = obj

@click.command()
@click.pass_obj
@click.option("--name", type=str, required=False, default='', help='template name')
@click.option("--all", 'type', flag_value='all', default=True)
@click.option("--template-cli", 'type', flag_value='TEMPLATE_CLI', default=True)
@click.option("--python", 'type', flag_value='PYTHON', default=True)
def list(obj, name, type):
    '''Display a list of template from NDFC'''
    table = PrettyTable()
    table.field_names = [
        "name",
        "templateType",
        "templateSubType",
        "contentType",
        "supportedPlatforms"
    ]
    table.align = "l"
    for item in obj.list(name=name):
        row = [
            item["name"],
            item["templateType"],
            item["templateSubType"],
            item["contentType"],
            item["supportedPlatforms"]
        ]
        if type != 'all':
            if item["contentType"] == type:
                table.add_row(row)
        else:
            table.add_row(row)
    click.echo(table)

@click.command()
@click.pass_obj
@click.option("--name", type=str, required=False, help='name of template to download')
@click.option("--all", 'all', flag_value=True, default=False, help='download all templates')
@click.option("--path", type=str, required=True, default=".", help='path for downloading files')
def get(obj, name, all, path):
    '''Download NDFC template(s)'''
    if not name and not all:
        print("Error: Command 'get' requires arguments: --all or --name")
        exit(1)
    if not all:
        obj.get(name, path)
    elif all:
        templates = []
        for template in obj.template_list():
            obj.get(template['name'])

ndfc_template.add_command(list)
ndfc_template.add_command(get)

if __name__ == "__main__":
    ndfc_template()
