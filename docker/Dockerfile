FROM tiangolo/uvicorn-gunicorn:python3.9
WORKDIR /usr/src/
COPY requirements.txt /usr/src/

# Using pip:
RUN python3.9 -m pip install -r requirements.txt

RUN echo "\nforce_color_prompt=yes\n" >> /root/.bashrc
RUN echo "\nalias python=python3.9\n" >> /root/.bashrc


ADD . /usr/src/
WORKDIR /usr/src/
EXPOSE 8000
RUN python setup.py install

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

# CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8080","smartlayerscore.app:app" ]