# download-kernel
During my daily routine of reproducing exploits, I've grown tired of the time it takes to download the appropriate Linux kernel version, so I wrote this script.
### Usage
First install dependencies:
```sh
pip install -r requirements.txt
```
Then you can use it like so:
```sh
# Specific kernel version
python ./download-kernel.py 6.5.3
# Or release candidate
python ./download-kernel.py 6.5-rc3
# v6.5-rc3.tar.gz: 184MiB [00:34, 4.54MiB/s] 
```
Notice that kernel version should be in x.x, x.x.x or x.x-rcx format 
