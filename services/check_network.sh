#!/bin/bash

# Define the target address and network interface
TARGET="google.com"
INTERFACE="usb0"

# Run the ping command
ping -I "$INTERFACE" -c 1 "$TARGET" > /dev/null 2>&1

# Check if the ping command was successful
if [ $? -eq 0 ]; then
    echo "Ping successful. No action needed."
    exit 0
else
    echo "Ping failed. Restarting modem and renewing DHCP lease."

    # Restart the modem
    sudo minicom -S restart_modem.sh

    # Wait for 15 seconds to allow the modem to restart
    sleep 15

    # Renew the DHCP lease
    sudo dhclient -v "$INTERFACE"

    echo "Modem restarted and DHCP lease renewed."
fi
