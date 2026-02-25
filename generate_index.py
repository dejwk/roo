#!/usr/bin/env python3
"""
Generate index.html for the API documentation site.
"""

import os
import shutil
from datetime import datetime, timezone

# Repository information (name: description)
REPOS = {
    "roo_display": "Arduino-compliant library for driving display devices and touch panels, e.g. ILI9486, ILI9341, or ST7789. Powerful and fast.",
    "roo_io": "Common I/O classes and routines: data encoding/decoding, file and stream abstraction, byte iterators.",
    "roo_windows": "Window management library, supporting touch, visually modeled on Material Design.",
    "roo_testing": "Experimental ESP32 emulator that can be used to test Arduino sketches on Linux.",
    "roo_transport": "Reliable transport (bidi streams, reliable packets, messaging) over Serial.",
    "roo_logging": "Arduino logging library for ESP32 and related boards. Based on Google's glog.",
    "roo_windows_wifi": "GUI WiFi configurator for ESP32, using roo_windows.",
    "roo_windows_transceivers": "UI configuration for roo_transceivers, using the roo_windows framework.",
    "roo_prefs": "ESP32 'Preferences' utility library for management of persistent settings.",
    "roo_monitoring": "Library to allow capture and aggregation of monitoring metrics on microcontrollers.",
    "roo_time": "Arduino-compliant ESP32 library for basic management of elapsed time, wall time, and date time with multi-timezone support.",
    "roo_quantity": "Helpers to handle physical quantities, such as temperature, pressure, distance, velocity, etc.",
    "roo_transceivers": "Detection and aggregation of arbitrary transceiver devices, supporting arbitrary sensors and actuators.",
    "roo_wifi": "WiFi controller library for ESP32, supporting storing persistent configuration in flash.",
    "roo_onewire": "Library for OneWire thermometers. Supports asynchronous conversion with event notification.",
    "roo_collections": "Small, flat, memory-conscious hashtable for microcontrollers (e.g. Arduino projects).",
    "roo_scheduler": "Arduino-compliant microcontroller library for scheduling delayed and/or repetitive tasks.",
    "roo_blink": "Blink LEDs like a pro! (On ESP32 / Arduino).",
    "roo_flags": "Minimalistic support for run-time options. Useful in libraries, for dynamic configuration.",
    "roo_comms": "Home automation library for Espressif SOCs, building on top of the esp_now protocol.",
    "roo_locale": "Locale-related functionality, used by other roo libraries.",
    "roo_icons": "Collection of icons for use with the roo_display library.",
    "roo_threads": "Experimental portable threading library. Enables emulation of ESP32 multithreaded programs under roo_testing.",
    "roo_control": "Arduino relays, port extenders, debouncing, retries: common abstractions and implementations.",
    "roo_windows_onewire": "GUI OneWire thermometer configurator for ESP32, using roo_windows.",
    "roo_time_ds3231": "Arduino driver for DS3231 real-time clock, compliant with roo_time.",
}

def copy_theme_assets(output_dir, available_repos):
    """Copy Doxygen theme assets to a stable docs/_theme directory.

    Copies doxygen.css and tabs.css from the first available library's html/
    output, and copies the doxygen-awesome CSS/JS files from docs/doxygen-awesome/.
    Returns True if at least the doxygen.css was successfully copied.
    """
    theme_dir = os.path.join(output_dir, "_theme")
    os.makedirs(theme_dir, exist_ok=True)

    # Copy doxygen.css and tabs.css from the first library that has them
    for repo in available_repos:
        html_dir = os.path.join(output_dir, repo, "html")
        copied = 0
        for asset in ["doxygen.css", "tabs.css"]:
            src = os.path.join(html_dir, asset)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(theme_dir, asset))
                copied += 1
        if copied > 0:
            print(f"Copied doxygen.css/tabs.css from {repo}/html/ to {theme_dir}")
            break

    # Copy doxygen-awesome CSS/JS assets (already downloaded at a stable path)
    awesome_dir = os.path.join(output_dir, "doxygen-awesome")
    if os.path.isdir(awesome_dir):
        for fname in os.listdir(awesome_dir):
            src = os.path.join(awesome_dir, fname)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(theme_dir, fname))
        print(f"Copied doxygen-awesome assets to {theme_dir}")
    else:
        print(f"Warning: {awesome_dir} not found; theme assets may be incomplete")

    return os.path.exists(os.path.join(theme_dir, "doxygen.css"))


