input_dir=$1
for dirname in $(ls $input_dir); do
	echo "$dirname"
	aws --profile peroxide s3 cp "$input_dir/$dirname" s3://iot-signal-csv/ --recursive
	sleep 20s
done