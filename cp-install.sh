for x in scripts/*;do
    chmod +x $x
    cp $x /usr/local/bin/
done

mkdir /usr/local/notebook
