# REST API service.

Service realized on FastAPI framework with PostgreSQL DB in Docker containers.

### Endpoints
* ___/uploadfile/___ - upload Excel file with extension .xlsx to pass data to DB
* ___/download/{version}___ - download Excel file with data from previously uploaded file with required version
* ___/diagram/___ - get json data to draw diagram with required parameters (version of uploaded file, required year, type of values)

### DB tables
* ___types___ - types of table values to facilitate process of receiving data for diagram where type is one of parameters
* ___projects___ - data about projects (code, name)
* ___files___ - version of uploaded files
* ___records___ - value from tables at certain dates

### Startup
To start the application just run 'docker compose up' from CLI in root folder of project.

### Documentation
Description of application is available at <localhost:8000/docs>. You may try out all endpoints there.