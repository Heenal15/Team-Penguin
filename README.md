# Team Penguin Small Group project

## Deployment notes
If cloning from the github repo, ensure you follow the 'Installation instructions' in order to run the project successfully.
If you expereince any errors when logging in especailly after signing up please log out, you may use this link to do so at [Log Out](https://guarded-scrubland-54800.herokuapp.com/log_out/)

## Team members
The members of the team are:
- Heenal Vyas
- Yiting Gao
- Abdurrahman (Abdi) Lleshi
- Kai Corr
- Abbenayan Jeyakumar

## Chess Club Management System
The chess club system allows officers and club owner of a club to manage memberships of the club.
Users register on the website and become an applicant, awaiting approval or rejection from an officer or club owner.
Applicants at this stage can only edit their profile once they log into the site.
Once approved and a member; a member can access a list of other members.
The list displays the name, public bio and gravatar of each member.
Club owners can promote a member to an officer and demote an officer to a member.
A club owner can transfer ownership to another officer.
A member can register and create a club which can be viewed by all users.

## Project structure
The project is called `system`.  It currently consists of a single app `clubs`.

## Deployed version of the application
The deployed version of the application can be found at [URL](https://guarded-scrubland-54800.herokuapp.com/)

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
`
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
