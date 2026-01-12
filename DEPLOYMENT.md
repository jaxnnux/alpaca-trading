# AlpacaDesk Deployment Guide

**Version:** 1.0.0
**Last Updated:** January 12, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Development Environment Setup](#development-environment-setup)
4. [Building for Production](#building-for-production)
5. [Testing the Build](#testing-the-build)
6. [Distribution](#distribution)
7. [User Installation](#user-installation)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide covers deploying AlpacaDesk from development to production, including building installers, distribution, and user installation procedures.

### Deployment Checklist

- [ ] Development environment verified
- [ ] All tests passing
- [ ] Version numbers updated
- [ ] Production build successful
- [ ] Installer tested on clean Windows machine
- [ ] Documentation updated
- [ ] Release notes prepared

---

## Prerequisites

### Development Machine Requirements
- **OS:** Windows 10/11 (64-bit) or WSL2
- **Node.js:** 18.x or higher
- **Python:** 3.10 or higher
- **Git:** Latest version
- **Disk Space:** 2GB+ free space

### Build Tools
```bash
# Check Node.js version
node --version  # Should be v18.x or higher

# Check Python version
python --version  # Should be 3.10 or higher

# Check npm
npm --version
```

---

## Development Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd alpaca-trading
```

### 2. Install Dependencies

```bash
# Install JavaScript dependencies
npm install

# Install Python dependencies
cd engine
pip install -e ".[dev]"
cd ..
```

### 3. Verify Development Build

```bash
# Run in development mode
npm run dev

# This should:
# 1. Start Vite dev server (port 5173)
# 2. Start Python FastAPI server (port 8765)
# 3. Launch Electron application
```

### 4. Run Tests (if available)

```bash
# Frontend tests
npm test

# Backend tests
cd engine
pytest
cd ..
```

---

## Building for Production

### 1. Pre-Build Checklist

#### Update Version Numbers

**package.json:**
```json
{
  "name": "alpacadesk",
  "version": "1.0.0",
  "description": "Native Windows Algorithmic Trading Application"
}
```

**engine/pyproject.toml:**
```toml
[project]
name = "alpacadesk-engine"
version = "1.0.0"
```

#### Verify Configuration

**electron.vite.config.ts:**
- Check build paths
- Verify external dependencies
- Confirm Python bundling settings

**electron-builder.yml** (if exists):
- Verify app ID
- Check code signing config
- Confirm installer settings

### 2. Build Production Bundle

```bash
# Clean previous builds
npm run clean  # or manually delete dist/ and release/

# Build production version
npm run build

# This will:
# 1. Build React frontend (Vite)
# 2. Bundle Python backend (PyInstaller)
# 3. Create Electron installer
# 4. Output to release/ directory
```

### 3. Build Output

The build process creates:

```
release/
├── AlpacaDesk Setup 1.0.0.exe    # Windows installer
├── win-unpacked/                  # Unpacked application (for testing)
│   ├── AlpacaDesk.exe
│   ├── resources/
│   │   ├── app.asar              # Frontend code
│   │   └── engine/               # Python backend
│   └── ...                        # Electron runtime
└── builder-debug.yml              # Build metadata
```

### 4. Build Configuration Details

#### Frontend Build (Vite)
- Minification: enabled
- Source maps: disabled in production
- Code splitting: automatic
- Asset optimization: images, fonts

#### Backend Build (Python)
- PyInstaller creates standalone executable
- Bundles Python runtime + dependencies
- SQLite included
- No Python installation required on user machine

#### Electron Packaging
- ASAR archive for frontend code
- NSIS installer for Windows
- One-click installation experience
- Start menu shortcuts created

---

## Testing the Build

### 1. Test on Development Machine

```bash
# Run the unpacked application
cd release/win-unpacked
./AlpacaDesk.exe

# Verify:
# - Application launches
# - Login works with test credentials
# - All features functional
# - No console errors
# - Database creates properly (~/.alpacadesk/alpacadesk.db)
```

### 2. Test the Installer

```bash
# Run installer
cd release
./AlpacaDesk Setup 1.0.0.exe

# During installation:
# - Accept license
# - Choose install location
# - Create desktop shortcut
# - Launch after install

# Verify:
# - Installed to C:\Program Files\AlpacaDesk
# - Start menu entry created
# - Desktop shortcut works
# - Uninstaller available
```

### 3. Clean Machine Testing

**Critical:** Test on a fresh Windows installation or VM:

```
Required testing:
✓ Install from .exe installer
✓ First launch experience
✓ Login with Alpaca credentials
✓ Create and run strategy
✓ Run backtest
✓ Check execution quality
✓ Modify settings
✓ Restart application (persistence)
✓ Uninstall completely
```

**Test Environment:**
- Windows 10/11 fresh install
- No Node.js or Python installed
- No development tools
- Regular user account (not admin)

---

## Distribution

### 1. Release Preparation

#### Create Release Notes

**RELEASE_NOTES_v1.0.0.md:**
```markdown
# AlpacaDesk v1.0.0 Release Notes

## New Features
- Visual strategy builder with drag-and-drop
- 4 pre-built trading strategies
- Professional backtesting engine
- Real-time market data streaming
- Execution quality monitoring
- Comprehensive settings management

## System Requirements
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB disk space
- Internet connection

## Installation
1. Download AlpacaDesk Setup 1.0.0.exe
2. Run installer
3. Follow setup wizard
4. Launch application

## Getting Started
1. Sign up for Alpaca account at alpaca.markets
2. Generate paper trading API keys
3. Launch AlpacaDesk
4. Enter credentials and connect
5. Explore pre-built strategies

## Known Issues
- None

## Support
- Documentation: See README_COMPLETE.md
- Issues: [GitHub repository URL]
```

#### Package Distribution Files

```
distribution/
├── AlpacaDesk Setup 1.0.0.exe     # Installer
├── README.txt                      # Quick start
├── RELEASE_NOTES.txt               # What's new
└── LICENSE.txt                     # License agreement
```

### 2. Distribution Channels

#### Option 1: Direct Distribution
- Host installer on website
- Provide direct download link
- Include checksum for verification

```bash
# Generate checksum
certutil -hashfile "AlpacaDesk Setup 1.0.0.exe" SHA256
```

#### Option 2: GitHub Releases
1. Create new release on GitHub
2. Tag version (v1.0.0)
3. Upload installer
4. Add release notes
5. Mark as latest release

#### Option 3: Microsoft Store (Future)
- Requires Microsoft developer account
- App submission process
- Store review (1-3 days)
- Wider distribution

### 3. Code Signing (Recommended)

**Why Code Sign:**
- Prevents "Unknown Publisher" warnings
- Builds user trust
- Required for some distribution channels

**How to Sign:**
1. Obtain code signing certificate (DigiCert, Sectigo)
2. Configure electron-builder:

```json
{
  "win": {
    "certificateFile": "path/to/cert.pfx",
    "certificatePassword": "CERT_PASSWORD"
  }
}
```

3. Rebuild with signing:
```bash
npm run build
```

**Note:** Code signing certificates cost $100-400/year

---

## User Installation

### Standard Installation

1. **Download Installer**
   - Get `AlpacaDesk Setup 1.0.0.exe` from distribution source
   - Verify checksum (optional but recommended)

2. **Run Installer**
   - Double-click installer
   - Windows may show SmartScreen warning (if not code-signed)
   - Click "More info" → "Run anyway"

3. **Installation Wizard**
   - Accept license agreement
   - Choose installation directory (default: C:\Program Files\AlpacaDesk)
   - Select additional tasks:
     - ✓ Create desktop shortcut
     - ✓ Add to Start Menu
   - Click Install

4. **First Launch**
   - Application launches automatically (or from Start Menu)
   - Login screen appears
   - Enter Alpaca API credentials
   - Select Paper Trading mode
   - Click Connect

### Installation Directories

```
C:\Program Files\AlpacaDesk\        # Application files
C:\Users\{username}\.alpacadesk\    # User data
  ├── alpacadesk.db                 # SQLite database
  └── logs\                         # Application logs
```

### Uninstallation

**Method 1: Control Panel**
1. Open Control Panel
2. Programs > Uninstall a program
3. Select AlpacaDesk
4. Click Uninstall

**Method 2: Start Menu**
1. Right-click AlpacaDesk in Start Menu
2. Select Uninstall

**Note:** User data in `~/.alpacadesk/` is preserved. Manually delete if needed.

---

## Troubleshooting

### Build Issues

#### Issue: "Python not found"
```bash
# Verify Python installation
python --version

# Add Python to PATH if needed
# Windows: System Properties → Environment Variables → Path
```

#### Issue: "Node modules missing"
```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

#### Issue: "Build fails during packaging"
```bash
# Check logs in release/builder-debug.yml
# Verify disk space (need 2GB+)
# Try building with elevated permissions
```

### Installation Issues

#### Issue: "Application won't start"
**Solution:**
1. Check Windows Event Viewer for errors
2. Verify Windows 10/11 (64-bit)
3. Try running as administrator
4. Check antivirus didn't quarantine files

#### Issue: "Missing DLL errors"
**Solution:**
- Install Visual C++ Redistributable
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

#### Issue: "Database errors"
**Solution:**
```bash
# Reset database
# 1. Close application
# 2. Delete C:\Users\{username}\.alpacadesk\alpacadesk.db
# 3. Restart application
```

### Runtime Issues

#### Issue: "Cannot connect to Alpaca"
**Solution:**
1. Verify API keys are correct
2. Check internet connection
3. Verify Alpaca service status
4. Try paper trading first

#### Issue: "Strategies not executing"
**Solution:**
1. Check scheduler is started
2. Verify strategy is enabled
3. Check market hours (9:30 AM - 4:00 PM ET)
4. Review logs in ~/.alpacadesk/logs/

#### Issue: "Backtest fails"
**Solution:**
1. Verify date range (not too far back)
2. Check symbol validity
3. Ensure sufficient data available
4. Try smaller date range first

---

## Maintenance

### Version Updates

#### Semantic Versioning
- **Major (1.x.x):** Breaking changes
- **Minor (x.1.x):** New features, backward compatible
- **Patch (x.x.1):** Bug fixes

#### Update Process
1. Update version in package.json
2. Update version in pyproject.toml
3. Update CHANGELOG.md
4. Build new installer
5. Test thoroughly
6. Create GitHub release
7. Notify users

### Auto-Update (Future Enhancement)

**electron-updater integration:**
```typescript
import { autoUpdater } from 'electron-updater';

autoUpdater.checkForUpdatesAndNotify();
```

Requires:
- Update server or GitHub releases
- Code signing certificate
- Proper versioning

---

## Security Considerations

### Distribution Security
- ✅ Code signing (prevents tampering)
- ✅ HTTPS for downloads
- ✅ Checksum verification
- ✅ Reproducible builds

### User Security
- ✅ Credentials stored in Windows Credential Manager
- ✅ No cloud transmission of API keys
- ✅ Local database encryption (Windows DPAPI)
- ✅ HTTPS for all API calls

### Best Practices
1. Always code sign production builds
2. Provide checksums for verification
3. Use HTTPS for all distribution
4. Keep dependencies updated
5. Monitor for security advisories

---

## Production Checklist

Before releasing to users:

### Code Quality
- [ ] All features tested
- [ ] No console errors
- [ ] Performance verified
- [ ] Memory leaks checked

### Documentation
- [ ] README.md updated
- [ ] CHANGELOG.md current
- [ ] Release notes prepared
- [ ] User guide complete

### Build
- [ ] Version bumped
- [ ] Production build successful
- [ ] Installer tested
- [ ] Code signed (recommended)

### Testing
- [ ] Clean machine tested
- [ ] All features working
- [ ] Database persistence verified
- [ ] Uninstall tested

### Distribution
- [ ] Checksums generated
- [ ] Release notes published
- [ ] Download links working
- [ ] Support channels ready

---

## Support

### For Developers
- Development guide: See DEVELOPMENT.md
- API documentation: See README_COMPLETE.md
- Architecture: See ALPACADESK_PRD_v1.1.md

### For Users
- Quick start: See QUICKSTART.md
- Features guide: See README_COMPLETE.md
- Troubleshooting: This document
- Support: [Support channel URL]

---

## Appendix

### Useful Commands

```bash
# Development
npm run dev                 # Start dev environment
npm test                    # Run tests

# Building
npm run build              # Production build
npm run build:clean        # Clean build from scratch

# Utilities
npm run lint               # Lint code
npm run format             # Format code
npm run type-check         # TypeScript check

# Database
sqlite3 ~/.alpacadesk/alpacadesk.db  # Open database
```

### Build Configuration Files

```
electron.vite.config.ts    # Electron Vite configuration
vite.config.ts             # Vite configuration
tsconfig.json              # TypeScript configuration
engine/pyproject.toml      # Python project configuration
```

### Environment Variables

```bash
# Development
NODE_ENV=development       # Enable dev mode
VITE_API_URL=http://localhost:8765  # API endpoint

# Production
NODE_ENV=production        # Production optimizations
```

---

**Last Updated:** January 12, 2026
**Version:** 1.0.0
**Status:** Production Ready

---

*For questions or issues, please refer to the support documentation or contact the development team.*
