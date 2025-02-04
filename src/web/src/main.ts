import "./assets/main.css";

import { createPinia } from "pinia";
import { createApp } from "vue";

import App from "@/App.vue";
import router from "@/router";
import Vue3Toastify, { type ToastContainerOptions } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const app = createApp(App as Parameters<typeof createApp>[0]);

app.use(createPinia());
app.use(router);
app.use(Vue3Toastify, {
  toastStyle: {
    color: "rgb(var(--colors-primary))",
    background: "rgb(var(--colors-on-primary))",
    zIndex: "100000"
  }
} as ToastContainerOptions);

app.mount("#app");
