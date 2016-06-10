FROM unibaktr/dock-tex:python
MAINTAINER Marcel Grossmann <whatever4711@gmail.com>

RUN mkdir -p ${dir}/include
COPY PyTex.py ${dir}/
ADD pythonlib ${dir}/pythonlib
COPY metainfo.csv ${dir}/
COPY template.tex ${dir}/
ADD ExampleTemplate ${dir}/ExampleTemplate
WORKDIR ${dir}

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["pytex/PyTex.py", "-h"]