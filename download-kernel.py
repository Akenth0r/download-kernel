import argparse
import requests
from tqdm import tqdm

parser = argparse.ArgumentParser("Kernel Downloader", description="Tries to download the kernel version")
parser.add_argument("version", type=str, help="x.x or x.x.x")

kernel_sources = [
    "https://cdn.kernel.org/pub/linux/kernel/v{}.x/linux-{}.tar.xz",
    "https://github.com/torvalds/linux/archive/refs/tags/v{}.tar.gz"
]

def _progress_bar(resp: requests.Response, fname: str, chunk_size=1024)->bool:
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)

def _download_from_source(url):
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        _progress_bar(resp, url.split(sep="/")[-1])
        return True
    
    return False
    
def try_download(version: str)->bool:
    if "-rc" in version:
        url = kernel_sources[1].format(version)
        if True == _download_from_source(url):
            return True

        print("[+] Error: not found")

        return False
    
    ver = version.split(sep=".")
    if len(ver) < 2:
        print("[+] Error: write version in x.x, x.x.x or x.x-rcx format")
        return False

    # Trying first source
    url = kernel_sources[0].format(ver[0], version)
    if True == _download_from_source(url):
        return True
    
    print("[+] Not found")
    print("[+] Trying another source...")
    url = kernel_sources[1].format(version)
    if True == _download_from_source(url):
        return True
    
    print(f"[+] Error: Linux Kernel version {version} was not found")
    return False

if __name__ == "__main__":
    args = parser.parse_args()
    print("[+] Trying to download the kernel...")
    try_download(args.version)