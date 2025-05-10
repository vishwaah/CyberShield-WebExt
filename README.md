# CyberShield Web Extension

CyberShield is a browser extension designed to detect fraudulent websites and protect user privacy. It provides real-time safety scores and alerts to help users browse securely.

## Features

- **Real-Time Threat Detection**: Analyzes websites in real-time to identify potential threats and fraudulent activities.
- **Privacy Protection**: Safeguards user data by preventing unauthorized tracking and data collection.
- **User-Friendly Interface**: Offers intuitive alerts and safety scores to inform users about website credibility.
- **Lightweight and Efficient**: Designed to operate seamlessly without impacting browser performance.

## Installation

### For Chrome Users

1. Download the repository as a ZIP file or clone it using Git:
   ```bash
   git clone https://github.com/vishwaah/CyberShield-WebExt.git
   ```

2. Open Chrome and navigate to `chrome://extensions/`.

3. Enable **Developer mode** by toggling the switch in the top right corner.

4. Click on **Load unpacked** and select the `Extension` directory from the cloned repository.

### For Firefox Users

1. Download the repository as a ZIP file or clone it using Git:
   ```bash
   git clone https://github.com/vishwaah/CyberShield-WebExt.git
   ```

2. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`.

3. Click on **Load Temporary Add-on**.

4. Select the `manifest.json` file located in the `Extension` directory of the cloned repository.

## Usage

Once installed, CyberShield will automatically analyze each website you visit. If a site is deemed suspicious or potentially harmful, the extension will display an alert with a safety score, allowing you to make informed decisions while browsing.

## Development

The repository is structured into two main directories:

- **Extension**: Contains the browser extension's source code, including HTML, CSS, and JavaScript files.
- **Server**: Houses backend components that may support the extension's functionality (details depend on implementation).

To contribute or modify the extension:

1. Clone the repository:
   ```bash
   git clone https://github.com/vishwaah/CyberShield-WebExt.git
   ```

2. Navigate to the `Extension` directory and make desired changes.

3. Reload the extension in your browser to see the updates.

## Contributing

Contributions are welcome! If you'd like to enhance CyberShield, please fork the repository and submit a pull request. For major changes, open an issue first to discuss potential improvements.

## License

This project is licensed under the [MIT License](LICENSE).


