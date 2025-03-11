import type { Course, CourseSection, CourseSession } from "@/types/course";
import { useMemoize } from "@vueuse/core";
import { app } from "./common";

export type CourseResponse = Omit<Course, "coursesection" | "date_start" | "date_end"> & {
  coursesection: CourseSectionResponse[];
  date_start: string;
  date_end: string;
};

export type CourseSectionResponse = Omit<CourseSection, "sessions"> & {
  sessions: CourseSessionResponse;
};

export type CourseSessionResponse = CourseSession;

export type DepartmentResponse = { department: string }[];

export const getCourses = useMemoize(async (semester: string, search?: string) => {
  const resp = await app.get<CourseResponse[]>("/class", { params: { semester, search } });

  const data = resp.data;

  return data.map((raw) => {
    const t: Course = {
      ...raw,
      date_start: new Date(raw.date_start),
      date_end: new Date(raw.date_end),
      sections: raw.sections.filter((s) => s !== null),
      frequency: (raw.frequency ?? "").replace("When Offered:", "").trim()
    };
    return t;
  });
});

export const getDepartments = useMemoize(async () => {
  const resp = await app.get<DepartmentResponse>("/department");
  return resp.data;
});
