if [ "$2" = "" ] || [ "$2" = "build" ]; then 
    g++ -Wall -Wextra -Wshadow -Wconversion -D_GLIBCXX_DEBUG -std=c++2a -g -ggdb3 -o $1 $1.cpp -DACMTUYO
fi 

if [ "$2" = "" ] || [ "$2" = "run" ]; then 
    cp $1.cpp $1.print; 
    for x in $1*.in; do 
        echo "$(tput setaf 2)$(tput bold)ARCHIVO: $x" 
        echo "$(tput setaf 2)$(tput bold)$(cat "$x")"
        echo "$(tput sgr0)$(tput bold)============"
        echo "$(tput setaf 1)$(tput bold)$(./"$1" < "$x")$(tput sgr0)"
        echo "$(tput bold)============"
    done | tee -a $1.print
fi

sed -i $'s/\x1b\\[[0-9;]*[mGK]//g' "$1.print"