import VueRouter from "vue-router";
import AdminPage from "./pages/Admin";
import MainPage from "./pages/Main";
import UploadCsvPage from "./pages/UploadCsv";
import EditSemestersPage from "./pages/EditSemesters";

var router = new VueRouter({
  routes: [
    {
      path: "/",
      component: MainPage,
      name: "Schedule",
    },
    {
      path: "/Admin",
      component: AdminPage,
      name: "Admin",
    },
    {
      path: "/admin/csv",
      component: UploadCsvPage,
      name: "UploadCsv",
    },
    {
      path: "/admin/editsemesters",
      component: EditSemestersPage,
      name: "EditSemesters",
    },
  ],
  mode: "history",
});

export default router;
