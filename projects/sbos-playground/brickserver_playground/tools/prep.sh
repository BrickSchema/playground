#!/usr/bin/env bash


user_id=$1

script_dir=$(dirname $0)
echo $script_dir


$script_dir/load_appmarket
$script_dir/upgrade_brick_users
$script_dir/register_admin
$script_dir/register_admin $user_id
$script_dir/upgrade_brick_users
#$sciprt_dir/activate_apps_for_user $user_id

$script_dir/add_user_rooms $user_id
