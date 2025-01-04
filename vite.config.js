import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

function glslLoader() {
  return {
    name: 'vite-plugin-glsl-loader',
    transform(code, id) {
      if (id.endsWith('.glsl')) {
        // Convert the GLSL file into a JS module exporting a string
        return {
          code: `export default ${JSON.stringify(code)};`,
          map: null
        };
      }
    }
  };
}

export default defineConfig({
  plugins: [react(), glslLoader()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  }
});
