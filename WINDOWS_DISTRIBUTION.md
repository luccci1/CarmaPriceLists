# Windows Distribution Guide

## 🪟 **Creating Windows Executable**

### **Option 1: Cross-Platform Build (Recommended)**

Since you're on macOS, you have a few options to create Windows executables:

#### **A. Use GitHub Actions (Free)**
1. Create a `.github/workflows/build.yml` file
2. Push to GitHub
3. GitHub will build Windows, macOS, and Linux versions automatically

#### **B. Use Docker (Cross-platform)**
```bash
# Run Windows build in Docker
docker run --rm -v "$(pwd)":/app -w /app python:3.11-windowsservercore python create_windows_exe.py
```

#### **C. Use Virtual Machine**
- Install Windows VM on your Mac
- Run the build script inside Windows

### **Option 2: Manual Windows Build**

If you have access to a Windows machine:

1. **Copy the project to Windows**
2. **Install Python 3.8+ on Windows**
3. **Run the build script:**
   ```cmd
   python create_windows_exe.py
   ```

---

## 📦 **What You'll Get**

### **Windows Executable:**
- `dist/PriceListConverter.exe` - Standalone Windows executable
- `install_windows.bat` - Windows installer script

### **Distribution Package:**
```bash
# Create Windows distribution zip
zip -r PriceListConverter_Windows.zip dist/PriceListConverter.exe install_windows.bat README.md QUICKSTART.md
```

---

## 👥 **For Windows Users**

### **Installation:**
1. Download and extract the zip file
2. Double-click `install_windows.bat`
3. The app will be installed to `%USERPROFILE%\PriceListConverter\`

### **Running:**
1. Navigate to `%USERPROFILE%\PriceListConverter\`
2. Double-click `PriceListConverter.exe`

---

## 🚀 **Quick Solution: Multi-Platform Distribution**

### **Send Both Versions:**
```bash
# Create macOS version
zip -r PriceListConverter_macOS.zip dist/PriceListConverter.app README.md QUICKSTART.md

# Create Windows version (when available)
zip -r PriceListConverter_Windows.zip dist/PriceListConverter.exe install_windows.bat README.md QUICKSTART.md
```

### **Universal Instructions:**
- **macOS users**: Use the `.app` file
- **Windows users**: Use the `.exe` file
- **Both**: Include source code as backup

---

## 🔧 **Alternative: Source Code Distribution**

For maximum compatibility, you can always distribute the source code:

```bash
# Create source distribution
zip -r PriceListConverter_Source.zip . -x "venv/*" "*.pyc" "__pycache__/*" "dist/*" "build/*"
```

**Instructions for users:**
1. Install Python 3.8+
2. Extract files
3. Run `python main.py`

---

## 📋 **Recommended Approach**

1. **Primary**: Distribute macOS `.app` file (since you're on Mac)
2. **Secondary**: Include source code for Windows users
3. **Future**: Set up automated cross-platform builds

This way, macOS users get the easy executable, and Windows users can run the source code! 🎯
