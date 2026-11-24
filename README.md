# Acropalypse Multi-Tool 3.14

### PNG & GIF Detection, Restoration and Recovery

A modernized, cross-platform fork of the original Acropalypse Multi-Tool.

This application helps detect and attempt to restore PNG and GIF images affected by the **aCropalypse vulnerabilities** discovered in 2023.

These vulnerabilities could cause cropped screenshots to retain image data that users expected to have been permanently removed. In certain circumstances, parts of the original, uncropped image could therefore be recovered.

The application provides a graphical interface for scanning folders, identifying potentially affected images, and attempting image reconstruction.

---

## ⚠️ About This Fork & Credits

**Let's be clear: I take absolutely no credit for the original project.**

The original application was created by **Frank Weber (frankthetank-music)**.

All credits for the original implementation, research, algorithms and development belong to the original author and the respective contributors.

Original repository:

**https://github.com/frankthetank-music/Acropalypse-Multi-Tool**

So, why does this fork exist?

The original project was based on Python 3.10, and I wanted a version that would be easier to use with newer Python environments. I also wanted to improve the interface and make the project easier to install, build and preserve.

I used AI to carry out the modernization work.

My involvement was essentially:
- Forking the original project.
- Asking AI to modernize the codebase.
- Improving the graphical interface.
- Updating the Python packaging and build configuration.
- Adding cross-platform build automation.
- Preserving the project in a repository that I can easily maintain and access.

**I did not create the original software. I am not claiming authorship of its original code or restoration techniques.**

This is an unofficial, AI-assisted modernization and preservation effort.

If you find this tool useful, please also visit the original repository and give credit to its creator.

---

## What's New in This Fork?

### 1. Redesigned Graphical Interface

The original interface has been replaced with a redesigned desktop application.

The new interface uses a single window with two dedicated tabs:

- **Detection:** Scan folders for potentially affected PNG and GIF files.
- **Restoration:** Load an image, configure its original dimensions, preview the source and reconstructed images, and save the result.

Other interface improvements include:

- Dark-themed interface.
- Resizable application window.
- Side-by-side image previews.
- More accessible restoration controls.
- Device and screenshot presets.
- Editable original image dimensions.
- Explicit save-result action.
- Progress indication during long-running operations.

### 2. Improved Image Detection

The detection tool can recursively scan a selected directory and its subdirectories.

Supported detection formats:

- PNG
- GIF (requires the native GIF extension)

For PNG files, the detector checks whether additional data exists after the normal PNG `IEND` chunk.

For GIF files, detection is provided by the native Rust extension.

Double-clicking a detection result opens the corresponding file using the operating system's default application.

**Important:** Detection results indicate potentially affected files. They do not guarantee that an image is vulnerable or that it can be successfully restored.

### 3. Improved Image Restoration Workflow

The restoration interface provides:

- PNG and GIF image selection.
- Original image dimension configuration.
- Presets for supported screenshot sources and Google Pixel devices.
- Custom RGB and RGBA configurations.
- Original image preview.
- Reconstructed image preview.
- Dedicated reconstruction and save buttons.

Available presets include:

- Windows 11 Snipping Tool
- Google Pixel 3 / 3 XL / 3a / 3a XL
- Google Pixel 4 / 4 XL / 4a
- Google Pixel 5 / 5a
- Google Pixel 6 / 6 Pro / 6a
- Google Pixel 7 / 7 Pro
- Custom RGB
- Custom RGBA

The original dimensions are important for reconstruction. Incorrect dimensions or an incorrect preset may produce an inaccurate result.

### 4. Improved Processing

Several internal improvements have also been introduced:

- Long-running detection and restoration operations run in background threads.
- GUI updates are handled through the Tkinter main thread.
- Unique temporary output paths are used to avoid conflicts between simultaneous or successive operations.
- Improved error handling and status reporting.
- Cleaner separation between the graphical interface and the underlying restoration code.

