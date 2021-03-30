import VueRouter from "vue-router";
const AdminPage = () => import("./pages/Admin");
const StudentPage = () => import("./pages/Student");
const CourseSchedulerPage = () => import("./pages/CourseScheduler");
const UploadCsvPage = () => import("./pages/UploadCsv");
const EditSemestersPage = () => import("./pages/EditSemesters");
const CourseExplorerPage = () => import("./pages/CourseExplorer");
const CoursePage = () => import("./pages/CoursePage");
const DegreeTemplatesPage = () => import("./pages/DegreeTemplates");
const SubjectExplorerPage = () => import("./pages/SubjectExplorer");

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
        {
          path: "/explore/:subject",
          component: SubjectExplorerPage,
          name: "SubjectExplorer",
          props: true,
        },
        {
          path: "/explore/:subject/:course",
          component: CoursePage,
          name: "CoursePage",
          props: true,
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
