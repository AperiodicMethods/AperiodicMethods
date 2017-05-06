#!/bin/sh

# Check how many lines in module - excludes blanks line
printf "\n\n\n\n CHECK MODULE SIZE:"
find ./slf -name "*.py" -type f -exec grep . {} \; | wc -l

# Check number of lines using cloc
printf "\n\n\n CLOC OUTPUT (EXCLUDING TESTS): \n"
cloc slf --exclude-dir='tests'

printf "\n\n\n CLOC OUTPUT - TEST FILES: \n"
cloc slf/tests --exclude-dir='data'

# Run Tests & Check Coverage
#printf "\n\n\n RUN TESTS & CHECK COVERAGE: \n"
#coverage run --source slf --omit="*/plts/*" -m py.test

# Get summary from pylint?

# Print out some new lines
printf "\n\n\n\n"
