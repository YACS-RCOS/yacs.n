import { client } from "@/plugins/axios";

export const uploadCsv = (formData) =>
  client.post("/bulkCourseUpload", formData);

export const mapDateRangeToSemesterPart = (formData) =>
  client.post("/mapDateRangeToSemesterPart", formData);

export const updateSemester = (semester) =>
  client.post("/defaultsemesterset", { default: semester });

export const getAllSemesterInfo = () =>
  client.get("/semesterInfo").then((res) => res.data);

export const getDefaultSemester = () =>
  client.get("/defaultsemester").then((res) => res.data);
