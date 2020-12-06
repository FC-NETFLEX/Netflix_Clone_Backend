[![codecov](https://codecov.io/gh/FC-NETFLEX/Netflix_Clone_Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/FC-NETFLEX/Netflix_Clone_Backend)![Netflex CI](https://github.com/FC-NETFLEX/Netflix_Clone_Backend/workflows/Netflex%20CI/badge.svg?branch=master)

# NetFlex - Netflix Clone Project

Netflex API

## Team

1. 박홍빈
2. 허범영



## API Document

> 도메인 변경 (netflexx.ga -> hbyyynetflex.xyz)

https://documenter.getpostman.com/view/9448934/Szf24q2x



## Installation

- package management
  - use poetry



**`Poetry Install`**

```shell
# osx, linux
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# windows
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

**`package install`**

- poetry install
- pip install -r requirements.txt



## requirements

for using, you need secret key

- secret file structure

```
{
  "netflex": {
    "DJANGO_SECRET_KEY": "",
    "dsn": "",
    "AWS_ACCESS_KEY_ID": "",
    "AWS_SECRET_ACCESS_KEY": "",
    "DATABASES": {
      "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": 
     	 }    
    	}
	}
}
```

