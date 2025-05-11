#!/bin/bash

# Create the mount point directory
sudo mkdir -p /mnt/object

# Change ownership to user 'cc'
sudo chown -R cc /mnt/object
sudo chgrp -R cc /mnt/object

# Mount the object store (replace 'project-21' with your actual container name if different)
rclone mount chi_tacc:object-persist-project-21 /mnt/object \
  --read-only \
  --allow-other \
  --daemon

# Verify mount
ls /mnt/object
