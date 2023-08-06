# coi: manage shell script templates for reuse

I often improvise bash scripts and later regret not saving them.
This tool manages shell script templates for reuse.

1. run shell command templates with substitutions
2. keep track of commands run in each folder for later reference
1. store common templates

For example, the variable parts of the following batch execution may be

1. folder name pattern: `*_5/`
2. command: `$ABIN/generate.py`

```bash
for dname in *_5/; do python3 $ABIN/generate.py $dname${dname%/}-out.cms; done
```

After saving a template, we can rerun this command at current working directory with
```
coi run -i "*_5" -c "python3 $ABIN/generate.py"
```

## commands

- `run` sub command
- `templates` sub command
    - `coi templates add <name>`
    - `coi templates add <name> -t <template-file>`
    - `coi templates edit <name>`
    - `coi templates ls`
    - `coi templates rm <name>`
    - `coi templates set <name>`
    - `coi templates show <name>`

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
coi -c "wc -l" \
    -o "ll *.output" \
    -i "ll *.input" \
    jobs-folder
```

```bash
sub1 (1 / 2)
sub2 (0 / 2)
sub3 (2 / 2)
sub4 (1 / 1)
```

## customization

Python [template strings](https://docs.python.org/3/library/string.html#template-strings ])

## design

Essentially this is a tool for shell script templating, with up to 3 substitutions.

- templates are saved in
  - system folder: default
  - XDG/coi/templates/: user defined
  - the user defined templates shadow default ones if name clashes
- when a command is run once in `path`, save `path/.coi/1.json` where the keys
  are c, o, i, and template name

TODO:
- default template
- state machine when running main: q, r (always show the shell command to be run)

### integration with fzf

If json files exists in a path, we can let the user pick with fzf
