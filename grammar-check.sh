#!/usr/bin/env bash

# Copyright 2024 Zaphiro Technologies
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

error=0
errorMessages=""
declare -a ignorefiles
parameters=""

clean_brackets() {
  if [[ $(uname) == "Darwin" ]]; then
      # macOS requires an argument for -i to specify the backup file extension
      sed -E -i '' '/```/,/```/! s/`//g' "$1"
  else
      # Linux systems do not require an argument for -i
      sed -E -i '/```/,/```/! s/`//g' "$1"
  fi
}

while getopts m:f:mode:file: flag
do
    case "${flag}" in
        m|mode) mode=${OPTARG};;
        f|file) file=${OPTARG};;
    esac
done

if [ -z ${mode+x} ]; then
  echo "Mode not set using default";
  mode="github-action"
  parameters=""
else
  case $mode in
    github-action)
      parameters=""
      ;;
    local)
      parameters="-e casing -e colloquialisms -e compounding -e confused_words -e false_friends -e gender_neutrality -e grammar -e misc -e punctuation -e redundancy -e repetitions -e regionalisms -e semantics -e style -e typos"
      ;;
    local-non-interactive)
      parameters="-e casing -e colloquialisms -e compounding -e confused_words -e false_friends -e gender_neutrality -e grammar -e misc -e punctuation -e redundancy -e repetitions -e regionalisms -e semantics -e style -e typos  -p"
      ;;
    *)
      echo "Invalid Mode"
      exit 1
      ;;
  esac
fi

echo "Mode: $mode";
echo "Paramaters: $parameters"

if [ -z ${file+x} ]; then
  if [ -f .grammarignore ]; then
      echo 'Loading ignore list...'
      ignorefiles=(`cat ".grammarignore"`)
  fi

  while read line; do
    file=${line:2}
    if [[ ! ${ignorefiles[*]} =~ "$file" ]]
      then
        echo ""
        echo "...processing $file"
        echo ""
        filesize=$(wc -c $line | awk '{print $1}')
        if [[ $filesize -gt 20000 && $file ]]
          then
            echo "The file $file is too big, it will be split in sub files and checked:"
            csplit -k -n 4 -s -f 'tmp' $line '/##/' '{100}'
            while read tmp; do
                clean_brackets $tmp
                npx gramma check -m -p $parameters "$tmp"
                if [ $? -ne 0 ]; then
                  error=1
                  if [[ $errorMessages != *"$file"* ]]; then
                    errorMessages=$errorMessages"\n - ${file}"
                  fi    
                fi
            done <<<$(find . -name "tmp*" -type f)
            rm -rf tmp*
          else
            cp $line tmp
            clean_brackets tmp
            npx gramma check -m -p $parameters tmp
            if [ $? -ne 0 ]; then
                error=1
                errorMessages=$errorMessages"\n - ${file}"
            fi
            rm tmp
        fi
    fi
  done <<<$(find . -iname "*.md" -type f)

  if [ $error -ne 0 ]; then
    echo "The following files contain errors:"
    echo -e $errorMessages
    echo ""
    exit 1
  fi
else
  echo "Checking a single file"
  echo $file
  # filesize=$(wc -c $file | awk '{print $1}')
  # if [[ $filesize -gt 20000 && $file ]]
  #   then
  #     echo "The file $file is too big, it will be split in sub files and checked:"
  #     csplit -k -n 4 -s -f 'tmp' $file '/##/' '{100}'
  #     while read tmp; do
  #         clean_brackets $tmp
  #         npx gramma check -m -p $parameters "$tmp"
  #     done <<<$(find . -name "tmp*" -type f)
  #     rm -rf tmp*
  #   else
  #     if [ "$mode" != "local" ]; then
  #       cp $file tmp
  #       clean_brackets tmp
  #       npx gramma check -m $parameters tmp
  #       rm tmp
  #     else
  #       npx gramma check -m $parameters $file
  #     fi
  # fi
fi
