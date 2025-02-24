if [ "$2" = "" ] || [ "$2" = "build" ]; then 
   kotlinc $1.kt -include-runtime -d $1.jar 
fi 

if [ "$2" = "" ] || [ "$2" = "run" ]; then 
    cp $1.kt $1.print; 
    for x in $1*.in; do 
        echo "$(tput setaf 2)$(tput bold)ARCHIVO: $x" 
        echo "$(tput setaf 2)$(tput bold)$(cat "$x")"
        echo "$(tput sgr0)$(tput bold)============"
        echo "$(tput setaf 1)$(tput bold)$(java -jar -ea -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1920m -Xmx1920m $1.jar < "$x" 2>&1)$(tput sgr0)"
        echo "$(tput bold)============"
    done | tee -a $1.print
    sed -i $'s/\x1b\\[[0-9;]*[mGK]//g' "$1.print"
fi