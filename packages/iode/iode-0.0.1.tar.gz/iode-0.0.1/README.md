# IODE

iode is a command-line tool for simple maintenance and management of isolated vscode environments written in Python.

## download

```
git clone https://github.com/jugangdae/iode
cd iode
```

## install

```
pyhton -m build
pip install iode-0.0.1-py3-none-any.whl
```

## config

create `~/.iode/config`
```
$ vi ~/.iode.conf
```
```
[default]
iode_run = code
iode_dir = /Users/username/.iode
```
create `iode_dir`
```
$ mkdir ~/.iode
```

## usage

add new iode env
```
$ iode add [iode_env]
```

delete iode env
```
$ iode del [iode_env]
```

show iode env list
```
$ iode list
```

run iode
```
$ iode run [iode_env] [path]
```
