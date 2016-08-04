FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------


RUN \
    mkdir -p /kb/module && \
    cd /kb/module && \
    git clone https://github.com/msneddon/data_api && \
    cd data_api && \
    git checkout dab1ce56f4d734fbf042a7b2299d0bb0de7c70cc && \
    cd /kb/module && \
    mkdir lib/ && \
    cp -a data_api/lib/doekbase lib/

RUN pip install -r //kb/module/data_api/requirements.txt

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
