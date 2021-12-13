# ProcessPayment API

Before running the app assuming that **python 3.7.xx** is installed on development machine

1. Create virtual environment with python3.7.xx
```shell
$ python3.7 -m venv envname
```
2. Activate the virtual environment
```shell
$ source envname/bin/activate
```
3. Install requisite packages:
```shell
$ sh scripts/install_requirements.sh
```
4. Run flask API:
```shell
$ python app.py
```
5. Url:
```
http://0.0.0.0:5051/api/v1/process-payment/ (post)
```
6. In order to Run tests:
```
$ python -m pytest -vv
```
7. Post-man collection under extras folder
i
