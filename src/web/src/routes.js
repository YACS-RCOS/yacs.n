import VueRouter from "vue-router";
const AdminPage = () => import("./pages/Admin");
const StudentPage = () => import("./pages/Student");
const CourseSchedulerPage = () => import("./pages/NewCourseScheduler"); /**/
const UploadCsvPage = () => import("./pages/UploadCsv");
const EditSemestersPage = () => import("./pages/EditSemesters");
const CourseExplorerPage = () => import("./pages/CourseExplorer");
const CoursePage = () => import("./pages/CoursePage");
const GPACalculatorPage = () => import("./pages/GPACalculator");
const PathwayPage = () => import("./pages/Pathway");
const SubjectExplorerPage = () => import("./pages/SubjectExplorer");
const NotFoundPage = () => import("./pages/NotFound");
const FinalExamScheduler = () => import("./pages/FinalExamScheduler");

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
          path: "/GPACalc",
          component: GPACalculatorPage,
          name: "GPACalculator"
        },
        {
          path: "/pathway",
          component: PathwayPage,
          name: "Pathway",
        },
        {
          path: "/FinalExamScheduler",
          component: FinalExamScheduler,
          name: "Finals",
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
    {
      path: "*",
      component: NotFoundPage,
      name: "NotFound",
    },
  ],
  mode: "history",
});

export default router;
