# covidsim
This project builds on the functionality of the excellent epydemic package to run multiple simulation experiments aimed at understanding Covid-19.  It extends the ComponentModel process from that project and adds a plugin structure so that the simulation behavior and data gathered by be customized per experiment.  It contains Covid-19 facts from literature, and it contains several specific experiments.

## Getting Started

### Installing

All requirements are listed in the included requirements.txt.

### Running the included experiments.

To run the various included experiments, go to the "Scripts" directory.  Each experiment will have a "run" script and a "report" script.  Edit the run script to specify the parameters you want for the experiment, then run the "report" script to see the graphical output.

All experiment runs are saved by parameter set in the output file which is created in the Scripts directory.  Each time you run a "report" script, it will only show the results for those runs that were done using the parameters that are specified in the "run" script.

## Creating your own experiments.

At the minimum, you will need a experiment class (see the variability_study.py for an example to copy), a "run" and a "report" script (see the examples in the Scripts folder to copy).

## License

This project is licensed under the BSD License - see the LICENSE file for details.

## Acknowledgements

Thanks to the epydemic team for the excellent framework!
