# YACS.n

![](https://github.com/YACS-RCOS/yacs.n/workflows/CI/badge.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/yacs-rcos/yacs.n/badge)](https://www.codefactor.io/repository/github/yacs-rcos/yacs.n)
[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)

YACS with support for multi and sub-semesters for any school

## YACS at your school?

Clone the repo and

`scripts/start.sh`

Once up,

Head to the admin panel at `/admin`

You'll be able to

1. Import courses
2. Select default semesters
3. Rename semester parts (useful for semesters that are split in parts)

Head to `/` and allow your peers/students to schedule away!

## Development

You should have a postgresql db running on your machine

**1. Build Schema**

from src/data
run `bash build.sh` to build the schema

**2. Run**

```bash
npm i && FLASK_APP=src/api/app.py npm start
```

You should be able to access @ `localhost:8080`

**3. Populate with your schools data**

In `localhost:8080/admin` submit your school's courses by CSV and you're ready to schedule!

For schema see /rpi_data/summer-2020.csv as an example

Alternatively to develop using docker

**Start containers**

`bash scripts/dev-start.sh`

**Stop containers**

`bash scripts/dev-stop.sh`
