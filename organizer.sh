#!/bin/bash
# organizer.sh - archives grades.csv with a timestamp, resets the workspace, and logs the action.

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
ORIGINAL="grades.csv"

# Create the archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created dir: $ARCHIVE_DIR"
fi

# Make sure there is a file to archive
if [ ! -f "$ORIGINAL" ]; then
    echo "Error: $ORIGINAL not found in $(pwd). Nothing to archive."
    exit 1
fi

# Generate the timestamp and the new filename
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVED="grades_${TIMESTAMP}.csv"

# Move (rename) the file into the archive directory
if ! mv "$ORIGINAL" "$ARCHIVE_DIR/$ARCHIVED"; then
    echo "Error: could not move $ORIGINAL to $ARCHIVE_DIR/$ARCHIVED."
    exit 1
fi

# Workspace reset: create a fresh, empty grades.csv
touch "$ORIGINAL"

# Append the details to the log (>> accumulates entries across runs)
echo "[$TIMESTAMP] Original: $ORIGINAL | Archived as: $ARCHIVE_DIR/$ARCHIVED" >> "$LOG_FILE"

echo "Archived $ORIGINAL as $ARCHIVE_DIR/$ARCHIVED"
echo "Created a new empty $ORIGINAL"
echo "Logged to $LOG_FILE"
