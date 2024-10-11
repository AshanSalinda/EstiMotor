# Power Shell Commands for the Project



- To run as Administrator
  ```
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- To create virtual environment
  ```
    python -m venv venv
  ```

- To Activate the venv
  ```
    .\venv\Scripts\Activate.ps1
  ```

- To Deactivate the venv
  ```
    deactivate
  ```

- To Remove venv
  ```
    Remove-Item -Recurse -Force venv
  ```

- To install the dependencies on requirements.txt
  ```
    pip install -r requirements.txt
  ```

- To Update the
  ```
    pip freeze > requirements.txt
  ```

