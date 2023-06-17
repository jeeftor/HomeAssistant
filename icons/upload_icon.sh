#!/bin/bash
set -e

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
    curl -L -s "https://api.github.com/repos/$OWNER/$REPO/contents/$DIRECTORY?ref=$BRANCH" | jq -r '.[].download_url'
}

verify_gif() {
    local FILE_NAME="$1"

    gif_header=$(head -c 6 "$FILE_NAME" | od -An -t x1 | tr -d ' ')
    if echo "$gif_header" | grep -q "^474946383961"; then
        # echo "File $FILE_NAME appears to be a valid a GIF file."
        return 0
    else
        echo "Error: File $FILE_NAME is NOT a valid GIF file."
        return 1
    fi
}
upload_icon() {
    local IP_ADDRESS="$1"
    local ICON_NAME="$2"
    local FILE_NAME="$3"
    echo FILE_NAME=$FILE_NAME

    URL="http://$IP_ADDRESS/edit"

    TEMP_FILE=".$FILE_NAME"

    BASE_URL="https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/"
    GIF_FILE="$BASE_URL/$ICON_NAME"

    curl -L -s -X GET "$GIF_FILE" -o "$TEMP_FILE"

    if verify_gif "$TEMP_FILE"; then
        curl -X POST -F "file=@$TEMP_FILE;filename=/ICONS/$FILE_NAME" "$URL"
        echo "Uploaded icon: $FILE_NAME"
    else
        echo "Error: File $TEMP_FILE is not a valid GIF file."
    fi

    rm -f "$TEMP_FILE"

}

# Prompt for IP address
read -p "Enter the IP address: " IP_ADDRESS

# Validate IP address format
if ! [[ $IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Invalid IP address format."
    exit 1
fi
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

echo "Downloading $ICONS"

for ICON_URL in "${ICONS[@]}"; do
    ICON_NAME=$(basename "$ICON_URL")

    upload_icon "$IP_ADDRESS" "$DIRECTORY_NAME/$ICON_NAME" "$FILE_NAME"
done
