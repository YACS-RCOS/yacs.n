import { app } from "./common";

export type SemesterResponse = { semester: string }[];
export type SemesterInfoResponse = { public: boolean; semester: string }[];

/** Gets a list of available semesters
 */
export async function getSemesters() {
  const resp = await app.get<SemesterResponse>("/semester");
  return resp.data.map((v) => v.semester);
}

/** Gets semester info
 */
export async function getSemesterInfo() {
  const resp = await app.get<SemesterInfoResponse>("/semesterInfo");
  return resp.data;
}
