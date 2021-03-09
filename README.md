


# Set Up and Installation
To install the project locally, git clone the project into any folder. This project required the use of npm to run node, so this must be installed as well.
Use 'npm install' in terminal or on command line to download the required dependencies.

# Running the Server
To run the program, start by running 'npm run start' in command-line. Exit from this and this use 'npm run dev'. This will run the project in your folder of choice.

# Project Architecture
By top-level folder in alphabetical order.

## RNATracker
This folder contains the code required to make initial prediction on the RNA-binding properties of a given sequence.

## PhyloPGM
This folder contains the code required to run PhyloPGM, which combines prediction scores across phylogenetically related sequences.

## phylo_utils
This folder contains utility functions that, given an input BED file, can extract and collect maf files to be used as input to RNA tracker.

## public
This folder contains index.html and the favicon. The browser is first directed here.

## scripts
This folder contains a copy of python scripts, including phyloPGM and phylo_utils, as well as the connector scripts.

## src
This is the source folder for the client and server-side react components.

## toy-data
This folder contains toy-data used in the development of the local version.
