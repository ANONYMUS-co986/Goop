import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { fileURLToPath } from 'node:url';

// absolute path to the reel videos (kept out of the app bundle —
// served by the dev server via /@fs so the repo isn't doubled)
const ARSENAL_FS = fileURLToPath(new URL('../studio/drops/FINALE/videos', import.meta.url));

export default defineConfig({
  plugins: [react()],
  define: {
    __ARSENAL_FS__: JSON.stringify(ARSENAL_FS),
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['.e2b.app', '.e2b.dev'],
    fs: { allow: ['..'] },
  },
  preview: { host: '0.0.0.0', port: 4174, allowedHosts: ['.e2b.app', '.e2b.dev'] },
});
