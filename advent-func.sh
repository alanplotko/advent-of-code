# Bash function to simplify running advent of code challenges
advent() {
  # Defaults
  filenames=()
  pythonFile="./$(basename "$PWD").py"

  # Shorcut when in repo/<year> to run solutions for /day-x without cd'ing into it
  if [[ "$PWD" =~ .*"/advent-of-code/"[0-9]{4}$ ]]; then
    if ! [ -z "$1" ] && [[ $1 =~ ^[0-9]{1,2}$ ]]; then
      n=$(printf %02d $1)
      filenames+=( "./day-$n/test.txt" )
      # For parsing find results, see latest 2020 update on bash 4.4-alpha+ here: https://stackoverflow.com/questions/23356779/how-can-i-store-the-find-command-results-as-an-array-in-bash/23357277#23357277
      readarray -d '' otherTests < <(find . -wholename "*/day-$n/test-*.txt" -print0)
      filenames+=("${otherTests[@]}")
      filenames+=( "./day-$n/input.txt" )
      pythonFile="./day-$n/day-$n.py"
    else
      echo "Error: Bad day number provided"
      return
    fi
  # Otherwise, must be in repo/<year>/day-x
  elif ! [[ "$PWD" =~ .*"/advent-of-code/"[0-9]{4}"/day-"[0-9]{1,2} ]]; then
    echo "Error: advent command only available in advent-of-code directory"
    return
  fi

  # Determine filenames if not already set
  if [ ${#filenames[@]} -eq 0 ]; then
    if [ -z "$1" ] || [[ $1 =~ ^all|A|a$ ]]; then
      filenames+=( "./test.txt" )
      # For parsing find results, see latest 2020 update on bash 4.4-alpha+ here: https://stackoverflow.com/questions/23356779/how-can-i-store-the-find-command-results-as-an-array-in-bash/23357277#23357277
      readarray -d '' otherTests < <(find . -name "test-*.txt" -print0)
      filenames+=("${otherTests[@]}")
      filenames+=( './input.txt' )
    elif [[ $1 =~ ^test|T|t$ ]]; then
      filenames+=( "./test.txt" )
      # For parsing find results, see latest 2020 update on bash 4.4-alpha+ here: https://stackoverflow.com/questions/23356779/how-can-i-store-the-find-command-results-as-an-array-in-bash/23357277#23357277
      readarray -d '' otherTests < <(find . -name "test-*.txt" -print0)
      filenames+=("${otherTests[@]}")
    elif [[ $1 =~ ^input|I|i$ ]]; then
      filenames=( "./input.txt" )
    else
      echo "Error: Bad input file provided"
      return
    fi
  fi

  # Run Python file using provided input file
  for filename in "${filenames[@]}"
  do
    echo -e "\n--- Running $pythonFile for $filename ---"
    python $pythonFile < $filename
  done
}
