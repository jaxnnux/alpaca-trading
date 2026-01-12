import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { spawn, ChildProcess } from 'child_process';

let mainWindow: BrowserWindow | null = null;
let pythonProcess: ChildProcess | null = null;

const PYTHON_PORT = 8765;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
    titleBarStyle: 'default',
    icon: path.join(__dirname, '../../resources/icon.ico'),
  });

  if (process.env.NODE_ENV === 'development') {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

function startPythonBackend() {
  const pythonExecutable = app.isPackaged
    ? path.join(process.resourcesPath, 'engine', 'dist', 'main.exe')
    : 'python';

  const enginePath = app.isPackaged
    ? path.join(process.resourcesPath, 'engine')
    : path.join(__dirname, '../../engine');

  const args = app.isPackaged
    ? []
    : ['-m', 'uvicorn', 'src.alpacadesk_engine.main:app', '--port', PYTHON_PORT.toString()];

  pythonProcess = spawn(pythonExecutable, args, {
    cwd: enginePath,
    stdio: 'pipe',
  });

  pythonProcess.stdout?.on('data', (data) => {
    console.log(`[Python]: ${data}`);
  });

  pythonProcess.stderr?.on('data', (data) => {
    console.error(`[Python Error]: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
    pythonProcess = null;
  });
}

function stopPythonBackend() {
  if (pythonProcess) {
    pythonProcess.kill();
    pythonProcess = null;
  }
}

app.whenReady().then(() => {
  startPythonBackend();

  // Wait for Python backend to start
  setTimeout(createWindow, 2000);

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  stopPythonBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  stopPythonBackend();
});

// IPC Handlers
ipcMain.handle('get-python-port', () => {
  return PYTHON_PORT;
});