def generate_index():
    """Generate the index.html file."""
    
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check which repositories have documentation
    available_repos = []
    for repo in REPOS.keys():
        repo_doc_path = os.path.join(output_dir, repo, "html", "index.html")
        if os.path.exists(repo_doc_path):
            available_repos.append(repo)
    
    # Sort repositories alphabetically
    available_repos.sort()

    # Copy Doxygen theme assets to a stable location
    copy_theme_assets(output_dir, available_repos)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Roo Libraries - API Documentation</title>
    <link href="_theme/tabs.css" rel="stylesheet" type="text/css" />
    <link href="_theme/doxygen.css" rel="stylesheet" type="text/css" />
    <link href="_theme/doxygen-awesome.css" rel="stylesheet" type="text/css" />
    <script type="text/javascript" src="_theme/doxygen-awesome-darkmode-toggle.js"></script>
    <script type="text/javascript">
        if (typeof DoxygenAwesomeDarkModeToggle !== "undefined") {{
            DoxygenAwesomeDarkModeToggle.init();
        }}
    </script>
    <style>
        /* Card grid layout - not provided by the Doxygen theme */
        .repo-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }}

        .repo-card {{
            border: 1px solid var(--separator-color, #e0e0e0);
            border-radius: var(--border-radius-large, 8px);
            padding: 20px;
            transition: all 0.3s ease;
        }}

        .repo-card:hover {{
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }}

        .repo-card h2 {{
            font-size: 1.3em;
            margin-bottom: 10px;
        }}

        .repo-card a {{
            text-decoration: none;
            color: inherit;
        }}

        .repo-card p {{
            font-size: 0.95em;
            margin-bottom: 15px;
            min-height: 60px;
        }}

        .repo-links {{
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .btn {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.9em;
            transition: all 0.2s ease;
        }}

        .btn-primary {{
            background-color: var(--primary-color, #1976d2);
            color: white;
        }}

        .btn-primary:hover {{
            background-color: var(--primary-dark-color, #1565c0);
        }}

        .btn-secondary {{
            background-color: var(--code-background, #f5f5f5);
            color: var(--page-foreground-color, #333);
            border: 1px solid var(--separator-color, #ddd);
        }}

        .btn-secondary:hover {{
            background-color: var(--separator-color, #e0e0e0);
        }}

        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--separator-color, #e0e0e0);
            text-align: center;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div id="top">
        <div id="titlearea">
            <table cellspacing="0" cellpadding="0">
                <tbody>
                    <tr id="projectrow">
                        <td id="projectalign">
                            <div id="projectname">Roo Libraries</div>
                            <div id="projectbrief">API Documentation</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    <div id="doc-content">
        <div class="PageDoc">
            <div class="contents">
                <div class="textblock">
                    <p><strong>Welcome to the Roo Libraries API Documentation!</strong></p>
                    <p>The Roo libraries are a collection of Arduino-compatible C++ libraries for ESP32 and related microcontrollers.
                       They provide powerful tools for displays, UI, I/O, testing, and more.</p>
                    <p>This documentation is automatically generated from the source code using Doxygen.</p>
                </div>

                <h2 style="margin-bottom: 20px;">Available Libraries ({len(available_repos)})</h2>

                <div class="repo-grid">
"""
    
    for repo in available_repos:
        description = REPOS.get(repo, "API documentation")
        html += f"""
                    <div class="repo-card">
                        <h2>{repo}</h2>
                        <p>{description}</p>
                        <div class="repo-links">
                            <a href="{repo}/html/index.html" class="btn btn-primary">📚 API Docs</a>
                            <a href="https://github.com/dejwk/{repo}" class="btn btn-secondary" target="_blank">💻 GitHub</a>
                        </div>
                    </div>
"""
    
    html += f"""
                </div>

                <footer>
                    <p>Documentation generated on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>
                    <p>
                        View all repositories:
                        <a href="https://github.com/dejwk?tab=repositories&q=roo_" target="_blank">
                            github.com/dejwk
                        </a>
                    </p>
                    <p style="margin-top: 10px; font-size: 0.85em;">
                        Powered by <a href="https://www.doxygen.nl/" target="_blank">Doxygen</a> |
                        Hosted on <a href="https://pages.github.com/" target="_blank">GitHub Pages</a>
                    </p>
                </footer>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    index_path = os.path.join(output_dir, "index.html")
    with open(index_path, "w") as f:
        f.write(html)
    
    print(f"Generated index page: {index_path}")
    print(f"Found documentation for {len(available_repos)} repositories:")
    for repo in available_repos:
        print(f"  - {repo}")

if __name__ == "__main__":
    generate_index()
