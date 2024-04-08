import { fileURLToPath, URL } from 'node:url';
import vuetify from 'vite-plugin-vuetify';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import fs from 'fs';
import https from 'https';

const devURLBase = 'https://127.0.0.1:8000/';

/* eslint-disable */
export default defineConfig(({ command, mode }) => {
  /* eslint-enable */
  // base configuration: used in both development and production:
  const baseConfig = {
    plugins: [vue(), vuetify({ autoImport: true })],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  };
  if (command === 'serve') {
    // development configuration: base configuration extended for configuratiion used only in development
    return {
      ...baseConfig,
      server: {
        https: {
          key: fs.readFileSync('../../key.pem'),
          cert: fs.readFileSync('../../cert.pem'),
        },
        proxy: {
          '/api/': {
            target: devURLBase,
            changeOrigin: true,
            ws: true,
            // to avoid error: read ECONNRESET
            // at TLSWrap.onStreamRead (node:internal/stream_base_commons:220:20)
            // more info: https://github.com/vitejs/vite/issues/4794
            agent: new https.Agent(),
          },
          '/static/': {
            target: devURLBase,
            changeOrigin: true,
            ws: true,
            // to avoid error: read ECONNRESET
            // at TLSWrap.onStreamRead (node:internal/stream_base_commons:220:20)
            // more info: https://github.com/vitejs/vite/issues/4794
            agent: new https.Agent(),
          },
          '/media/': {
            target: devURLBase,
            changeOrigin: true,
            ws: true,
            // to avoid error: read ECONNRESET
            // at TLSWrap.onStreamRead (node:internal/stream_base_commons:220:20)
            // more info: https://github.com/vitejs/vite/issues/4794
            agent: new https.Agent(),
          },
        },
        // to disable error overlay that Vue uses in development mode:
        // hmr: {
        //   overlay: process.env.BUILD == "yes" ? false : { errors: false },
        // },
      },
    };
  } else {
    return baseConfig;
  }
});
