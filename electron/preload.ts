import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electron', {
  getPythonPort: () => ipcRenderer.invoke('get-python-port'),
});

// Type definitions for window.electron
export interface ElectronAPI {
  getPythonPort: () => Promise<number>;
}

declare global {
  interface Window {
    electron: ElectronAPI;
  }
}
