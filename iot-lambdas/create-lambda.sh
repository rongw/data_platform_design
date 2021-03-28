code_dir=$1

config_file=$code_dir/lambda.config
source $config_file
echo "Use following Lambda config>>>>>>"
cat $config_file
cd $code_dir/code 
zip lambda-code.zip . -r
mv lambda-code.zip ../
cd ..
aws --profile $aws_profile lambda create-function --zip-file fileb://lambda-code.zip --function-name $function_name --role $role_arn --handler $handler --runtime $run_time --timeout $time_out --memory-size $memory
rm lambda-code.zip
