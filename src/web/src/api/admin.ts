import { app } from "./common";

export async function upload_course_csv(data: File) {
  const formdata = new FormData();
  formdata.append("file", data);
  formdata.append("isPubliclyVisible", "true");
  await app.post("/bulkCourseUpload", formdata);
}
