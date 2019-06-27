FROM continuumio/miniconda3
MAINTAINER Lorenzo Riches "lo.riches@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN conda create -n test-environment -c conda-forge python=3 pip gdal
RUN echo "source activate test-environment" > ~/.bashrc
ENV PATH /opt/conda/envs/test-environment/bin:$PATH
ENV GDAL_DATA /usr/share/gdal/2.2/
RUN conda install Fiona
RUN conda install Flask
RUN conda install -c conda-forge rasterstats
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]
CMD ["flask_api.py"]
