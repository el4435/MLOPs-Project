#!/bin/bash

set -e

echo "Installing rclone ..."
curl https://rclone.org/install.sh | sudo bash

echo "Enabling 'user_allow_other' in /etc/fuse.conf ..."
sudo sed -i '/^#user_allow_other/s/^#//' /etc/fuse.conf

echo "Creating rclone config directory ..."
mkdir -p ~/.config/rclone

echo "Writing rclone.conf ..."
cat <<EOF > ~/.config/rclone/rclone.conf
[chi_tacc]
type = swift
user_id = el4435
application_credential_id = 89af6e3bf3864ba591ff0310c6ca43bf
application_credential_secret = WgK2QXScRF5yz55JxC17ss9dZu8ITWTwU2aN04ubhSWRGvk5iXMoY7WELEOZMuVbMJSGTqdpfxgWppAtC98X5A
auth = https://chi.tacc.chameleoncloud.org:5000/v3
region = CHI@TACC
EOF

echo "rclone setup complete. You can test the connection with:"
echo "    rclone lsd chi_tacc:"
