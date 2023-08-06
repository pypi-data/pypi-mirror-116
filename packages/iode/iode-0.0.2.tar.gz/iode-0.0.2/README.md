# iode
![](./resources/screenshot.png)

![](./resources/iode1.png)

iode is a command-line tool for simple maintenance and management of isolated vscode environments written in Python.


## Installation
Install from pypi
```
pip install iode --user
```
Install from soruce
```
git clone https://github.com/jugangdae/iode
cd iode
pyhton -m build
pip install iode-0.0.1-py3-none-any.whl
```

## Configuration
Using the default setting, does not require a config file
```
iode_run = code
iode_dir = ~/.iode
```
If you want to change the settings, create `~/.iode.config`
```
[default]
iode_run = [code or code-insiders]
iode_dir = [absolute path]
```

## usage

Add new iode env
```
$ iode add [iode_env]
```
```
$ iode a [iode_env]
```
Delete iode env
```
$ iode del [iode_env]
```
```
$ iode d [iode_env]
```
Show iode env list
```
$ iode list
```
```
$ iode l
```
Run iode
```
$ iode run [iode_env] [path]
```
```
$ iode r [iode_env] [path]
```

Show help
```
iode -h
```
```
iode [command] -h
```
