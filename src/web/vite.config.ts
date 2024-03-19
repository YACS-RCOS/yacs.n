import vue from "@vitejs/plugin-vue";
import { fileURLToPath, URL } from "node:url";
import vueRouter from "unplugin-vue-router/vite";
import { defineConfig } from "vite";
import checker from "vite-plugin-checker";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vueRouter({
      routesFolder: "src/views"
    }),
    vue(),
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
    port: 8080
  }
});