### 5. Modernized Python Packaging

The project now uses a modern Python packaging configuration through `pyproject.toml`.

Main changes:

- Updated Pillow dependency.
- Maturin-based native extension compilation.
- PyO3 integration for the Rust GIF component.
- Removal of old precompiled `.pyd` and `.so` binaries.
- Improved installation workflow.

The old native binaries were platform- and Python-version-specific. The new approach builds the extension for the active Python environment.

### 6. Cross-Platform Build Automation

A GitHub Actions workflow has been added to automate native GIF extension builds.

The workflow targets:

| Platform | Python versions |
|---|---|
| Windows | 3.10, 3.11, 3.12, 3.13, 3.14 |
| Linux | 3.10, 3.11, 3.12, 3.13, 3.14 |

Builds are triggered by pushes, pull requests and manual workflow execution.

Generated wheels are uploaded as GitHub Actions artifacts.

This automation is intended to simplify distribution and installation across supported environments.

---

## Security Background — The aCropalypse Vulnerabilities

The aCropalypse vulnerabilities were publicly disclosed in March 2023.

They affected screenshot editing applications that did not correctly truncate image files after cropping or editing.

As a result, information that users believed had been removed could remain inside the resulting image file.

### CVE-2023-21036 — Google Pixel

This vulnerability affected Google's Pixel Markup screenshot editing application.

A flaw in the image editing and saving process could leave parts of the original image data in the resulting file.

Affected platform:
- Google Pixel devices.

