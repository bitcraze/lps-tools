# Common options for setup.py and cx_setup.py

setup_options = {
    "name": "lpstools",
    "version": "0.1",
    "description": "Loco positioning tools",
    "packages": ['lpstools', 'dfuse'],
    "url": 'http://github.com/bitcraze/lps-tools',
    "author": 'Bitcraze',
    "author_email": 'contact@bitcraze.io',
    "license": 'MIT',
    "install_requires": ["pyusb~=1.0.2", "pyserial~=3.4"],
}
