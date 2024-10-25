
## About

This Django project aims to help people secure jobs in IT.\
It will include various features to make the process more efficient, faster,\
and convenient.

## Technologies used

These are a few of the main technologies that have been used in the project:
- Python (3.10)
- Django Rest Framework (3.14.0)
- Docker (26.0.0)

## Tools installation:
- If you're on Windows please install ```WSL```. To ensure you already have it type:
```
wsl --version
``` 
<i class="fas fa-copy"></i>

- Install ```task``` if you don't have it, or check by typing:
```
task --version
```
<i class="fas fa-copy"></i>

- If you don't have ```task``` make sure you have ```scoop```:
```
scoop --version
``` 
<i class="fas fa-copy"></i>
- If you don't have both, install them by doing the following:\
For Windows, please open your ```PowerShell``` and launch this command:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```
<i class="fas fa-copy"></i>
Then launch the next command:
```
scoop install task
```
<i class="fas fa-copy"></i>
- Lastly [Download Docker Desktop](https://www.docker.com/products/docker-desktop/), register and start it.\
Make sure you have ```Docker Desktop``` running every time you're launching the project in ```Docker```

## Project installation:
- Clone the project.
```
git clone https://github.com/RuslanSlepuhin/server_bot.git
```
<i class="fas fa-copy"></i>

- Go to the project directory and launch:
```
git config core.autocrlf false
```
<i class="fas fa-copy"></i>

- Save the ```example.env``` file  as ```.env``` in the same directory.
- Fill out the ```.env``` file with your data.

## Project launching:
- To build and start:
```
task docker-up
```
<i class="fas fa-copy"></i>

- To stop:
```
task docker-down
``` 
<i class="fas fa-copy"></i>
- To use both frontend and backend parts of the project open in your browser:
```
http://localhost
```
<i class="fas fa-copy"></i>
- To use just the backend open in your browser:
```
http://localhost:8000
```
<i class="fas fa-copy"></i>
