#!/bin/sh

# This script mocks the following scenario:
# 1. Student 'jimbo' logins into account (account will be created if does not exist)
# 2. Student 'jimbo' checks waitlist

curl -i -L -X 'POST' \
  'http://localhost:5400/api/register/?username=jimbo&password=test&roles=1' \
  -H 'accept: application/json' \
  -d '' \

response=$(curl -s -L -X GET "http://localhost:5400/api/verify?username=jimbo&password=test" -H "accept: application/json")

# Extract the access token from the JSON response using grep and awk
token=$(echo "$response" | grep -o '"access_token":"[^"]*' | awk -F ':"' '{print $2}')
printf "\n"
# Check if the token is successfully retrieved
if [ -z "$token" ]; then
  echo "Failed to retrieve the token."
  exit 1
fi

# Attempt to Enroll a Student into a Section that is full
curl -i -L -H "Authorization: Bearer $token" -X POST "http://localhost:5400/api/student/enroll/?section_id=4&id=1"
printf "\n"
curl -i -L -H "Authorization: Bearer $token" -X GET "http://localhost:5400/api/student/check_waitlist/?section_id=4&id=1"
printf "\n"

# Attempt to have student subscribe to webhook
curl -i -L -H "Authorization: Bearer $token" -X POST "http://localhost:5400/api/notify/subscribe/?section_id=4&id=1&email=test@email.com"
printf "\n"

# Remove students from the waitlist to have our student 'jimbo' enroll and be notified
# We are dropping students internally, so we dont have to login as the student
curl -s -L -X PUT "http://localhost:5300/student/drop/?section_id=4&id=15"
# for i in $(seq 2 14); do
#   curl -s -L -X PUT "http://localhost:5300/student/drop/?section_id=4&id=$i"
#   printf "\n"
# done