import FontAwesome from "@/plugins/fontawesome-vue";
import VueBootstrap from "bootstrap-vue-next";
import { createApp } from "vue";
import VueCookies from "vue-cookies";
import { createMetaManager, deepestResolver, defaultConfig } from "vue-meta";
import VueVirtualScroller from "vue-virtual-scroller";
import App from "./App.vue";
import store from "./store";
import router from "./router";

// import "mutationobserver-shim";
import "vue-virtual-scroller/dist/vue-virtual-scroller.css";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";
// import "./plugins/bootstrap-vue";
// import "./plugins/fontawesome-vue";
// import "./registerServiceWorker";

const app = createApp(App);

app.use(router);
app.use(VueBootstrap);
app.use(VueCookies);
app.use(store);
app.use(VueVirtualScroller);
app.use(createMetaManager(defaultConfig, deepestResolver.resolve));
app.component("font-awesome-icon", FontAwesome);

app.mount("#app");
