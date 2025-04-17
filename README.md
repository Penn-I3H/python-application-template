# python-application-template

Ensure that your main file makes use of the `INPUT_DIR` and the `OUTPUT_DIR` ENVIRONMENT variables, to access input files and to write output.

Add additional dependencies to the `Dockerfile`.

To run locally:

Run: `docker-compose up --build`

The above will create a `data` directory in your root directory locally.

The example copies files from the `INPUT_DIR` directory to the `OUTPUT_DIR` directory. The directories are set in `dev.env` and are defaulted to `/service/data/input` and `/service/data/ouput` for the input and output directories respectively.
To test, create `input` and `output` subfolders in the `data` directory. Create a test file (for example `test.txt`) in the `/service/data/input` directory. 

Re-Run: `docker-compose up --build`

The testfile should be copied to the `data/output` directory.


Read all input parameters from a config.json file. config.json is created by brainlife.io at runtime on the current working directory.
Read all input data from paths specified in config.json (config.json contains both the input parameters; such as command line arguments as well as paths to data files; like t1.nii.gz)
Write all output files in the current directory (./), in a structure defined as a Brainlife datatype. More information about Brainlife datatypes.

App Development Timeline
You would normally follow these steps to develop and register your App on Brainlife.

Develop an algorithm that runs on your laptop or local cluster with your test datasets.
Create a sample config.json file.
Create main that parses config.json and passes it to your algorithm.
Publish it as public github repo.
Register your App on Brainlife. During this step, you can define what parameters and input file(s) should be made available to your App via config.json.
Contact resource administrators and ask them to enable your App (more below).

examples:
https://github.com/BrainlifeMEEG/app-ICA-apply/tree/master
Datatype: https://brainlife.io/app/63358285db978c7991a30e5b

References:
https://github.com/brainlife/abcd-spec
https://brainlife.io/docs/apps/introduction/
https://brainlife.io/docs/user/datatypes/
https://brainlife.io/docs/apps/register/
