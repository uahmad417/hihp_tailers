# Description

This repo includes a set of script for tailing and parsing sysmon and scapy data in a honeypot environment. As such it is necassary to first configure sysmon in the target environemnt.

## Environment

The environemnt, which was the high interaction honeypot, in which these scripts were run, used sysmon and scapy for monioritng and logging purposes. The honeypot was set up with a vulnerable web application DVWA to act as an entry point for attackers.

## Scripts

`sysmon_tailer.py` takes an evtx file as input and converts the logs into json format. Requires the `path` field to be set under the `sysmon` section in `config.ini`.

`scapy_monitor.py` monitors and logs all HTTP request messages on the target machine to json format.

`brute_force.py` is fuzzer tool that performs a dictionary attack on the dvwa login page. The different configuration options are provided in `config.ini`.

`elastic_upload.py` uploads the scapy and sysmon logs to elasticsearch.

## Dependecies

Dependencies are provided requirments.txt

First setup virtual environment:

```bash
$ virtualenv env
```

Activate the virtual environment

```bash
$ source env/scipts/activate
```

Install the dependencies:

```bash
$ pip install -r requirements.txt
```
