# !/bin/bash -x

# usage: mjob_run.sh 6
# first param is the replicate number
num_repl=$1
repl_name=imp_model_$1
#repl_job_count=2
echo "replicates number:"$repl_name
#set defaults for cores and replicates
export cores="1"
#cd ../
#cp -R imp_model imp_model_2
#cp -R imp_model imp_model_3
#sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' ConfigImp.yaml > param.sh
cat ConfigImp.yaml | grep -e cores | sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' | sed -e 's/ //g' | sed -e 's/^/export /g' > param.sh
chmod 755 param.sh
#source the env vars from param.sh as these are exported
. param.sh
cat ConfigImp.yaml | grep -e replicates | sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' | sed -e 's/ //g' | sed -e 's/^/export /g' > param.sh
chmod 755 param.sh
#source the env vars from param.sh as these are exported
. param.sh
echo "cores:"$cores
echo "replicate job count:" $replicates
# construct slurm file
cat << EOF > param_prep.slurm
#!/bin/bash
# example slurm job script setup to run on for example Cedar
#SBATCH --job-name=SLURM_imp
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=0-01:00:00
#SBATCH --account=def-dschriem


mpiexec -n $cores python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml
#srun python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml

echo "Job Finished"
EOF
# nix line ending and not wnd
sed -e "s/\r//" param_prep.slurm > run_imp.slurm
#clean up intermedate files
rm -rf param_prep.slurm
rm -rf param.sh
# from imp_model folder we clone the driver scripts
# replicates job count repeat clone incrementing repl_name by 1 each time
#repl_job_count=2
START=1
END=`echo -n $replicates | tr -d '\r' `
i=$START
for (( repljob=$START; repljob<=$END; repljob++))
#while [[ $i -le $END ]]
do
    #echo -n "$i "
    #((i = i+1  ))
    #sleep 1
    echo $repl_name$repljob

    #cd ../
    cp -R ../imp_model ../$repl_name$repljob
    #cd $repl_name$repljob
    #sbatch run_imp.slurm
    #squeue -u tpells
    #cd ../
done


