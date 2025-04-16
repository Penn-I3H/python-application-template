cwlVersion: v1.2
class: CommandLineTool

requirements:
  DockerRequirement:
    dockerPull: hackathon/python
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
  output_dir:
    type: Directory
    outputBinding:
      glob: data/output