cwlVersion: v1.2
class: CommandLineTool

baseCommand: ["python", "main.py"]

requirements:
  DockerRequirement:
    dockerPull: python:3.11
  InitialWorkDirRequirement:
    listing:
      - entryname: main.py
        entry: $(inputs.script)

inputs:
  script:
    type: File
    inputBinding: {}
    doc: "The main Python script"

  input_dir:
    type: Directory
    inputBinding:
      prefix: "data/input"
      separate: false

  output_dir:
    type: Directory
    inputBinding:
      prefix: "data/output"
      separate: false

outputs:
  output_data:
    type: Directory
    outputBinding:
      glob: data/output
