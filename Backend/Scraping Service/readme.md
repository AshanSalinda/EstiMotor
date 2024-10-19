# Power Shell Commands for the Project

<br>

- To Activate the venv
  ```
    .\venv\Scripts\Activate.ps1
  ```

- To install the dependencies on requirements.txt
  ```
    pip install -r requirements.txt
  ```

- To Run the App
  ```
    uvicorn app.main:app
  ```

- To Deactivate the venv
  ```
    deactivate
  ```

- To Update the requirements.txt
  ```
    pip freeze > requirements.txt
  ```

- To run as Administrator
  ```
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  
- To create virtual environment
  ```
    python -m venv venv
  ```

- To Remove venv
  ```
    Remove-Item -Recurse -Force venv
  ```





