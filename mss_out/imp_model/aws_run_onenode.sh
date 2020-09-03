#/usr/bin/bash -x
runnum=$1
# pip install awscli --upgrade --user

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
    
	sudo cp -R ../imp_model ../$repl_name$repljob
    cd ../$repl_name$repljob
	

	# number of cores on instance determines param for -N 16
	#nohup /shared/anaconda/bin/mpiexec -N $cores /shared/anaconda/bin/python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml >/shared/imp/danhells/imp_model$runnum/trace.log 2>&1 &
	# we can only run this in series and not in parallel on aws. Additional instances need to be launched to run replicate job runs in parallel
	/shared/anaconda/bin/mpiexec -N $cores /shared/anaconda/bin/python prep_hyperp_imp_v2ux.py --count=1 --name=DemoImpModel --config=ConfigImp.yaml > trace.log 2>&1 &

    cd ../imp_model

done





# archive
# tar -cvzf imp_model18.tgz /shared/imp/danhells/imp_model18
# aws s3 cp imp_model18.tgz s3://pcluster-resource
