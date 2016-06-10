# 1. LaTeX Framework for Exercises

## 1.1 Requirements

1. Python 3 to run `python3 Pytex.py` and either
2. Docker installed to compile latex inside a container or
3. a native latex installation with the `latexmk` compiler


## 1.2 Execution

```[bash]
usage: PyTex.py [-h] [-c] [-d] [-cn CONTAINERNAME] [term] number [number ...]

Install latexmk or Docker and make sure it's in your path, before you start
the Builder with the following parameter

positional arguments:
  number                Input the exercise number(s)

optional arguments:
  -h, --help            show this help message and exit
  -j, --json            To parse a JSON file from stdin
  -c, --clean           Compile and clean temporary files
  -d, --dockerized      Perform LaTeX compilation inside a container
  -cn CONTAINERNAME, --containerName CONTAINERNAME
                        Specify a custom containerName, if docker is enabled
```

- If you want to run the latex compiler inside a container use `-d`. Moreover you may specify a specific name for the container with `-cn`
- If you compile latex natively on your host os, you can cleanup all files by selecting `-c`

## 1.3 Specific Information

In the file `metainfo.csv` you can specify the variables that change for each compiled pdf.
The header must correspond to the names used in `template.tex`, where the csv information is parsed into.

## 1.4 Templates

**Remember:** Template changes modify **all** compiled examples.

To modify the latex layout of the example, use the following files:

- In `template.tex` you can specify all variables needed for the assignments
- In the `ExampleTemplate` your LaTeX Layout for all compiled files need to be specified
