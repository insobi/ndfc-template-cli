# NDFC Template CLI
A Command Line Interface designed for listing and downloading NDFC Templates from Cisco NDFC

## Installation

Clone the repo
```bash
git clone https://github.com/insobi/ndfc-template-cli.git
```
Go to your project folder
```bash
cd ndfc-template-cli
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Set environment variables
```bash
export NDFC_USERNAME="admin"
export NDFC_PASSWORD="C1sco12345"
export ND_URL="https://198.18.133.100"
```

Display how to use
```bash
Usage: ndfc-template.py [OPTIONS] COMMAND [ARGS]...

  Command Line Interface for managing Cisco NDFC Template

Options:
  --help  Show this message and exit.

Commands:
  get   Download NDFC template(s)
  list  Display a list of template from NDFC
```

check out list of TEMPLATE_CLI based templates from NDFC
```bash
$ python ndfc-template.py list --template-cli
+-----------------------------------------------+--------------+---------------------------+--------------+-------------------------------------------+
| name                                          | templateType | templateSubType           | contentType  | supportedPlatforms                        |
+-----------------------------------------------+--------------+---------------------------+--------------+-------------------------------------------+
| Default_Network_Extension_Universal           | PROFILE      | VXLAN                     | TEMPLATE_CLI | All                                       |
| Default_Network_Universal                     | PROFILE      | VXLAN                     | TEMPLATE_CLI | All                                       |
| Default_VRF_Extension_Universal               | PROFILE      | VXLAN                     | TEMPLATE_CLI | All                                       |
| Default_VRF_Universal                         | PROFILE      | VXLAN                     | TEMPLATE_CLI | All                                       |
| External_VRF_Lite_eBGP                        | POLICY       | DEVICE                    | TEMPLATE_CLI | All                                       |
| Service_Network_Universal                     | PROFILE      | SERVICE                   | TEMPLATE_CLI | N9K                                       |
...

```

Or check out specific template by name
```bash
$ python ndfc-template.py list --name int_trunk_host
+----------------+--------------+--------------------+-------------+--------------------+
| name           | templateType | templateSubType    | contentType | supportedPlatforms |
+----------------+--------------+--------------------+-------------+--------------------+
| int_trunk_host | POLICY       | INTERFACE_ETHERNET | PYTHON      | All                |
+----------------+--------------+--------------------+-------------+--------------------+
```

Download templates from NDFC
```bash
$ python ndfc-template.py get --name int_trunk_host

$ ls -l int_trunk_host*
-rw-r--r--  1 insekim  staff  12466 Nov 17 11:24 int_trunk_host.template
```