Reference:
- [NVD — CVE-2023-21036](https://nvd.nist.gov/vuln/detail/CVE-2023-21036)
- [Android Security Bulletin — March 2023](https://source.android.com/docs/security/bulletin/2023-03-01)

### CVE-2023-28303 — Microsoft Windows

This vulnerability affected Microsoft's screenshot applications:

- Snip & Sketch on Windows 10.
- Snipping Tool on Windows 11.

Under certain circumstances, the applications could fail to properly truncate an image after editing or cropping.

This could leave original image data recoverable.

Reference:
- [Microsoft Security Response Center — CVE-2023-28303](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-28303)
- [NVD — CVE-2023-28303](https://nvd.nist.gov/vuln/detail/CVE-2023-28303)

**Note:** Security updates have been released for the affected software. This tool is intended for image recovery, research and educational purposes.

---

## Requirements

| Component | Requirement |
|---|---|
| Python | 3.10–3.14 |
| Operating systems | Windows 10/11 and Linux |
| GUI | Tkinter |
| Image processing | Pillow 11.0 or newer |
| Native GIF support | Rust stable + Maturin |
| Packaging | PyInstaller (optional) |

Tkinter must be available in your Python installation.

On some Linux distributions, you may need to install it separately:

```bash
sudo apt install python3-tk
```

---

## Installation

### Windows

Clone the repository:

```powershell
git clone https://github.com/MaxenceGoix/Acropalypse-Multi-Tool-3.14.git
cd Acropalypse-Multi-Tool-3.14
```

Create a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Launch the application:

```powershell
python gui.py
```

Alternatively, use the provided launcher:

```powershell
.\run_windows.bat
```

### Linux

Clone the repository:

```bash
git clone https://github.com/MaxenceGoix/Acropalypse-Multi-Tool-3.14.git
cd Acropalypse-Multi-Tool-3.14
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Launch the application:

```bash
python gui.py
```

Alternatively:

```bash
chmod +x run_linux.sh
./run_linux.sh
```

### What works with the basic installation?

The basic Python installation provides:

- The graphical interface.
- PNG detection.
- PNG reconstruction.
- Image previews and saving.

**GIF detection and restoration require the native Rust extension to be compiled and installed.**

---

## Enabling GIF Support

The GIF component is written in Rust and exposed to Python through PyO3.

The previous precompiled native binaries have been removed. The extension must now be built for your operating system and Python environment.

### Prerequisites

Install Rust using rustup:

https://rustup.rs/

Then install Maturin:

```bash
python -m pip install --upgrade maturin
```

From the root of the repository, build and install the extension:

```bash
python -m pip install .
```

This compiles the native GIF module for the active Python environment.

Restart the application:

```bash
python gui.py
```

For additional build information, see [BUILD.md](BUILD.md).

---

## Building Standalone Applications

The project includes a PyInstaller packaging script.

This allows you to create an executable that does not require users to manually install Python.

Install PyInstaller:

```bash
python -m pip install pyinstaller
```

Run:

```bash
python package_app.py
```

The generated application will be placed in the `dist/` directory.

**Important:** PyInstaller builds must be performed on the target operating system.

- Build on Windows to generate a Windows executable.
- Build on Linux to generate a Linux executable.

Cross-compilation between Windows and Linux is not supported by this packaging workflow.

For GIF support, compile and install the native extension before packaging.

---

## Running Tests

The repository includes basic smoke tests.

Run them with:

```bash
python -m unittest discover -s tests -v
```

The current smoke test checks that the demo PNG files can be processed by the PNG detector.

The test suite is intentionally small and does not constitute complete validation of every restoration scenario or operating system.

---

## Project Structure

```text
Acropalypse-Multi-Tool-3.14/
│
├── .github/
│   └── workflows/
│       └── build.yml
│
├── demo-images/
│
├── gif_lib/
│   ├── __init__.py
│   └── gif_lib_src/
│       ├── Cargo.toml
│       └── src/
│           └── lib.rs
│
├── tests/
│   └── test_smoke.py
│
├── acropalypse.py
├── gui.py
├── package_app.py
├── pyproject.toml
├── requirements.txt
├── run_linux.sh
├── run_windows.bat
├── BUILD.md
├── LICENSE
└── README.md
```

---

## Troubleshooting

### Tkinter is missing

On Debian/Ubuntu:

```bash
sudo apt install python3-tk
```

### GIF support is unavailable

Make sure Rust and Maturin are installed, then run:

```bash
python -m pip install .
```

Make sure you use the same virtual environment to install the extension and launch the application.

### Rust compilation fails

Update your Rust toolchain:

```bash
rustup update
```

Then retry the installation.

### Restoration does not produce the expected result

Check the following:

- The original image dimensions.
- The selected device preset.
- Whether the source image is actually affected by a supported vulnerability.
- Whether the file still contains enough data for reconstruction.

Not every cropped image can be restored.

---

## Limitations

This application is specialized in certain PNG and GIF files affected by the aCropalypse-related image editing issues.

It is not a general-purpose image recovery tool.

Successful reconstruction depends on:
- The original image format.
- The application or device that created the image.
- The original image dimensions.
- The data remaining in the edited file.

Detection does not guarantee successful reconstruction.

The compatibility matrix describes the intended build targets; actual runtime compatibility should be confirmed through CI results and testing on the target system.

---

## Original Research & Acknowledgements

This fork is based on the original work and research of:

- **Frank Weber:** [Original Acropalypse Multi-Tool](https://github.com/frankthetank-music/Acropalypse-Multi-Tool)
- **David Buchanan:** [Original aCropalypse research](https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02)
- **Heriet:** [Acropalypse GIF implementation](https://github.com/heriet/acropalypse-gif)

All original credits belong to their respective authors and contributors.

The original MIT license and copyright notices are retained in this repository. Please consult [LICENSE](LICENSE) for the applicable license terms.

---

## Disclaimer

This project is provided for educational, research and image recovery purposes.

No guarantee is made that a particular image can be detected or restored successfully.

Only use this software on images you own or are authorized to inspect.

This repository is an unofficial, AI-assisted modernization of an existing project. It does not claim authorship of the original implementation.

**All credit for the original project belongs to Frank Weber and the original contributors.**

Original project: https://github.com/frankthetank-music/Acropalypse-Multi-Tool

