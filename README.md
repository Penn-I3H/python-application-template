# python-application-template

Ensure that your main file makes use of the `INPUT_DIR` and the `OUTPUT_DIR` ENVIRONMENT variables, to access input files and to write output.

Add additional dependencies to the `Dockerfile`.

To run locally:

Run: `docker-compose up --build`

The above will create a `data` directory in your root directory locally.

The example copies files from the `INPUT_DIR` directory to the `OUTPUT_DIR` directory. The directories are set in `dev.env` and are defaulted to `/service/data/input` and `/service/data/ouput` for the input and output directories respectively.
To test, create `input`, `output` and `resources` subfolders in the `data` directory. Create a test file (for example `test.txt`) in the `/service/data/input` directory. 

Re-Run: `docker-compose up --build`

The testfile should be copied to the `data/output` directory.
