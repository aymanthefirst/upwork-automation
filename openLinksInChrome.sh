#!/bin/bash

chrome_path="/c/Program Files/Google/Chrome/Application/chrome.exe"

urls=(
"https://www.upwork.com/ab/proposals/job/~01901c8ea3f0d9aeb5/apply/"
"https://www.upwork.com/ab/proposals/job/~019b77f1c60fea989d/apply/"
"https://www.upwork.com/ab/proposals/job/~0100fa158f026a4849/apply/"
"https://www.upwork.com/ab/proposals/job/~01901c8ea3f0d9aeb5/apply/"
"https://www.upwork.com/ab/proposals/job/~01fd942ba4a83e3137/apply/"
"https://www.upwork.com/ab/proposals/job/~013477dcd61a6b22f0/apply/"
)

for url in "${urls[@]}"
do
  "$chrome_path" --new-tab "$url"
done
