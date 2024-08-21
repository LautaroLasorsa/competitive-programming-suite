cd "$CP"

notebooks=(
    "icpc-team-notebook-el-vasito"
    "notebook-unlam-python"
)

for notebook in "${notebooks[@]}";do
    if [ -d "$notebook" ]; then
        cd "$notebook"
        git pull
        cd ..
    fi
done
    



