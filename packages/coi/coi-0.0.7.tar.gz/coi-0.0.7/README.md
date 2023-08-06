[![PyPi version](https://img.shields.io/pypi/v/coi.svg?color=blue)](https://pypi.org/project/coi/)
[![licence](https://img.shields.io/pypi/l/coi.svg)](https://github.com/nosarthur/coi/blob/master/LICENSE)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/coi.svg)](https://pypistats.org/packages/coi)



# coi: manage shell script templates for reuse

I often improvise the same (boring) bash scripts over and over again.
This is my solution to cut the repetitive work.

This command-line tool can

1. manage (CRUD) templates
1. run template command with substitutions
2. keep track of commands run in each folder for later reference


## examples

Three examples are in order here.
They are all small frequent `for` loops.
One could alternatively define shell functions for them.

In the first example, I need to delete jobs with some key word. The varying part
is `BIHYEW10`.

```
for x in `qstat -u nosarthur |grep BIHYEW10 |awk '{print $1}'`; do
  qdel $x
done
```

With `coi` set up, I can simply do

```
coi run -i BIHYEW10
```

The corresponding template is

```
for x in `qstat -u nosarthur |grep $i |awk '{print $$1}'`; do
  qdel $$x
done
```

Note that it's simply the Python
[template strings](https://docs.python.org/3/library/string.html#template-strings ]).

In the second example, I often need to process data with a common directory
pattern, e.g., `ABC_5/ABC-out.cms`:

```bash
for dname in *_5/; do python3 process.py $dname${dname%/}-out.cms; done
```

Here the variable parts are

1. folder name pattern: `*_5/`
2. command: `$ABIN/generate.py`


After saving a template, we can run
```
coi run -i "*_5" -c "python3 process.py" some-path
```

and the template is

```
cd $path
for dname in $i; do
  $c $$dname$${dname%/}-out.cms
done
```
where `some-path` will substitute `$path`.


In the third example, I often want to know how many jobs are done in many folders,
and the criteria of 'done' may vary.

Suppose the folder structure is as follows
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

## commands

- `run` command
    - `coi run -i <i> -c <c> -o <o> -t <name> <path>`: run template command `<name>`
- `templates` command
    - `coi templates add <name>`: create a new template called `<name>`
    - `coi templates cp <name> <new-name>`: copy `<name>` to a new template called `<new-name>`
    - `coi templates ll <name>`: show content of template `<name>`
    - `coi templates ls <name>`: show path of template `<name>`; You can pass it
      to your favorate editor.
    - `coi templates rm <name>`: delete template `<name>`
    - `coi templates set <name>`: set template `<name>` as default template

The `run` command takes up to 3 parameters `c`, 'o', and 'i'. If template `-t`
is not specified, default template is used. If `<path>` is omitted, current
working directory is used.

## customization

User defined templates are saved/searched in `$XDG_CONFIG_HOME/coi`
(most likely `~/.config/coi/`).

## other tune-ups

```
alias coir='coi run'
alias coit='coi template'
```
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
