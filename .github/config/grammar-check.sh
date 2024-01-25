#!/usr/bin/env bash

error=0
errorMessages=""

while read line; do
  file=${line:6}
  echo ""
  echo "...processing $file"
  echo ""
  filesize=$(wc -c $line | awk '{print $1}')
    
  if [[ $filesize -gt 20000 ]]
    then
       echo "The file $file is too big, it will be split in sub files and checked:"
       csplit -k -n 4 -s -f 'tmp' $line '/##/' '{100}'
       while read tmp; do
          npx gramma check -m -p "$tmp"
          if [ $? -ne 0 ]; then
            error=1
            if [[ $errorMessages != *"$file"* ]]; then
              errorMessages=$errorMessages"\n - ${file}"
            fi    
          fi
       done <<<$(find . -name "tmp*" -type f)
       rm -rf tmp*
    else
       npx gramma check -m -p "$line"
       if [ $? -ne 0 ]; then
          error=1
          errorMessages=$errorMessages"\n - ${file}"
       fi 
  fi
done <<<$(find ../.. -name "*.md" -type f)

if [ $error -ne 0 ]; then
  echo "The following files contain errors:"
  echo -e $errorMessages
  echo ""
  exit 1
fi