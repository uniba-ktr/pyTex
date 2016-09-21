FROM unibaktr/latex:python
MAINTAINER Marcel Grossmann <whatever4711@gmail.com>

COPY PyTex.py ${dir}/
ADD pythonlib ${dir}/pythonlib
COPY template.tex ${dir}/
ADD ExampleTemplate ${dir}/ExampleTemplate
WORKDIR ${dir}

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["pytex/PyTex.py", "-h"]
