# Backend with fastapi

## isinstance()
The built-in function isinstance(object, classinfo) is used to check if an object is an instance of a specified class or a tuple of classes.

## Post
To test post in swagger, use this json: 

```python
{
        "id": 0,
        "nickname": "Scanbo",
        "fullname": "Scanlan Shorthalt",
        "occupation": ["Wizard","Adventurer","Deity"],
        "powers": [ "Arcane magic proficiency", "Lute playing","Charisma"],
        "hobby": ["Singing", "Having sex"],
        "type": "Casanova",
        "rank": 65
},
{
        "id": 12,
        "nickname": "Finn",
        "fullname": "Finn Quickstep",
        "occupation": ["Bard", "Diplomat"],
        "powers": ["Charm", "Inspiration", "Illusion"],
        "hobby": ["Playing lute", "Storytelling"],
        "type": "Bard",
        "rank": 42
        },
{
        "id": 13,
        "nickname": "Kael",
        "fullname": "Kael Frostborne",
        "occupation": ["Cryomancer", "Hunter"],
        "powers": ["Ice blast", "Freeze", "Blizzard"],
        "hobby": ["Ice sculpting", "Mountain climbing"],
        "type": "Mage",
        "rank": 59
},
{
        "id": 14,
        "nickname": "Raven",
        "fullname": "Raven Darkwing",
        "occupation": ["Shapeshifter", "Spy"],
        "powers": ["Transformation", "Flight", "Mimicry"],
        "hobby": ["Bird watching", "Aerial acrobatics"],
        "type": "Shifter",
        "rank": 50
},
{
        "id": 15,
        "nickname": "Thorne",
        "fullname": "Thorne Bloodaxe",
        "occupation": ["Berserker", "Chieftain"],
        "powers": ["Rage", "Cleave", "Regeneration"],
        "hobby": ["Battle training", "War drums"],
        "type": "Berserker",
        "rank": 63
}

```

# Docker

## Entrypoint vs Dockerfile vs Docker Compose

**The Analogy**: Building a House vs. Moving In

### 1- Dockerfile (The Construction Crew)

***When it happens:*** "Build Time" (once, when you run docker build).

***What it does:*** It builds the house. It lays the foundation (Linux), installs the plumbing (Python), puts in the furniture (Dependencies), and locks the door.

***Result:*** A static "Image". It is frozen. You can't change the walls once the house is built.


### 2- Entrypoint (The Mover)

***When it happens:*** "Run Time" (every time you run docker up).

***What it does:*** It happens the moment you unlock the door to move in. It checks if the electricity is on (Database is ready), arranges your personal items (Environment variables), and then finally lets you start living (Runs the app).


### 3- Docker Compose

While `Dockerfile` defines *WHAT* the container is - "I am a Linux machine with Python and these specific files installed"-,
`docker-compose.yml` defines *HOW* to run that container: "Take that blueprint, build it, name it 'api', open port 8000, and link these folders."


## How to run Fastgres from docker
```shell
docker compose up --build
```


# PostgreSQL

## How to install it

### Update and install dependencies

```shell
sudo apt update && sudo apt upgrade -y
sudo apt install wget software-properties-common apt-transport-https ca-certificates -y
```
### For newer versions of Ubuntu (25)
```shell
# Create the Keyring Directory
sudo install -d /usr/share/postgresql-common/pgdg

# Import the Key (The Modern Way)
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc

# Add the Repository with "Signed-By"
echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Install
sudo apt update
sudo apt install postgresql-16 postgresql-contrib -y
```

### For older versions of Ubuntu

```shell
# Import GPG key to verify the packages:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Add the repository to your system
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list

# Install POstgreSQL
sudo apt update
sudo apt install postgresql-16 postgresql-contrib -y
```

### Verify the installation
```shell
sudo systemctl status postgresql

# sudo systemctl start postgresql
# sudo systemctl stop postgresql
# sudo systemctl enable postgresql => will start postgresql auto each time you boot your pc

```

## Basic Configuration & Access

PostgreSQL uses "ident" authentication by default, meaning it associates Postgres roles with matching Unix/Linux system accounts.

In PostgreSQL, a **Role** is a single concept that replaces the traditional idea of "Users" and "Groups."

While other systems separate people (users) from their departments (groups), Postgres treats them as the same type of entity. 
Whether a role acts as a user or a group simply depends on how you configure it

