FROM CENTOS
RUN mkdir /root/.kube
COPY kube/config /root/.kube/config
RUN pip install -r requirements.txt
