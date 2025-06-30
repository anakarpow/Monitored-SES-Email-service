export BUCKET_INPUT="test=bucket"
export local="running local"
export PYTHONPATH='../shared/python'


echo 'Environemnt variables ready'

## starting backgound services for testing and deployment

sudo service docker start
echo 'Docker started'

