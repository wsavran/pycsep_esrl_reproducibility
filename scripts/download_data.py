import os
import sys
import requests
import hashlib


def check_hash(filename, checksum):
    algorithm, value = checksum.split(':')
    if not os.path.exists(filename):
        return value, 'invalid'
    h = hashlib.new(algorithm)
    with open(filename, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            h.update(data)
    digest = h.hexdigest()
    return value, digest

def download_file(url, filename):
    progress_bar_length = 72
    block_size = 1024
    r = requests.get(url, stream=True)
    total_size = int(r.headers.get('content-length'))
    download_size = 0
    print(f'Downloading file with size of {total_size / block_size:.3f} kB')
    with open(filename, 'wb') as f:
        for data in r.iter_content(chunk_size=block_size):
            download_size += len(data)
            f.write(data)
            # for progress bar
            progress = int(progress_bar_length*download_size/total_size)
            sys.stdout.write('\r[{}{}] {:.1f}%'.format('█'*progress, '.' * (progress_bar_length-progress),
                100*download_size/total_size))
            sys.stdout.flush()
    sys.stdout.write('\n')


# this can be found in the DOI for the Zenodo record
record_id = sys.argv[1]
# download to top-level directory
output_dir = './'

# Used for progress bar
block_size = 1024

# grab the urls and filenames and checksums 
r = requests.get(f"https://zenodo.org/api/records/{record_id}")
download_urls = [f['links']['self'] for f in r.json()['files']]
filenames = [(f['key'], f['checksum']) for f in r.json()['files']]

# download and verify checksums
for (fname, checksum), url in zip(filenames, download_urls):
    full_path = os.path.join(output_dir, fname) 
    if os.path.exists(full_path):
        print('Found file, checking checksum to see if download is required.')
        value, digest = check_hash(full_path, checksum)
        if value != digest:
            print(f"Downloading {fname} from Zenodo...")
            download_file(url, full_path)
    else:
        print(f"Downloading {fname} from Zenodo...")
        download_file(url, full_path)
    value, digest = check_hash(full_path, checksum)
    if value != digest:
        print("Checksum does not match.")
