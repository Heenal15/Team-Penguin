# Team Penguin Small Group project

## Team members
The members of the team are:
- Heenal Vyas
- Yiting Gao
- Abdurrahman (Abdi) Lleshi
- Kai Corr
- Abbenayan Jeyakumar


## Project structure
The project is called `system`.  It currently consists of a single app `clubs`.

## Deployed version of the application
The deployed version of the application can be found at [URL](URL).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Any errors with the database:

```
$ python3 manage.py migrate --run-syncdb
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`
All the code has borrowed ideas from the recommended training videos.