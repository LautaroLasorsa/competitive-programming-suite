cd scripts/

CP="/home/competitive-programming"

mkdir -p $CP/scripts
mkdir -p $CP/notebook
touch $CP/notebook/template.py 
touch $CP/notebook/template.cpp


for x in *.sh;do
    chmod +x $x
    cp $x "$CP/scripts/${x%.*}"
done

export PATH="PATH:$CP/scripts"