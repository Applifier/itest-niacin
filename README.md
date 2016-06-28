# itest-niacin

Python Requirements
------
* Python 3
```
brew install python3
easy_install virtualenv
```
* Please install required packages using (system wide)
```
[itest-niacin]$ pip install -r requirements.txt
```
* or then use virtualenv
```
[itest-niacin]$ ./install_and_start_py.sh setup_virtualenv
## and activate
[itest-niacin]$ source activate_venv.sh
## and install requirements
[itest-niacin]$ pip install -r requirements.txt
...do awesome stuff..
## and how to deactivate
(.env) [itest-niacin]$ deactivate
```
* if you install new packages inside virtualenv for itest-niacin freeze them to requirements
```
(.env) [itest-niacin]$ pip freeze > requirements.txt
```