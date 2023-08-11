import axios from "axios";

const client = axios.create({
  baseURL: "/api",
});

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

export const remove_professor = (email) =>
  client.delete("/professor/remove/" + email).then((res) => res.data);

export const addProfessors = (msg) =>
  client.post("/professor/add/" + msg).then((res) => res.data);

export const addProfessorsTest = () =>
  client.post("/professor/add/test").then((res) => res.data);

export const removePathway = (pathway) =>
  client.delete("/pathway/remove/" + pathway).then((res) => res.data);

export const removeCourse = (course) =>
  client.delete("/pathway/remove/" + course).then((res) => res.data);

export const addPathway = (pathway) =>
  client.post("/pathway/add/" + pathway).then((res) => res.data);

export const addCourse = (course) =>
  client.post("/pathway/add/" + course).then((res) => res.data);

