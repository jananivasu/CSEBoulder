current_file_path=$(readlink -f '$0')
parentDir=$(dirname "$current_file_path")


# Run the linter on every file
pylint_runner "$parentDir"

# Run test coverage on the project
py.test --cov="$parentDir" --cov-report=xml "$parentDir"