import {
  computed,
  ComputedRef,
  effect,
  reactive,
  ref,
  watch,
  watchEffect,
} from "vue";
import {
  getCourses,
  getDefaultSemester,
  getSemester,
} from "../plugins/axios/api";
import yacs from "./local";

/**
 *
 */
(() => {
  getSemester().then((semesters) => {
    semesters.forEach((semester) => {
      yacs.semesters[semester.semester] =
        yacs.semesters[semester.semester] || {};
    });
  });
  if (!yacs.currentSemester) {
    getDefaultSemester().then((res: any) => {
      yacs.currentSemester = yacs.currentSemester || res;
    });
  }
})();

const parseSession = (sessions: any[]): number[] => {
  try {
    return sessions.reduce(
      (arr, session) => {
        const a = session["time_start"]
          .split(":")
          .map((x: string) => Number.parseInt(x));
        const b = session["time_end"]
          .split(":")
          .map((y: string) => Number.parseInt(y));
        const duration = Math.abs(
          (b[0] - a[0]) * 2 + (a[1] < 30 ? 1 : 0) + (b[1] >= 30 ? 1 : 0)
        );
        const end = (20 - b[0]) * 2 + (b[1] < 30 ? 1 : 0);
        arr[session["day_of_week"]] |= ((1 << duration) - 1) << end;
        return arr;
      },
      [0, 0, 0, 0, 0]
    );
  } catch (e) {
    // console.warn('session missing essential attributes!')
    return [0, 0, 0, 0, 0];
  }
};

const userFilter = reactive({
  text: "",
  department: "",
});

const defaultCourses = ref(["Data Structures"]);

const courses: {
  dictionary: Map<string, any>;
  courseList: any[];
} = reactive({
  dictionary: new Map(),
  courseList: [],
});

/**
 *
 */
watchEffect(() => {
  const newCourseMap = new Map();
  getCourses(yacs.currentSemester).then((data) => {
    data.forEach((course) => {
      const sections = new Map();
      course.sections.forEach((section) => {
        section &&
          sections.set(
            section.crn,
            Object.assign(section, {
              sessions: parseSession(section.sessions),
            })
          );
      });
      newCourseMap.set(
        course.full_title || course.title,
        Object.assign(course, { sections })
      );
    });
    courses.dictionary = newCourseMap;
  });
});

/**
 *
 */
watchEffect(() => {
  if (!courses.dictionary.size) return;
  let newCourses = defaultCourses.value;
  userFilter.text &&
    getCourses(yacs.currentSemester, userFilter.text).then((data) => {
      newCourses = data.map((course) => course.full_title || course.title);
    });
  courses.courseList = newCourses.map((title) => courses.dictionary.get(title));
});

export { courses };
