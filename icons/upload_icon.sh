#!/bin/bash
#
# Call this script with:
# bash -c "$(curl -fsSL https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/upload_icon.sh)"
#
list_icon_directories() {
    OWNER="jeeftor"
    REPO="HomeAssistant"
    BRANCH="master"
    DIRECTORY="icons"

    # Make the API request to list the directory contents
    response=$(curl -s "https://api.github.com/repos/$OWNER/$REPO/contents/$DIRECTORY?ref=$BRANCH")

    # Extract directory names
    directories=($(echo "$response" | jq -r '.[] | select(.type == "dir") | .name'))

    # Return the list of directories
    echo "${directories[@]}"
}

list_icons() {
    OWNER="jeeftor"
    REPO="HomeAssistant"
    BRANCH="master"
    DIRECTORY="icons/$1"

    # Make the API request to list the directory contents
    curl -s "https://api.github.com/repos/$OWNER/$REPO/contents/$DIRECTORY?ref=$BRANCH" | jq -r '.[].download_url'
}

upload_icon() {
    IP_ADDRESS="$1"
    ICON_NAME="$2"
    FILE_NAME="$3"
    URL="http://$IP_ADDRESS/edit"

    TEMP_FILE=$(mktemp)

    BASE_URL="https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/"
    GIF_FILE="$BASE_URL/$ICON_NAME"

    curl -s -X GET "$GIF_FILE" -o "$TEMP_FILE"
    curl -X POST -F "file=@$TEMP_FILE;filename=/ICONS/$FILE_NAME" "$URL"
    echo "Uploaded icon: $ICON_NAME"

    rm "$TEMP_FILE"
}

# Prompt for IP address
read -p "Enter the IP address: " IP_ADDRESS

# List icon directories
echo "Available icon directories:"
directories=($(list_icon_directories))

# Prompt for directory selection
PS3="Select a directory: "
select DIRECTORY_NAME in "${directories[@]}"; do
    if [[ -n $DIRECTORY_NAME ]]; then
        break
    else
        echo "Invalid selection. Please try again."
    fi
done

# Example usage
ICONS=($(list_icons "$DIRECTORY_NAME"))

for ICON_URL in "${ICONS[@]}"; do
    ICON_NAME=$(basename "$ICON_URL")
    FILE_NAME="$ICON_NAME"

    upload_icon "$IP_ADDRESS" "$DIRECTORY_NAME/$ICON_NAME" "$FILE_NAME"
done
