import VueRouter from 'vue-router';
import AdminPage from "./pages/Admin";
import MainPage from "./pages/Main";

var router = new VueRouter({
    routes: [
        {
            path: "/",
            component: MainPage
        },
        {
            path: "/Admin",
            component: AdminPage
        }
    ],
    mode: "history",
});

export default router;