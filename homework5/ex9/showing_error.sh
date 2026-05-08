FILE="config.config"
if [ -f "$FILE" ]; then
	cat "$FILE"
else
	echo "Error. File $FILE doesn't exist"
fi
