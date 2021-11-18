import client from "./index";
import { Course } from "../../store/types";

const getSemester = (): Promise<object> => client.get("/semester");

const getDefaultSemester = () => client.get("/defaultsemester");

const getCourses = (semester: string): Promise<Course[]> =>
  client.get("/class", { params: { semester } });

export { getSemester, getDefaultSemester, getCourses };
