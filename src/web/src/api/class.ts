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

export const getCourses = useMemoize(
  async (semester: string, search?: string): Promise<Course[]> => {
    const resp = await app.get<CourseResponse[]>("/class", { params: { semester, search } });

    const data = resp.data;

    return data.map((raw) => {
      return {
        ...raw,
        date_start: new Date(new Date(raw.date_start).toUTCString()),
        date_end: new Date(new Date(raw.date_end).toUTCString()),
        sections: raw.sections.filter((s) => s !== null)
      };
    });
  }
);
