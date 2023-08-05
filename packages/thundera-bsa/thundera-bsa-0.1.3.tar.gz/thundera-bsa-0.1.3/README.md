# ThunderaBSA-Cli

ThunderaBSA it's a Binary Static Analysis tool that infers what Open Source packages are present on binary apps by searching for "symbols."

A "symbol" for ThunderaBSA it's the representation of a file property (file name, file path, folders names) or content (symtree, class names, function names, variable names).

ThunderaBSA doesn't perform reverse engineering over the software. Instead, it extracts the symbols offered by the file's metadata, the same way as the operative system scan for file mime-types or file sizes.

The CLI (ThunderaBSA CLI) it's one of the three main components of the project. The CLI tool scan files to extract symbols and export the "symbols" to a report file. The reports can be used later by other components to perform the symbol matching offline.

## Installation
ThunderaBSA-CLI requires a few tools to be available on your system:

$ sudo apt install python3-pip

$ sudo apt install universal-ctags elfutils binutils libimage-exiftool-perl

$ pip3 install thundera-bsa
