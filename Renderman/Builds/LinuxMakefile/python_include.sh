PYTHON_EXEC=$(which python3 || which python)

PYTHON_VERSION=$("PYTHON_EXEC" -c "import sys; print(sys.version_info.major)" 2>/dev/null)

PYTHON_INCLUDE="/usr/include/python$PYTHON_VERSION"

echo $PYTHON_INCLUDE