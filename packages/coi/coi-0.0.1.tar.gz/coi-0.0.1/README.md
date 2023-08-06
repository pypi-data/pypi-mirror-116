# coi: see output/input status of all sub-folders

This tool batch run 2 shell commands on all sub-folders and display the outputs
succinctly.

## example

Suppose the folder structure
```
jobs-folder
├── sub1
│   ├── 1.input
│   ├── 1.output
│   └── 2.input
├── sub2
│   ├── 1.input
│   └── 2.input
├── sub3
│   ├── 1.input
│   ├── 1.output
│   ├── 2.input
│   └── 2.output
└── sub4
    ├── 1.input
    └── 1.output
```

```bash
coi -o ll *.output
coi -i ll *.input
coi jobs-folder
```

```bash
sub1 (1 / 2)
sub2 (0 / 2)
sub3 (2 / 2)
sub4 (1 / 1)
```
