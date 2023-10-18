# export BUCKET_INPUT_BILLING="vwag-dpp-billing-detailed-billing-reports"
# export BUCKET_INPUT_MANUAL="vw-lambda-reporting-manual-input"
# export BUCKET_OUTPUT="test-dev-automation"
# export BUCKET_MERCUR_OUTPUT="consumer-bucket-471685057907"
# export BUCKET_MERCUR_OUTPUT_TEST="usage-testing"
export BUCKET_INPUT='vw-lambda-reporting-output'
# export BUCKET_INPUT_METERING="consumer-bucket-471685057907"
# export BUCKET_INPUT_METERING_LOCAL="vw-lambda-reporting-output"
# export SECRETS_MANAGER="arn:aws:secretsmanager:eu-west-1:471685057907:secret:dpp-dco-CAST-VT5LkZ"
export local="running local"
export GIT_DISCOVERY_ACROSS_FILESYSTEM=1
export branch=$(git symbolic-ref --short HEAD)
# export BUCKET_CROSS_ACCOUNT="dpp-dco-metering-cross-account"

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
