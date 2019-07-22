# !/bin/bash -x

# usage: mjob_run.sh 6
# first param is the replicate number
num_repl=$1
repl_name=imp_model_$1
echo "replicates number:"$repl_name
#set defaults for cores and replicates
export cores="1"
export replicates="1"

#sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' ConfigImp.yaml > param.sh
cat ConfigImp.yaml | grep -e cores -e replicates | sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' | sed -e 's/ //g' | sed -e 's/^/export /g' > param.sh
chmod 755 param.sh
#source the env vars from param.sh as these are exported
. param.sh
echo "cores:"$cores
echo "replicates:"$replicates 
# from imp_model folder we clone the driver scripts
cd ../
cp -R imp_model $repl_name
cd $repl_name
sbatch run_imp.slurm
#squeue -u username
#scancel jobID



