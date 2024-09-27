import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import vueRouter from "unplugin-vue-router/vite";
import { defineConfig } from "vite";
import checker from "vite-plugin-checker";
import { VitePWA } from "vite-plugin-pwa";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vueRouter({
      routesFolder: "src/views"
    }),
    vue(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        description: "YACS is a RPI course scheduler to help students plan out their semester.",
        display_override: ["window-controls-overlay"],
        display: "minimal-ui",
        theme_color: "#ff444c"
        // todo: add screenshots for richer pwa install
      },
      includeAssets: ["logo.svg"],
      pwaAssets: {
        config: true
      }
    }),
    checker({
      vueTsc: {
        tsconfigPath: "./tsconfig.app.json"
      },
      eslint: {
        lintCommand: "eslint .",
        useFlatConfig: true
      }
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url))
    }
  },
  server: {
    port: 8080,
    proxy: {
      "/api": {
        target: process.env.YACS_API_HOST ?? "http://localhost:5000",
        changeOrigin: true,
        secure: false
      }
    }
  }
});
