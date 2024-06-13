# Business Central API fields optimization :safety_vest:

This project is a simple tool to search which fields returned by the Business Central API are used in the project. The goal is to optimize the API calls by only returning the fields that are used in the project.

## Table of contents

- [Business Central API fields optimization :safety\_vest:](#business-central-api-fields-optimization-safety_vest)
  - [Table of contents](#table-of-contents)
  - [How to use it ?](#how-to-use-it-)
  - [Technologies](#technologies)
  - [Authors](#authors)

## How to use it ?

```bash
$ git clone https://github.com/AlxisHenry/business-central-api-fields-optimization.git
```

Copy the `.env.example` file to `.env`

```bash
$ cp .env.example .env
```

Configure the environment variables in the `.env` file

```bash
$ cat .env
BC_BASE_ENDPOINT=https://...
ADDITIONALS_PARAMS=""
CLIENT_ID=""
CLIENT_SECRET=""
ROOT=""
```

Configure your target entities in the `targets.json` file. Note that the entity name is case unsensitive.

```json
{
  "entities": [
    "contacts",
    "customers",
    "someentity"
  ]
}
```

Install the python dependencies

```bash
$ pip install -r requirements.txt
```

Run the script

```bash
$ python app.py
```

The script will generate a `unused_keys.txt` file with the unused fields for each entity. And a `used_keys.txt` file with the used fields for each entity.

```bash
$ ls entities
unused_keys.txt  used_keys.txt
```

## Technologies

![](https://img.shields.io/badge/python-%252320232a.svg?style=for-the-badge&logo=python&color=20232a)

## Authors

- [@AlxisHenry](https://github.com/AlxisHenry)