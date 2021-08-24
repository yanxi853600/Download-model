FROM yanxilincc/pytorch_cu101:latest
LABEL maintainer="yanxilincc"
COPY . /usr/src/pytorch_yolov3
WORKDIR /usr/src/pytorch_yolov3
ENTRYPOINT [ "python" ]
CMD [ "./download_model.py" ]
