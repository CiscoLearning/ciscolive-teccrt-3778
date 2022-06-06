# Working With Docker Containers

This case study explores how to containerize a Python application using Docker.  The intent is to complete a `Dockerfile` that properly containerizes the application while allowing for persistent storage to be used (for the app's DB), providing a flexible path to the database using environment variables, and being flexible with the mapped port.

The candidate must not only complete the `Dockerfile` but also complete a Bash script that will start the container.

## Starting the Task

Prior to starting the work the database needs to be initialized.  This is done by running the following command:

```sh
make DB_FILE=db/storage.db
```

The reason things are setup this way is to provide for flexible "grading" of the task.  That is, while you provide a solution based on the overall question, grading will be able to easily modify the input data and parameters to ensure that the task was completed successfully, accounting for all of the constraints.
