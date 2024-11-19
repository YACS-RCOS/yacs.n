import VueRouter from "vue-router";
const AdminPage = () => import("./pages/Admin");
const StudentPage = () => import("./pages/Student");
const CourseSchedulerPage = () => import("./pages/NewCourseScheduler"); /**/
const UploadCsvPage = () => import("./pages/UploadCsv");
const EditSemestersPage = () => import("./pages/EditSemesters");
const CourseExplorerPage = () => import("./pages/CourseExplorer");
const CoursePage = () => import("./pages/CoursePage");
const ProfExplorer = () => import("./pages/ProfExplorer");
const ProfPage = () => import("./pages/ProfPage");
const DegreeTemplatesPage = () => import("./pages/DegreeTemplates");
const PathwayPage = () => import("./pages/Pathway");
const SubjectExplorerPage = () => import("./pages/SubjectExplorer");
const NotFoundPage = () => import("./pages/NotFound");
const FinalExamScheduler = () => import("./pages/FinalExamScheduler");
const AboutPage = () => import("./pages/About");
const FAQPage = () => import("./pages/FAQ");

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
        {
          path: "/professor",
          component: ProfExplorer,
          name: "Professors",
          props: true,
        },
        {
          path: "/professor/:rcs",
          component: ProfPage,
          name: "ProfPage",
          props: true,
        },
        {
          path: "/about",
          component: AboutPage,
          name: "About",
          props: true,
        },
        {
          path: "/faq",
          component: FAQPage,
          name: "FAQ",
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
