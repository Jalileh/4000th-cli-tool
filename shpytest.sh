#!/bin/bash

shellRequestCD=$("./run.py")
export pymation_request_cd=value

output=$(py ./run.py)
eval "$output"

# Check if the variable was set correctly
echo $pymation_request_cd
# git.sh "kill" "bash.exe" "--check"
