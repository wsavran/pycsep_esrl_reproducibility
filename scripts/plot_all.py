"""
 Executes the following Python scripts to recreate figures from Savran et al.
  - pyCSEP: A Python Toolkit for Earthquake Forecast developers.
  Figure 1 and Figure 8 are not generated programatically, and are not included in the output from this script.

 This script can be executed in a stand-alone mode, but will require that the data files
 (10.5281/zenodo.5717419) are downloaded and extracted into the top-level directory of the
 reproducibility package. This script should be executed automatically when the Docker container
 containing the pyCSEP environment is created.

 Scripts executed :

     1. plot_Figure2.py
         Inputs:
             - '../forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat'
             - '../forecasts/bird_liu.neokinema-fromXML.dat'
             - '../forecasts/ebel.aftershock.corrected-fromXML.dat'
             - '../data/evaluation_catalog_zechar2013_merge.txt'
             - '../data/SRL_2018031_esupp_Table_S1.txt'
             - '../forecasts/lombardi.DBM.italy.5yr.2010-01-01.dat'
             - '../forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat'
             - '../forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
         Outputs:
             - '../figures/figure2.png'

     2. plot_Figure3.py
         Inputs:
             - '../forecasts/ucerf3_forecast/results_complete.bin.gz'
             - '../forecasts/ucerf3_forecast/config.json'
             - '../forecasts/ucerf3_forecast/m71_event.json'
         Outputs:
             - '../figures/figure3.png'

     3. plot_Figure4.py
         Inputs:
             - '../forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat'
             - '../forecasts/bird_liu.neokinema-fromXML.dat'
             - '../forecasts/ebel.aftershock.corrected-fromXML.dat'
             - '../data/evaluation_catalog_zechar2013_merge.txt'
             - '../forecasts/lombardi.DBM.italy.5yr.2010-01-01.dat'
             - '../forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat'
             - '../forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
         Outputs:
             - '../figures/figure4.png'

     4. plot_Figure5.py
         Inputs:
             - '../forecasts/ucerf3_forecast/results_complete.bin.gz'
             - '../forecasts/ucerf3_forecast/config.json'
             - '../forecasts/ucerf3_forecast/m71_event.json'
         Outputs:
             - '../figures/figure5a.png'
             - '../figures/figure5b.png'
             - '../figures/figure5c.png'

     5. plot_Figure6.py
         Inputs:
             - '../forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat'
             - '../forecasts/bird_liu.neokinema-fromXML.dat'
             - '../forecasts/ebel.aftershock.corrected-fromXML.dat'
             - '../data/evaluation_catalog_zechar2013_merge.txt'
             - '../forecasts/lombardi.DBM.italy.5yr.2010-01-01.dat'
             - '../forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat'
             - '../forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
         Outputs:
             - '../figures/figure6.png'

     6. plot_Figure7.py
         Inputs:
             - '../forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat'
             - '../forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
         Outputs:
             - '../figures/figure7.png'
"""

import os

import plot_figure2
import plot_figure3
import plot_figure4
import plot_figure5
import plot_figure6
import plot_figure7

def verify_file_manifest():
    """ Checks directories for data and forecasts to determine which version of the reproducibility package to run.

        Returns:
            out (str): 'full' or 'light'
    """

    # Expected files for the 'full' and 'light' versions, full is light + full
    file_manifest = {
        'full': [
            '../forecasts/config.json',
            '../forecasts/m71_event.json',
            '../forecasts/results_complete.bin.gz'
        ],
        'light': [
            '../data/evaluation_catalog_zechar2013_merge.txt',
            '../data/SRL_2018031_esupp_Table_S1.txt',
            '../forecasts/bird_liu.neokinema-fromXML.dat',
            '../forecasts/ebel.aftershock.corrected-fromXML.dat',
            '../forecasts/helmstetter_et_al.hkj.aftershock-fromXML.dat',
            '../forecasts/lombardi.DBM.italy.5yr.2010-01-01.dat',
            '../forecasts/meletti.MPS04.italy.5yr.2010-01-01.dat',
            '../forecasts/werner.HiResSmoSeis-m1.italy.5yr.2010-01-01.dat'
        ]
    }

    print('Locating necessary files to recreate figures.')
    light = True
    full = True
    for fpath in file_manifest['light']:
        if not os.path.exists(fpath):
            print(fpath)
            light = False
    for fpath in file_manifest['full']:
        if not os.path.exists(fpath):
            print(fpath)
            full = False
    # determine which version to run
    if light and full:
        output = 'full'
        print('Found all files, running full version of reproducibility package')
    elif light:
        output = 'light'
        print('Missing UCERF3-ETAS forecasts, running lightweight version of reproducibility package')
    else:
        raise FileNotFoundError('Missing files unable to run reproducibility package. '
                                'Try re-downloading from Zenodo. Contact wsavran [at] usc.edu for assistance.')
    return output


def main(version):

    print(f'\n\nRunning {version} version of the reproducibility package. See README.md for more information.')
    print('=========================================================================================')

    print('')
    print('Generating Fig. 2')
    print('=================')
    plot_figure2.main()

    if ver == 'full':
        print('')
        print('Generating Fig. 3')
        print('=================')
        plot_figure3.main()
    else:
        print("Skipping Fig. 3. See README for more information.")

    print('')
    print('Generating Fig. 4')
    print('=================')
    plot_figure4.main()

    if ver == 'full':
        print('')
        print('Generating Fig. 5')
        print('=================')
        plot_figure5.main()
    else:
        print("Skipping Fig. 5. See README for more information.")

    print('')
    print('Generating Fig. 6')
    print('=================')
    plot_figure6.main()

    print('')
    print('Generating Fig. 7')
    print('=================')
    plot_figure7.main()


if __name__ == "__main__":
    ver = verify_file_manifest()
    main(ver)
