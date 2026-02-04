# roo.github.io

API Documentation for the 'roo' libraries - a collection of Arduino-compatible C++ libraries for ESP32 and related microcontrollers.

## About

This repository hosts the API documentation for the [roo libraries](https://github.com/dejwk?tab=repositories&q=roo_), including:

- **roo_display** - Library for driving display devices and touch panels (ILI9486, ILI9341, ST7789, etc.)
- **roo_io** - Common I/O classes and routines (data encoding/decoding, file and stream abstraction)
- **roo_windows** - Window management library with Material Design UI
- **roo_testing** - ESP32 emulator for testing Arduino sketches on Linux
- And many more...

## Documentation

Visit [https://dejwk.github.io/roo.github.io/](https://dejwk.github.io/roo.github.io/) to view the complete API documentation.

## How it Works

The documentation is automatically generated using [Doxygen](https://www.doxygen.nl/) from the source code of each library. The process is automated through GitHub Actions:

1. **Weekly Updates**: Documentation is regenerated every Sunday to capture the latest changes
2. **Manual Trigger**: Documentation can be regenerated on-demand via GitHub Actions
3. **Automatic Deployment**: Generated docs are deployed to GitHub Pages

## Local Development

To generate documentation locally:

```bash
# Install prerequisites
sudo apt-get install doxygen graphviz

# Generate documentation
bash generate_docs.sh

# Generate index page
python3 generate_index.py

# View docs (open docs/index.html in browser)
```

## Adding New Libraries

To add a new library to the documentation:

1. Edit `generate_docs.sh` and add the repository name to the `REPOS` array
2. Edit `generate_index.py` and add the repository name and description to the `REPOS` dictionary
3. Commit and push changes - the documentation will be regenerated automatically

## License

The documentation generation scripts are provided as-is. Each library has its own license - refer to the individual repository for details.

