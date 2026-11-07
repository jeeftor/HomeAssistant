#!/usr/bin/env bash

set -uo pipefail

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly NC='\033[0m'

readonly GITHUB_API='https://api.github.com/repos/jeeftor/HomeAssistant/contents'
readonly GITHUB_REF='master'

usage() {
    cat <<'EOF'
Usage: upload_icon_ng.sh [AWTRIX_HOST] [ICON_DIRECTORY]

Examples:
  ./upload_icon_ng.sh 192.168.1.42 weather
  ./upload_icon_ng.sh awtrix-ng.local
  ./upload_icon_ng.sh https://awtrix.example.test weather

AWTRIX_HOST and ICON_DIRECTORY are requested interactively when omitted.

If HTTP Basic Auth is enabled on AWTRIX NG, set AWTRIX_USER. The script asks
for AWTRIX_PASSWORD without echoing it when the variable is not already set.
EOF
}

fail() {
    printf '%bError:%b %s\n' "$RED" "$NC" "$1" >&2
    exit 1
}

require_command() {
    command -v "$1" >/dev/null 2>&1 || fail "Required command '$1' is not installed."
}

github_api() {
    curl --fail-with-body --silent --show-error --location \
        --header 'Accept: application/vnd.github+json' \
        --header 'X-GitHub-Api-Version: 2022-11-28' \
        "$1"
}

normalise_base_url() {
    local host="$1"

    host="${host%/}"
    if [[ "$host" != http://* && "$host" != https://* ]]; then
        host="http://$host"
    fi

    if [[ ! "$host" =~ ^https?://[^/]+$ ]]; then
        fail "AWTRIX_HOST must be a hostname or base URL without a path."
    fi

    printf '%s' "$host"
}

configure_auth() {
    AUTH_ARGS=()
    if [[ -z "${AWTRIX_USER:-}" ]]; then
        return
    fi

    if [[ ! -v AWTRIX_PASSWORD ]]; then
        read -rsp "AWTRIX password for ${AWTRIX_USER}: " AWTRIX_PASSWORD
        printf '\n'
    fi
    AUTH_ARGS=(--user "${AWTRIX_USER}:${AWTRIX_PASSWORD}")
}

list_icon_directories() {
    github_api "${GITHUB_API}/icons?ref=${GITHUB_REF}" |
        jq -er '[.[] | select(.type == "dir") | .name] | sort | .[]'
}

choose_icon_directory() {
    local requested="${1:-}"
    local directory
    local -a directories=()

    mapfile -t directories < <(list_icon_directories)
    ((${#directories[@]} > 0)) || fail 'No icon directories were found.'

    if [[ -n "$requested" ]]; then
        for directory in "${directories[@]}"; do
            if [[ "$directory" == "$requested" ]]; then
                printf '%s' "$directory"
                return
            fi
        done
        fail "Unknown icon directory '$requested'."
    fi

    printf '%bAvailable icon directories:%b\n' "$GREEN" "$NC" >&2
    PS3='Select a directory: '
    select directory in "${directories[@]}"; do
        if [[ -n "$directory" ]]; then
            printf '%s' "$directory"
            return
        fi
        printf '%bInvalid selection. Please try again.%b\n' "$YELLOW" "$NC" >&2
    done
}

list_icons() {
    local directory="$1"

    github_api "${GITHUB_API}/icons/${directory}?ref=${GITHUB_REF}" |
        jq -er '.[] | select(.type == "file" and (.name | test("\\.gif$"; "i"))) |
            [.name, .download_url] | @tsv'
}

verify_gif() {
    local path="$1"

    if file --brief --mime-type "$path" | grep -q '^image/gif$'; then
        return 0
    fi

    printf '%bSkipping invalid GIF:%b %s\n' "$RED" "$NC" "$(basename "$path")" >&2
    return 1
}

verify_awtrix_ng() {
    local response
    local version

    if ! response=$(curl --fail-with-body --silent --show-error \
        "${AUTH_ARGS[@]}" "${BASE_URL}/api/v1/version"); then
        fail "Cannot reach the AWTRIX NG API at ${BASE_URL}."
    fi

    version=$(jq -er '.version' <<<"$response") ||
        fail 'The device returned an unexpected version response.'
    printf '%bConnected to AWTRIX NG %s.%b\n' "$GREEN" "$version" "$NC"
}

upload_icon() {
    local icon_name="$1"
    local icon_url="$2"
    local local_path="${TEMP_DIR}/${icon_name}"
    local response

    if ! curl --fail-with-body --silent --show-error --location \
        "$icon_url" --output "$local_path"; then
        printf '%bDownload failed:%b %s\n' "$RED" "$NC" "$icon_name" >&2
        return 1
    fi

    verify_gif "$local_path" || return 1

    if ! response=$(curl --fail-with-body --silent --show-error \
        "${AUTH_ARGS[@]}" --request POST \
        --form "file=@${local_path};filename=${icon_name}" \
        "${BASE_URL}/api/v1/files?dir=/ICONS"); then
        printf '%bUpload failed:%b %s\n' "$RED" "$NC" "$icon_name" >&2
        return 1
    fi

    if ! jq -e '.ok == true' >/dev/null <<<"$response"; then
        printf '%bUnexpected upload response for %s:%b %s\n' \
            "$RED" "$icon_name" "$NC" "$response" >&2
        return 1
    fi

    printf '%bUploaded:%b %s\n' "$GREEN" "$NC" "$icon_name"
}

main() {
    local host="${1:-}"
    local requested_directory="${2:-}"
    local directory
    local icon_name
    local icon_url
    local uploaded=0
    local failed=0

    if [[ "$host" == '-h' || "$host" == '--help' ]]; then
        usage
        return
    fi
    if (($# > 2)); then
        usage >&2
        exit 2
    fi

    require_command curl
    require_command file
    require_command jq
    require_command mktemp

    if [[ -z "$host" ]]; then
        read -rp 'Enter the AWTRIX NG hostname or IP address: ' host
    fi
    [[ -n "$host" ]] || fail 'AWTRIX_HOST must not be empty.'

    BASE_URL=$(normalise_base_url "$host") || exit 1
    configure_auth
    verify_awtrix_ng

    directory=$(choose_icon_directory "$requested_directory") || exit 1
    printf '%bDownloading and uploading icons from %s...%b\n' \
        "$YELLOW" "$directory" "$NC"

    while IFS=$'\t' read -r icon_name icon_url; do
        [[ -n "$icon_name" && -n "$icon_url" ]] || continue
        if upload_icon "$icon_name" "$icon_url"; then
            ((uploaded += 1))
        else
            ((failed += 1))
        fi
    done < <(list_icons "$directory")

    if ((uploaded == 0 && failed == 0)); then
        fail "No GIF files were found in '$directory'."
    fi

    printf '\nUploaded: %d, failed: %d\n' "$uploaded" "$failed"
    ((failed == 0))
}

TEMP_DIR=$(mktemp -d) || fail 'Could not create a temporary directory.'
trap 'rm -rf -- "$TEMP_DIR"' EXIT

declare -a AUTH_ARGS=()
BASE_URL=''

main "$@"
