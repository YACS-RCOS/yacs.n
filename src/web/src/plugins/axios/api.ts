import client from "./index";
import { Course } from "../../store/types";

const getSemester = (): Promise<
  {
    semester: string;
  }[]
> => client.get("/semester");

const getDefaultSemester = () => client.get("/defaultsemester");

const getCourses = (semester: string, search?: string): Promise<Course[]> =>
  client.get("/class", { params: { semester, search } });

export { getSemester, getDefaultSemester, getCourses };
