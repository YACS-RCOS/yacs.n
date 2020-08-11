import VueRouter from "vue-router";
import AdminPage from "./pages/Admin";
import StudentPage from "./pages/Student";
import CourseSchedulerPage from "./pages/CourseScheduler";
import UploadCsvPage from "./pages/UploadCsv";
import EditSemestersPage from "./pages/EditSemesters";
import CourseExplorerPage from "./pages/CourseExplorer";
import DegreeTemplatesPage from "./pages/DegreeTemplates";

var router = new VueRouter({
  routes: [
    {
      path: "/",
      component: StudentPage,
      props: true,
      children: [
        {
          path: "/",
          component: CourseSchedulerPage,
          name: "CourseScheduler",
          props: true,
        },
        {
          path: "/explore",
          component: CourseExplorerPage,
          name: "CourseExplorer",
          props: true,
        },
        {
          path: "/template",
          component: DegreeTemplatesPage,
          name: "DegreeTemplates",
        },
      ],
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
