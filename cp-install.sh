cd scripts/

for x in *.sh;do
    chmod +x $x
    cp $x "/usr/local/bin/${x%.*}"
done

mkdir -p /usr/local/competitive-programming/notebook
touch /usr/local/competitive-programming/notebook/template.py 
touch /usr/local/competitive-programming/notebook/template.cpp
