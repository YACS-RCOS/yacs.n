import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import { defineConfig, loadEnv } from "vite";
import { VitePWA } from "vite-plugin-pwa";
import "./env.d.ts";

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd()) as ImportMetaEnv;

  return {
    plugins: [
      vue(),
      VitePWA({
        registerType: "autoUpdate",
        devOptions: { enabled: env.VITE_ENABLE_SW },
        workbox: {
          globPatterns: ["**/*.{js,css,html,ico,png,svg}"],
        },
        manifestFilename: "public/manifest.webmanifest",
        strategies: "generateSW",
      }),
    ],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    css: {
      preprocessorOptions: {
        scss: {
          additionalData:
            '@import "bootstrap/scss/_functions.scss"; @import "bootstrap/scss/_variables.scss"; @import "bootstrap/scss/_mixins.scss";',
        },
      },
    },
    server: {
      host: true,
      port: env.VITE_PORT,
      proxy: {
        "/api": {
          target: env.VITE_API_HOST || "http://localhost:5000",
          changeOrigin: true,
          secure: false,
        },
      },
    },
  };
});
