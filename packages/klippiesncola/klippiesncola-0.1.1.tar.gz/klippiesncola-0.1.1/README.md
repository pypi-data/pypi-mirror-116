# klippies and cola : Link your team's call logs, recordings and matters

[![PyPI package](https://img.shields.io/badge/pip%20install-klippiesncola-brightgreen)](https://pypi.org/project/klippiesncola/) [![version number](https://img.shields.io/pypi/v/klippiesncola?color=green&label=version)](https://github.com/kearabiloe/klippiesncola/releases) [![Actions Status](https://github.com/kearabiloe/klippiesncola/workflows/Test/badge.svg)](https://github.com/kearabiloe/klippiesncola/actions) [![License](https://img.shields.io/github/license/kearabiloe/klippiesncola)](https://github.com/kearabiloe/klippiesncola/blob/main/LICENSE)

## klippies and cola (Made in South Africa).
Manage your clips and callers with the swiss army knife for your Debt Collection & tracing Call Center.

## Features
- Easily allocate and visualise matters on [Trello](https://trello.com),
- Bulk download call recordings from your [Switchtel](https://switchtel.co.za) VOIP/PBX account.

### 1. Install klippiesncola

Install klippiesncola and run it:

```bash
pip install klippiesncola
```
### 2. Set environment variables
```sh
export SWITCHTEL_USERNAME='changeme'
export SWITCHTEL_PASSWORD='changeme'
export SWITCHTEL_VPBXNAME='changeme'
export SWITCHTEL_VPBXID='changeme'
```
### 3. Import klippiesncola and test switchtel module

```python
import klippiesncola   

recordings = klippiesncola.switchtel.CallRecording() #loads Switchtel using configured  env variables
todays_recordings = recordings.list('2020-08-25') #loads all calls from date.
```
