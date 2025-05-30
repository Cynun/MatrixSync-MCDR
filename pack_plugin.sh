#!/bin/bash
package_config() {
    ini_file=$1
    section=$2
    key=$3

    value=$(awk -F '=' -v section="$section" -v key="$key" '
    /^\[/{in_section=0}
    /^\['$section'\]/{in_section=1}
    in_section && $1==key{print $2; exit}
    ' "$ini_file")

    echo $value
}

config_file="config.ini"
framework_ver=$(package_config "$config_file" "framework" "ver")
main_ver=$(package_config "$config_file" "main" "ver")
is_stable=$(package_config "$config_file" "release" "test")
build_plg=$(package_config "$config_file" "ci" "plugin")
build_subpack=$(package_config "$config_file" "ci" "subpack")

if [ "$build_plg" -eq 1 ]; then
    if [ "$is_stable" -eq 1 ]; then
        zip -r "MatrixSync-v${main_ver}-${framework_ver}.mcdr" mcdreforged.plugin.json requirements.txt LICENSE lang matrix_sync
    else
        zip -r "MatrixSync-v${main_ver}.mcdr" README.md README_en_us.md mcdreforged.plugin.json requirements.txt LICENSE lang matrix_sync
    fi
fi