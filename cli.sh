# echo "Running gsecrets inside Docker container"

SCRIPT_PATH=`greadlink -f ${BASH_SOURCE[0]} || readlink -f ${BASH_SOURCE[0]}`
cd `dirname ${SCRIPT_PATH}` > /dev/null

OUTPUT="$(docker-compose run --rm gsecrets $@)"
OUTPUT_NO_TRAIL_SPACE="$(echo "${OUTPUT}" | sed -e 's/[[:space:]]*$//')"
echo $OUTPUT_NO_TRAIL_SPACE