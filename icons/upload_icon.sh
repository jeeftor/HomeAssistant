#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

#
# Call this script with:
# bash -c "$(curl -fsSL https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/upload_icon.sh)"
#

list_icon_directories() {
    if ! command -v jq >/dev/null 2>&1; then
        echo -e "${RED}Error: 'jq' is not installed. Please install 'jq' to run this script.${NC}"
        exit 1
    fi

    local OWNER="jeeftor"
    local REPO="HomeAssistant"
    local BRANCH="master"
    local DIRECTORY="icons"

    # Make the API request to list the directory contents
    local response=$(curl -s "https://api.github.com/repos/$OWNER/$REPO/contents/$DIRECTORY?ref=$BRANCH")

    # Extract directory names
    local directories=($(echo "$response" | jq -r '.[] | select(.type == "dir") | .name'))

    # Return the list of directories
    echo "${directories[@]}"
}

list_icons() {
    local OWNER="jeeftor"
    local REPO="HomeAssistant"
    local BRANCH="master"
    local DIRECTORY="icons/$1"

    # Make the API request to list the directory contents
    local response=$(curl -L -s "https://api.github.com/repos/$OWNER/$REPO/contents/$DIRECTORY?ref=$BRANCH")

    # Extract URLs of files with the .gif extension
    local icons=($(echo "$response" | jq -r '.[] | select(.type == "file" and (.name | test("\\.gif$"))) | .download_url'))

    # Return the list of icons
    echo "${icons[@]}"
}

verify_gif() {
    local FILE_NAME="$1"

    if file -b --mime-type "$FILE_NAME" | grep -q '^image/gif$'; then
        # File is a valid GIF
        return 0
    else
        echo -e "${RED}Error: File $FILE_NAME is NOT a valid GIF file.${NC}"
        return 1
    fi
}

upload_icon() {
    local IP_ADDRESS="$1"
    local ICON_NAME="$2"
    local FILE_NAME="$3"

    URL="http://$IP_ADDRESS/edit"

    TEMP_FILE=".$FILE_NAME"

    BASE_URL="https://raw.githubusercontent.com/jeeftor/HomeAssistant/master/icons/"
    GIF_FILE="$BASE_URL/$ICON_NAME"

    curl -L -s -X GET "$GIF_FILE" -o "$TEMP_FILE"

    if verify_gif "$TEMP_FILE"; then
        curl -X POST -F "file=@$TEMP_FILE;filename=/ICONS/$FILE_NAME" "$URL"
        echo -e "  ${GREEN}Uploaded icon:${NC} $FILE_NAME${NC}"
    else
        echo -e "${RED}Error: File $FILE_NAME does not appear to be a valid GIF file.${NC}"
        echo -e "${RED}Try yourself with:${NC} curl -L -s -X GET \"$GIF_FILE\" -o $TEMP_FILE"
    fi

    rm -f "$TEMP_FILE"
}

# Prompt for IP address if not provided as command-line argument
if [ -z "$1" ]; then
    read -p "Enter the IP address: " IP_ADDRESS
else
    IP_ADDRESS="$1"
fi

# Validate IP address format
if ! [[ $IP_ADDRESS =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Invalid IP address format.${NC}"
    exit 1
fi

# List icon directories
echo -e "${GREEN}Available icon directories:${NC}"
directories=($(list_icon_directories))

# Prompt for directory selection
PS3="Select a directory: "
select DIRECTORY_NAME in "${directories[@]}"; do
    if [[ -n $DIRECTORY_NAME ]]; then
        break
    else
        echo -e "${YELLOW}Invalid selection. Please try again.${NC}"
    fi
done

# Example usage
ICONS=($(list_icons "$DIRECTORY_NAME"))

echo -e "${YELLOW}Downloading icons...${NC}"

for ICON_URL in "${ICONS[@]}"; do
    ICON_NAME=$(basename "$ICON_URL")

    upload_icon "$IP_ADDRESS" "$DIRECTORY_NAME/$ICON_NAME" "$ICON_NAME"
done
