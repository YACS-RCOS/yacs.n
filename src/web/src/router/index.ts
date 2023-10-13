import { createRouter, createWebHistory } from "vue-router";

import AdminPage from "@/pages/Admin.vue";
import StudentPage from "@/pages/Student.vue";
import CourseSchedulerPage from "@/pages/NewCourseScheduler.vue";
import UploadCsvPage from "@/pages/UploadCsv.vue";
import EditSemestersPage from "@/pages/EditSemesters.vue";
import CourseExplorerPage from "@/pages/CourseExplorer.vue";
import CoursePage from "@/pages/CoursePage.vue";
import ProfExplorer from "@/pages/ProfExplorer.vue";
import ProfPage from "@/pages/ProfPage.vue";
import DegreeTemplatesPage from "@/pages/DegreeTemplates.vue";
import PathwayPage from "@/pages/Pathway.vue";
import SubjectExplorerPage from "@/pages/SubjectExplorer.vue";
import NotFoundPage from "@/pages/NotFound.vue";
import FinalExamScheduler from "@/pages/FinalExamScheduler.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      path: "/*404",
      component: NotFoundPage,
      name: "NotFound",
    },
  ],
});

export default router;
