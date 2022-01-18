import os
import sys
import shutil
import requests
import hashlib
import argparse

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
    try:
        total_size = int(r.headers.get('content-length'))
    except TypeError:
        total_size = None
    download_size = 0
    if total_size:
        print(f'Downloading file with size of {total_size / block_size:.3f} kB')
    else:
        print(f'Downloading file with unknown size')
    with open(filename, 'wb') as f:
        for data in r.iter_content(chunk_size=block_size):
            download_size += len(data)
            f.write(data)
            # for progress bar
            if total_size:
                progress = int(progress_bar_length*download_size/total_size)
                sys.stdout.write('\r[{}{}] {:.1f}%'.format('█'*progress, '.' * (progress_bar_length-progress),
                    100*download_size/total_size))
                sys.stdout.flush()
        sys.stdout.write('\n')


def main():

    file_manifest = {
        'full': [
            'evaluation_catalog.json',
            'evaluation_catalog_zechar2013_merge.txt',
            'SRL_2018031_esupp_Table_S1.txt',
            'bird_liu.neokinema-fromXML.dat',
            'ebel.aftershock.corrected-fromXML.dat',
            'helmstetter_et_al.hkj.aftershock-fromXML.dat',
            'lombardi.DBM.italy.5yr.2010-01-01.dat',
            'meletti.MPS04.italy.5yr.2010-01-01.dat',
            'werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat',
            'config.json',
            'm71_event.json',
            'results_complete.bin.gz'
        ], 
        'light': [
            'evaluation_catalog_zechar2013_merge.txt',
            'SRL_2018031_esupp_Table_S1.txt',
            'bird_liu.neokinema-fromXML.dat',
            'ebel.aftershock.corrected-fromXML.dat',
            'helmstetter_et_al.hkj.aftershock-fromXML.dat',
            'lombardi.DBM.italy.5yr.2010-01-01.dat',
            'meletti.MPS04.italy.5yr.2010-01-01.dat',
            'werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
        ]
    }   

    dir_map = {
        'evaluation_catalog.json': './data',
        'evaluation_catalog_zechar2013_merge.txt': './data',
        'SRL_2018031_esupp_Table_S1.txt': './data',
        'bird_liu.neokinema-fromXML.dat': './forecasts',
        'ebel.aftershock.corrected-fromXML.dat': './forecasts',
        'helmstetter_et_al.hkj.aftershock-fromXML.dat': './forecasts',
        'lombardi.DBM.italy.5yr.2010-01-01.dat': './forecasts',
        'meletti.MPS04.italy.5yr.2010-01-01.dat': './forecasts',
        'werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat': './forecasts',
        'config.json': './forecasts',
        'm71_event.json': './forecasts',
        'results_complete.bin.gz': './forecasts'
    }
    
    # parse command line arguments
    parser = argparse.ArgumentParser(
        description="Download data for pyCSEP: A Software Toolkit for Earthquake Forecast Developers"
    )
    parser.add_argument("record_id", help="record id associated with zenodo data")
    parser.add_argument("--full", help="download full version of reproducibility package. default: false", action='store_true')
    args = parser.parse_args()

    # This can be found in the DOI for the Zenodo record
    record_id = args.record_id

    # Determine what to download from command line
    download_type = 'full' if args.full else 'light'

    # Download to data directory
    output_dir = './'

    # Used for progress bar
    block_size = 1024

    # Grab the urls and filenames and checksums 
    r = requests.get(f"https://zenodo.org/api/records/{record_id}")
    download_urls = [f['links']['self'] for f in r.json()['files']]
    filenames = [(f['key'], f['checksum']) for f in r.json()['files']]

    # Download and verify checksums
    for (fname, checksum), url in zip(filenames, download_urls):
        if not fname in file_manifest[download_type]:
            continue
        # Make directory for file, fail silently if directory exists
        try:
            os.makedirs(dir_map[fname])
        except FileExistsError:
            pass
        full_path = os.path.join(dir_map[fname], fname) 
        if os.path.exists(full_path):
            print(f'Found file {fname}, checking checksum to see if download is required.')
            value, digest = check_hash(full_path, checksum)
            if value != digest:
                print(f"Checksum is different: re-downloading {fname} from Zenodo...")
                download_file(url, full_path)
        else:
            print(f"Downloading {fname} from Zenodo...")
            download_file(url, full_path)
        value, digest = check_hash(full_path, checksum)
        if value != digest:
            print("Error: Checksum does not match. Please contact wsavran [at] usc.edu for assistance.")
            sys.exit(-1)

if __name__ == "__main__":
    main()
