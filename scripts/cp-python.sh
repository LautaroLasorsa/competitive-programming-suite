cp $1.py $1.print; 
for x in $1*.in; do 
    echo "$(tput setaf 2)$(tput bold)ARCHIVO: $x" 
    echo "$(tput setaf 2)$(tput bold)$(cat $x)"
    echo "$(tput sgr0)$(tput bold)============"
    echo "$(tput setaf 1)$(tput bold)$(python3 "$1".py < $x)$(tput sgr0)"
    echo "$(tput bold)============"
done | tee -a $1.print

sed -i $'s/\x1b\\[[0-9;]*[mGK]//g' "$1.print"