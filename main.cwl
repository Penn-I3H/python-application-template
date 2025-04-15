cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python3.13", "main.py"]

requirements:
  DockerRequirement:
    dockerPull: python:3.13.1
  InitialWorkDirRequirement:
    listing:
      - entryname: main.py
        entry: $(inputs.script)
      - entryname: data/input
        entry: $(inputs.input_dir)
      - entryname: data/output
        entry: "$(null)"
        writable: true
  EnvVarRequirement:
    envDef:
      INPUT_DIR: "data/input"
      OUTPUT_DIR: "data/output"

inputs:
  script:
    type: File
    doc: "The main Python script"

  input_dir:
    type: Directory
    doc: "Input directory"

outputs:
  output_data:
    type: Directory
    outputBinding:
      glob: data/output