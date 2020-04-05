#!/bin/bash
## Version 1 brought over from old repo
## https://github.com/psjbeisler/comvert

## System Variables
BLIST="/opt/comvert/blacklist.ini" # Define the blacklist
TEMP="/tmp" # Convert stats are temporary

## Default Options
SOURCE=$(pwd)
INPUT="cbr"
OUTPUT="cbz"

## User Options
while getopts s:i:o:f:l:h opt; do
	case $opt in
	s) # Source directory
		SOURCE=$OPTARG
		;;
	i) # Input format
		INPUT=$OPTARG
		;;
	o) # Output format
		OUTPUT=$OPTARG
		;;
	f) # Only work one file
		FILE=$OPTARG
		;;
	l) # Log suspicious files locally
		LOCAL="1"
		;;
	h) # Help dialog
		HELP="1"
		;;
	esac
done

shift $((OPTIND - 1))

if [[ "$HELP" == "1" ]]; then
	echo "-s [ source directory ]
-i [ input file type {cbr,cbz,cbt,cb7} ]
-o [ output file type {cbz,cbt,cb7} ]
	7-Zip doesn't support .rar ouput
-f [ single filename ]
-l [ log anything suspicious ]"
	exit 0
fi

## Check source folder
if [[ "$SOURCE" != /* ]]; then
	SOURCE="$(dirname -- "$(realpath -- "$SOURCE")")/$SOURCE"
fi

## Define INPUT format
if [ -z "$FILE" ]; then
	COMIC="*.$INPUT"
else
	INPUT="${FILE#*.}" # Get INPUT type from file
	FILE=`basename "$FILE" .$INPUT` # Redefine the file
	COMIC="$FILE.$INPUT"
fi

## Define OUTPUT format
if [ "$OUTPUT" == "cbz" ]; then
	FORMAT="zip"
elif [ "$OUTPUT" == "cbt" ]; then
	FORMAT="tar"
elif [ "$OUTPUT" == "cb7" ]; then
	FORMAT="7z"
else
	{ echo "+ Output format is not supported"; echo; exit 1; }
fi

## Output Variables
LOG="$TEMP/comvert.log"
CACHE="$SOURCE/.cb_cache"

## Sanity checks
if [ ! -f "$BLIST" ];then
	{ echo "+ Could not find the Blacklist"; exit 1; }
fi

if [ -f "$LOG" ];then
	rm "$LOG" \
		|| { echo "+ Error removing old log"; exit 1; }
	touch "$LOG" 2>/dev/null \
		|| { echo "+ Error writing log"; exit 1; }
else
	touch "$LOG" 2>/dev/null \
		|| { echo "+ Error writing log"; exit 1; }
fi

if [ -d "$CACHE" ]; then
	rm -rf "$CACHE" \
		|| { echo "+ Error removing old cache"; exit 1; }
	mkdir "$CACHE" 2>/dev/null \
		|| { echo "+ Error creating cache"; exit 1; }
else
	mkdir "$CACHE" 2>/dev/null \
		|| { echo "+ Error creating cache"; exit 1; }
fi

## Start Logging
clear
exec > >(tee "$LOG")
echo "+ Working from $SOURCE"
echo

## Convert Loop
find "$SOURCE" -name "$COMIC" | while read CBFILE; do

BASENAME=`basename "$CBFILE" .$INPUT`
DIRNAME=`dirname "$CBFILE"`
NEWNAME="$BASENAME.$OUTPUT"

echo "> Processing: $BASENAME"
	cd "$CACHE"

echo "-> Extracting"
	7z x "$CBFILE" >/dev/null

echo "--> Scanning"

## Scan the Blacklist
while read CBSCAN; do
	CBCRED=`find -type f -iname "$CBSCAN"`
	if [ ! -z "$CBCRED" ]; then
		rm "$CBCRED"
		echo "--> Removed Blacklisted File"
	fi
done < "$BLIST"

## Scan for Suspicious files
SUSP="$SOURCE/suspicious_files.txt"
CBSCAN=`find -type f -iname "[x-z]*"`
if [ ! -z "$CBSCAN" ]; then
	echo "--> Suspicious files found!"
	if [ "$LOCAL" == "1" ];then
		echo "$BASENAME" >> "$SUSP"
		echo "$CBSCAN" >> "$SUSP"
		echo "|" >> "$SUSP"
		echo "--> And logged to file"
	else
		echo "--> But not logged"
	fi
fi

echo "-> Compressing"
	7z a -sdel -t$FORMAT "$NEWNAME" * > /dev/null
	mv "$NEWNAME" "$DIRNAME"

## Dont delete the new file if it has the same name
if [ "$INPUT" != "$OUTPUT" ]; then
	rm "$CBFILE"
fi

echo "> Complete"
echo
done

echo "=> Conversion Done"
rmdir "$CACHE"
echo

## Stats
CBDID=$(cat "$LOG" |grep -c -i "Processing")
CBFND=$(cat "$LOG" |grep -c -i "Blacklisted")
CBMSD=$(cat "$LOG" |grep -c -i "Suspicious")

echo "+ $CBDID archives processed"
echo "+ $CBFND files removed"
echo "+ $CBMSD suspicious archives"
echo

## Optionally Notify
#notify-send Comvert "Sir, your comics are done"
