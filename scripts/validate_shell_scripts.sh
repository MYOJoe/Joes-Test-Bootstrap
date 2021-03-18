#!/bin/sh
# shellcheck disable=SC2044
# shellcheck disable=SC2039
set -euo

rc=0
for filename in $(find . -name '*.sh') ; do
  echo "==> Validating ${filename}"
  shellcheck "${filename}" || exit $?
done

exit $rc
