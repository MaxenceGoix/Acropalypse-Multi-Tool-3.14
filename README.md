# Acropalypse Restoration & Detection Multi-Tool

### A modernized, cross-platform version of the original Acropalypse restoration tool

A tool to detect and restore PNG and GIF images affected by the **aCropalypse vulnerability**, discovered in 2023.

The vulnerability could cause cropped screenshots to retain image data that should have been permanently removed. In certain circumstances, this made it possible to recover parts of the original, uncropped image.

This project provides tools to detect potentially affected images in local folders and attempt to restore their original contents.

---

## ⚠️ About This Fork — Please Read

**I want to be completely transparent about the origin of this project.**

I did not create the original software, and I claim absolutely no credit for its original implementation.

All original development credits belong to:

**[frankthetank-music – Acropalypse-Multi-Tool](https://github.com/frankthetank-music/Acropalypse-Multi-Tool)**

This repository is simply my attempt to modernize and preserve that project.

The original version was based on Python 3.10 and was becoming inconvenient to use with newer Python environments. I wanted a more accessible version, with updated dependencies, improved usability, and better cross-platform support.

I used AI to carry out the modernization work, including code modifications, compatibility updates, and interface improvements.

To be clear:
- I did not write the original application.
- I take no credit for the original algorithms or restoration techniques.
- The modernization was performed with AI assistance.
- My contribution was essentially to initiate this update and provide a place where the project could continue to be accessible.

**All credits for the original project go to its original author and contributors.**

Please visit and support the original repository:

👉 https://github.com/frankthetank-music/Acropalypse-Multi-Tool

This fork is not an official continuation of the original project.

---

## Key Features

- Restore and detect both PNG and GIF formats.
- Support for PNG images with and without alpha channels (RGB and RGBA).
- Compatibility with images affected by Google Pixel Markup and Windows Snipping Tool.
- Support for different image resolutions and device presets.
- Detection of potentially vulnerable images in local folders.
- Batch scanning of directories.
- Improved graphical interface.
- Updated Python packaging and dependency management.
- Cross-platform development targeting Windows and Linux.

## Interface

The graphical interface provides two main tools:

- **DetectTool:** Scan folders and identify potentially affected images.
- **RestoreTool:** Attempt to reconstruct the original image data.

![Acropalypse Multi-Tool Interface](tool.png)

---

## Security Background — The aCropalypse Vulnerabilities

The aCropalypse vulnerability was publicly disclosed in March 2023.

It affected screenshot editing applications that did not correctly truncate image files after cropping or editing.

As a result, image data that users expected to be permanently deleted could remain in the underlying file.

Two major vulnerabilities are associated with this issue:

### CVE-2023-21036 — Google Pixel

Affected Google's Pixel screenshot editing application, **Markup**.

A logic error in the image export process could prevent the file from being properly truncated after editing.

Consequently, the original image data could remain recoverable even after cropping.

- Platform: Google Pixel / Android
- Component: Markup
- Impact: Potential disclosure of information users believed they had removed.

References:
- [NVD – CVE-2023-21036](https://nvd.nist.gov/vuln/detail/CVE-2023-21036)
- [Android Security Bulletin – March 2023](https://source.android.com/docs/security/bulletin/2023-03-01)

### CVE-2023-28303 — Microsoft Windows

Affected Microsoft's screenshot applications:

- Snip & Sketch (Windows 10)
- Snipping Tool (Windows 11)

The applications could fail to properly remove cropped image data when overwriting an existing image.

This could allow someone with access to the resulting image file to recover information from the original screenshot.

- Platform: Windows 10 / Windows 11
- Components: Snip & Sketch and Snipping Tool
- Impact: Information disclosure.

References:
- [Microsoft Security Response Center – CVE-2023-28303](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-28303)
- [NVD – CVE-2023-28303](https://nvd.nist.gov/vuln/detail/CVE-2023-28303)

**Important:** These vulnerabilities have been addressed by security updates. This application is intended for recovering eligible legacy images and testing, not for exploiting systems.

---

## Getting Started

### Requirements

- Python 3.10 or newer.
- Windows or Linux.
- Required Python dependencies.
- Rust toolchain for building the optional native GIF component.

The project is being modernized to support newer Python versions. Compatibility should be verified against the actual release and CI build results.

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
pip install -r requirements.txt
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
pip install -r requirements.txt
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

### Building the Native GIF Component

If you need the native GIF restoration functionality, install Rust and Maturin:

```bash
pip install maturin
pip install .
```

This builds and installs the native Python extension.

For more detailed build instructions, see [BUILD.md](BUILD.md).

---

## How to Use RestoreTool

1. **Select Image:** Click the image selection button and choose a PNG or GIF file.
2. **Choose Preset:** Select the appropriate preset corresponding to the original device or screenshot application.
3. **Set Original Dimensions:** If using a custom preset, manually enter the original image width and height.
4. **Restore Image:** Start the restoration process.
5. **Save Image:** Save the reconstructed image to your preferred location.

The success of restoration depends on the original image, its format, the cropping operation, and the information still available in the file.

Not every cropped image can be restored.

## How to Use DetectTool

1. Open the detection interface.
2. Select the folder containing the images you want to inspect.
3. Start the scanning process.
4. Review the results to identify potentially affected files.

Detection results should be treated as indications rather than guarantees of successful restoration.

---

## Original Project & References

This project builds upon the work of the original author and the following research and implementations:

- **Original Multi-Tool:** https://github.com/frankthetank-music/Acropalypse-Multi-Tool
- **David Buchanan's original research:** https://gist.github.com/DavidBuchanan314/93de9d07f7fab494bcdf17c2bd6cef02
- **GIF restoration implementation:** https://github.com/heriet/acropalypse-gif

All original credits belong to their respective authors.

Please refer to the original repositories for their respective licenses and attribution requirements.

---

## Troubleshooting

If an error occurs during restoration:

1. Check that all dependencies are installed.
2. Verify that the image format is supported.
3. Check that the original dimensions and device preset are correct.
4. If using GIF restoration, verify that the native extension has been built and installed.
5. If the problem persists, open a GitHub issue with the error message and reproduction steps.

---

## Disclaimer

This software is provided for educational, research, and image recovery purposes.

Restoration is not guaranteed. Results depend on the image format, file contents, and the extent to which the original image data remains available.

Use this software only on images you own or are authorized to inspect.

**This repository is an AI-assisted modernization of an existing open-source project. It is not an original implementation, and no ownership of the original work is claimed.**

Once again, all original development credits go to:

**[frankthetank-music](https://github.com/frankthetank-music/Acropalypse-Multi-Tool)**

Thank you for creating and sharing the original project.
