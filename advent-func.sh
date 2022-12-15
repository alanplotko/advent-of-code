# Bash function to simplify running advent of code challenges
advent() {
  # Determine filenames
  if [ -z "$1" ] || [[ $1 =~ ^all|A|a$ ]]; then
    filenames=( 'test.txt' 'input.txt' )
  elif [[ $1 =~ ^test|T|t$ ]]; then
    filenames=( 'test.txt' )
  elif [[ $1 =~ ^input|I|i$ ]]; then
    filenames=( 'input.txt' )
  else
    echo "Error: Bad input file provided"
    return
  fi

  # Must be in advent of code repo
  if ! [[ "$PWD" =~ .*"/advent-of-code/"[0-9]{4}"/day-"[0-9]{1,2} ]]; then
    echo "Error: advent command only available in advent-of-code directory"
    return
  fi

  # Run Python file using provided input file
  day=$(basename "$PWD")
  for filename in "${filenames[@]}"
  do
    echo "--- Running $day.py for $filename ---"
    python "$day.py" < $filename
    echo -e "\n"
  done
}
