!/bin/bash

aws lambda create-function \
--function-name LearnSystemsFromQuizlet  \
--region us-east-1 \
--zip-file fileb://chainsnake.zip \
--role arn:aws:iam::360629931041:role/edu-17 \
--handler app.handler \
--runtime python3.6  \
--timeout 30 \
--memory-size 1024