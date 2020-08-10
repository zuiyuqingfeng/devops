#bin/bash
ps aux | grep -w "$0" | grep -q "sudo " && echo "do not run with sudo" && exit 2
# define BASE_DIR
BASE_DIR="$(cd "`dirname $0`" && echo $PWD || exit 2)"
# define python3
echo $BASE_DIR
#python3="${BASE_DIR}/python3/bin/python3"
python3=`which python3`
[ ! -x ${python3} ] && echo "check python3: ${python3}" && exit 2
echo $python3
main=${BASE_DIR}/apps/run_checker.py
[ ! -f $main ] && echo "$main not exist" && exit 2

${python3} $main "$@"