FROM ubuntu:20.04

COPY /volatility2 /root/volatility2
COPY /volatility3 /root/volatility3

WORKDIR /root
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
	&& apt update --no-install-recommends \
    && apt install -y curl vim unzip openssh-server python3-pip python \
    && sed -i 's/\#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config \
    && sed -i 's/\#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config \
    && echo 'root:root' | chpasswd \
    && python2 /root/volatility2/get-pip.py \
    && python /root/volatility2/distorm3-master/setup.py install \
    && pip2 install -i https://pypi.tuna.tsinghua.edu.cn/simple simplejson \
       construct pycryptodome \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /root/volatility3/requirements-minimal.txt \
    && mkdir /run/sshd

CMD ["/bin/bash"]
