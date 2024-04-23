
export BUCKET_INPUT='vw-lambda-reporting-output'
export local="running local"
export GIT_DISCOVERY_ACROSS_FILESYSTEM=1
export branch=$(git symbolic-ref --short HEAD)

if [ $branch = DEV ]
then
    export ENV='DEV'
elif [ $branch = main ]
then
    export ENV='MAIN'
else
    export ENV=$branch
fi

echo 'Environemnt variables ready'

## starting backgound services

sudo service docker start
echo 'Docker started'

sudo service postgresql start
sudo -u postgres psql -c \\q
echo 'PSQL started'
