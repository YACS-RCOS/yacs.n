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

export const removePathway = (course) =>
  client.delete("/pathway/remove/" + course).then((res) => res.data);

export const removeCourse = (course) =>
  client.delete("/pathway/remove/" + course).then((res) => res.data);

export const addPathway = (name) =>
  client.post("/pathway/add/" + name).then((res) => res.data);

export const addCourse = (name) =>
  client.post("/pathway/add/" + name).then((res) => res.data);

export const addPathwayTest = () =>
  client.post("/pathway/add/test").then((res) => res.data);

