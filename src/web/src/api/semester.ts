import { useMemoize } from "@vueuse/core";
import { app } from "./common";

export type SemesterResponse = { semester: string }[];
export type SemesterInfoResponse = { public: boolean; semester: string }[];

/** Gets a list of available semesters */
export const getSemesters = useMemoize(async () => {
  const resp = await app.get<SemesterResponse>("/semester");
  return resp.data.map((v) => v.semester);
});

/** Gets semester info */
export const getSemesterInfo = useMemoize(async () => {
  const resp = await app.get<SemesterInfoResponse>("/semesterInfo");
  return resp.data;
});
