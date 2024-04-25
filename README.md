# ParkingManagement


## Problem description

We are a large office with a small car park. Our team has been tasked with building a website to help us to manage the car park. A number
plate recognition system is in place, and we'd like to only allow the entrance to the car park to open if the number plate seen is one of our
employees. We want to be able to track the make, model and colour of the car as well as the owner of the car.

- Cars may only have one owner, but it's possible for one person to have many cars

- Private and international number plates are considered out of scope. Standard format of ```LLNN LLL``` is to be taken into consideration
only.

- Some kind of local persistent storage should be used to retain data across application restarts

- Please treat this application as production ready


## Http API endpoints

- List all available car makes and models. It should be possible to search the cars by make.
- List all registered employee cars. It should be possible to search for an employee by name.
- Add a new car make and model.
- Register a new car for an employee.
- Check whether a given number plate is registered by employees or not
- Perform a health check on the system


### Prerequisites

- Python 3.8 or later

## Installation


### Step 1: Move to the Project Directory

Navigate to the directory where you want to clone the project.
```bash
cd <path/to/project_directory>
```

### Step 2: Pull the project

```bash
git pull 
```


### Step 2: Create a Virtual Environment (Recommended)

It's recommended to create a virtual environment to isolate project dependencies. Run the following command to create a virtual environment named venv:

```bash
python -m venv venv
```
Activate the virtual environment:

On macOS and Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Dependencies
Install all required packages using requirements.txt:
```bash
cd ParkingManagement
```


```console
pip install -r app/requirements.txt
```

### Step 4: Running the Application
Start the application with Uvicorn:

```console
uvicorn app.main:app --reload
```

### Step 5: Adding given employees to our Database

```console
python3 add_emp_external.py
```


## Usage

Navigate to ``` http://127.0.0.1:8000/docs``` 

And access the endpoints via browser

#### Available Endpoints
-   GET - /health: Health check endpoint to verify the application is running.
-   POST - /car - Add a new employee
-   GET - /car - Get all cars
-   GET - /car/{car_make} - Filter cars by "car_make"
-   PUT - /car/{car_id} - Update Car
-   DELETE - /car/{car_id} - Delete Car

-   PUT - /car/register/{number_plate} - Add car to an employee
-   GET - /car/register/ - GET all registered Cars with employees
-   GET - /car/register/{emp_name} - GET cars registered for a particular employee

-   GET - /car/is_registered/{number_plate} - GET number plate is registered or not
-   POST - /emp - Add a new employee
-   GET - /emp - Get all employees
## Testing
Run tests using pytest:

```console
pytest
```

Contact
Raghuvir Dav - [davraghuvir9@gmail.com]

https://www.raghuvir.me