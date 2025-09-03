# Building Windows Executable Guide

## 🚀 **Option 1: GitHub Actions (Recommended)**

### **Setup:**
1. **Push your code to GitHub**
2. **Create a release tag:**
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **GitHub will automatically build executables for Windows, macOS, and Linux**
4. **Download the Windows executable from the releases page**

---

## 🖥️ **Option 2: Windows VM/Remote Desktop**

### **Using Parallels/VMware:**
1. **Install Windows VM on your Mac**
2. **Copy project to Windows VM**
3. **Install Python 3.8+ on Windows**
4. **Run the build script:**
   ```cmd
   python create_windows_exe.py
   ```

### **Using Remote Desktop:**
1. **Use Windows cloud instance (AWS, Azure, etc.)**
2. **Copy project via SCP/SFTP**
3. **Build on Windows instance**

---

## 🐳 **Option 3: Docker (Cross-platform)**

### **Create Dockerfile:**
```dockerfile
FROM python:3.11-windowsservercore

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install pyinstaller

RUN pyinstaller --onefile --windowed --name=PriceListConverter main.py

CMD ["dir", "dist"]
```

### **Build with Docker:**
```bash
# Build Windows executable in Docker
docker build -t price-converter .
docker run --rm -v "$(pwd)/dist:/app/dist" price-converter
```

---

## 🔧 **Option 4: Online Build Services**

### **GitHub Codespaces:**
1. **Open project in GitHub Codespaces**
2. **Select Windows environment**
3. **Run build script**

### **Replit:**
1. **Import project to Replit**
2. **Use Windows environment**
3. **Build executable**

---

## 📦 **Option 5: Manual Windows Build**

### **If you have access to a Windows PC:**

1. **Copy project to Windows machine**
2. **Install Python 3.8+**
3. **Run build script:**
   ```cmd
   python create_windows_exe.py
   ```

---

## 🎯 **Recommended Approach**

**Use GitHub Actions** - it's free, automated, and builds for all platforms:

1. **Push code to GitHub**
2. **Create release tag**
3. **Download Windows executable from releases**
4. **Distribute to users**

This way you get Windows, macOS, and Linux executables automatically! 🚀

---

## 📋 **What You'll Get**

After building, you'll have:
- `PriceListConverter.exe` - Windows executable
- `install_windows.bat` - Windows installer
- Ready-to-distribute package

**Users just need to:**
1. Download the `.exe` file
2. Double-click to run
3. No Python installation required!