### User vs Group

*User Role:* A role that has the LOGIN permission. This is an account you can actually use to connect to the database (it usually has a password).

*Group Role:* A role that does not have the LOGIN permission. You can't log in as this role; instead, you grant this role to other users so they "inherit" its permissions.

By default, we have a `postgres` role (**system user** and **database role**) with no password

Need to log in for the first time to this default `postgres` user

```shell
sudo -i -u postgres
psql
```
```sql
ALTER USER postgres WITH PASSWORD 'postgres';
-- or ALTER ROLE postgres PASSWORD 'postgres';
\q
```
```shell
exit
```

To verify if password works:

```shell
psql -h localhost -U postgres
```


# Install Pgadmin

## 1. Setup the repository key:

```shell
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
```

## 2. Add the repository:

```shell
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```

## 3. Install pgAdmin 4 (Desktop mode):

```shell
sudo apt install pgadmin4-desktop
```

## 4 . Add psycopg and sqlmodel in .toml file

Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

It's a translator or bridge:

* Python speaks in objects, variables, and functions.
* PostgreSQL speaks in SQL queries, tables, and rows.
* Psycopg sits in the middle, allowing your Python code to send commands to the database and receive data back in a format Python can understand.

***What is it used for in a Python Backend?***

In a backend application, Psycopg handles the low-level communication details:

* Connecting: It establishes the network connection to the PostgreSQL server.
* Executing Queries: It sends SQL statements (SELECT, INSERT, UPDATE) to the database.
* Data Conversion: It converts Python types (like int, datetime, str) into PostgreSQL types and vice versa.
* Security: It handles parameter binding to prevent SQL injection attacks.

# ORM

Object-Relational Mapping: You are "mapping" a Python Object to a Relational Database Row.

***Class:*** It defines how you interact with the data in your Python code. 

***Table:*** It defines how the data is structured in your Storage through sql.

Class   <---------------------------->    Table
Python                                    SQL

Table is a `sql table` representation of class in sql language, so that if we create a new hero in python, we can easily add this data into sql.


When you work with SQLModel, the "bridge" between your Python code and the SQL database works like this:

**The Python Object:** You create an instance of your class in memory. It's just a bunch of data sitting in your RAM.

**The Session:** You hand that object to a "Session" (which is like a conversation with the database).

**The SQL Translation:** SQLModel looks at your object, looks at your class definition, and automatically writes the INSERT INTO hero... SQL command for you.


# Snippet explanation

## *args vs **kwargs
While **kwargs handles named items (like a dictionary), 
*args is used when you want to pass a variable number of positional arguments (like a list or tuple).

They are like variadic functions in C:

| Feature           | `*args`                           | `**kwargs`                                      |
|-------------------|-----------------------------------|-------------------------------------------------|
| Name              | Positional Arguments              | Keyword (Named) Arguments                       |
| C Equivalent      | `va_arg` (indexed/sequential)     | (No direct C equivalent—like passing a Hashmap) |
| Data Structure    | Tuple `(1, 2, 3)`                 | Dictionary `{'a': 1, 'b': 2}`                   |
| Used when...      | You have a list of similar items. | You want to set specific named properties.      |
| Example call      | `func(1, 2, "three")`             | `func(id=1, name="Hero")`                       |


## How to use **kwargs

```python
def update_hero(hero_id: int, **kwargs) -> Optional[Hero]:
```
We use it like this:
```python
# Both health and nickname are sent in **kwargs
update_hero(1, health=120, nickname="Super Sparky")

#or 
new_data = {"speed": 7.5, "role": "Warrior"}
update_hero(1, **new_data)
```
## `setattr()`

Use it when you don't know the name of the attribute until the code is actually running.

```python
setattr(hero, key, value)
```
it's like hero.key=value but allows the attribute name to be a string variable

## `session.exec()`

session.exec() returns an iterable result object, that's why sometimes we need to use first()

## DATABASE_URL

- **Format**: postgresql://user:password@host:port/database_name

If you are running this LOCALLY (outside docker), use `localhost`
If you are running this INSIDE docker, use `db` (the service name)

```python
DATABASE_URL = f"postgresql://{DB_USER}:{load_password()}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
```
postgresql:// -> defaults to psycopg2 (which we don't have)