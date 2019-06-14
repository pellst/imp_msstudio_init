#!/usr/bin/python3

import os, subprocess, platform, argparse

# default paths to anaconda and data roots
ANACONDA_DIR = os.path.join("C:\\", "Apps", "Anaconda3") if platform.system() == "Windows" else os.path.join("~", "anaconda3")
DEFAULT_COUNT, DEFAULT_NAME, DEFAULT_CONFIG = 1, "DemoImpModel", "ConfigImp.yaml"

# parse args for path replacements & args for the job start command execution
parser = argparse.ArgumentParser()
parser.add_argument("--anaconda_dir", type=str, help="path to the root directory of your Anaconda installation")
parser.add_argument("--count", type=int, help="count variable for IMP")
parser.add_argument("--name", type=str, help="Name of job")
parser.add_argument("--config", type=str, help="config file name (within imp_model directory)")
parser.add_argument("--output_file", type=str, help="file to redirect imp script execution into, rather than stdout")
args = parser.parse_args()

if args.anaconda_dir is not None:
	ANACONDA_DIR = args.anaconda_dir

outfile = args.output_file if args.output_file is not None else "prep_hyperp_imp_v2_trace.txt"
with open(outfile, 'w') as f:
	subprocess.run(
		"{0} prep_hyperp_imp_v2.py --count={1} --name={2} --config={3}".format(
			os.path.join(ANACONDA_DIR, "python.exe"),
			args.count  if args.count  is not None else DEFAULT_COUNT,
			args.name   if args.name   is not None else DEFAULT_NAME,
			args.config if args.config is not None else DEFAULT_CONFIG,
		),
		stdout=f,
		stderr=(subprocess.STDOUT)
	)