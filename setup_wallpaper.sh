#!/bin/bash

# Variables for paths
SCRIPT_NAME="wallpaper.py"
PLIST_NAME="com.wallpaper.plist"
SCRIPTS_DIR="$HOME/scripts"
FULLDISK_DIR="$SCRIPTS_DIR/FullDisk"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_DESTINATION="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Function to print messages
print_message() {
    echo -e "\033[1;32m$1\033[0m"
}

# Step 1: Install Homebrew (if not installed)
if ! command -v brew &> /dev/null; then
    print_message "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" </dev/null
else
    print_message "Homebrew is already installed."
fi

# Step 2: Install Python (if not installed)
if ! command -v python3 &> /dev/null; then
    print_message "Python3 not found. Installing Python3..."
    brew install python -q
else
    print_message "Python3 is already installed."
fi

# Step 3: Install Python dependencies
print_message "Installing Python dependencies (requests, beautifulsoup4)..."
pip3 install --quiet --user requests beautifulsoup4

# Step 4: Create necessary directories
print_message "Creating necessary directories..."
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$FULLDISK_DIR"
mkdir -p "$LAUNCH_AGENTS_DIR"

# Step 5: Copy files to their correct locations
print_message "Copying script and Launchd plist file..."
cp "./$SCRIPT_NAME" "$SCRIPTS_DIR/$SCRIPT_NAME"
cp "./$PLIST_NAME" "$PLIST_DESTINATION"

# Step 6: Set permissions
print_message "Setting permissions..."
chmod +x "$SCRIPTS_DIR/$SCRIPT_NAME"
chmod 644 "$PLIST_DESTINATION"

# Step 7: Replace placeholders in plist file
print_message "Configuring plist file..."
sed -i '' "s|~/scripts|$SCRIPTS_DIR|g" "$PLIST_DESTINATION"

# Step 8: Load the Launchd job
print_message "Loading Launchd job..."
launchctl unload "$PLIST_DESTINATION" 2>/dev/null  # Unload if already loaded
launchctl load "$PLIST_DESTINATION"

# Step 9: Final message
print_message "Setup complete!"
echo "Wallpaper script has been installed. Images will be stored in: $FULLDISK_DIR"
echo "Log file: $SCRIPTS_DIR/wallpaper.log"

