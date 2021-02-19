FROM alpine:3.12

ENV ANSIBLE_HOSTS=/ansible/hosts

RUN apk --update add py-pip ansible bash ca-certificates \
 && pip install --upgrade pip boto boto3 \
 && update-ca-certificates 2&>1 > /dev/null

COPY ansible /ansible
COPY sh/* /usr/local/bin/
