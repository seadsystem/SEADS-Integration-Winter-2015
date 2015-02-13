# File: filecheck.sh
# Description: checks file for size
# Author: Henry Crute
# 6/30/2014

#starts talking to eagle
<<<<<<< HEAD
#python raineagletalk.py &
=======
python raineagletalk.py &
>>>>>>> 0cde7882074562e88e21430fc8a0e1169191baea

#insert file name and minimum size to compare in bytes
file="sample.txt"
minimumsize=256
while true; do
sleep 15
actualsize=$(wc -c "$file" | cut -f 1 -d ' ')
#compares file size to threshhold
if [ $actualsize -ge $minimumsize ]; then
	#rewrites zero into sample file
	cp sample.txt temp
<<<<<<< HEAD
	cat /dev/null > "$file"
	#sends data
	python client.py
=======
	#sends data
	python client.py
	#removes temporary parsed file that was transferred
	rm temp
	cat /dev/null > "$file"
>>>>>>> 0cde7882074562e88e21430fc8a0e1169191baea
fi
done

