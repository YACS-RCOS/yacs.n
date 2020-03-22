# YACS.n

YACS with support for multi and sub-semesters for any school

---

## Development

You should have a postgresql db running on your machine

**1. Build Schema**

from src/data
run `bash build.sh` to build the schema

**2. Run**

```bash
npm i && FLASK_APP=src/app.py npm start
```

You should be able to access @ `localhost:8080`

**3. Populate with your schools data**

In `localhost:8080/admin` submit your school's courses by CSV and you're ready to schedule!

For schema see /rpi-data/summer-2020.csv as an example

## YACS at your school?

`in development`
