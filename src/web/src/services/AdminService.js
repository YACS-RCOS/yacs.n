import axios from "axios";

const client = axios.create({
  baseURL: "/api",
});

export const uploadCsv = (formData) =>
  client.post("/bulkCourseUpload", formData);

export const addPathways = (formData) =>
  client.post("/bulkPathwayUpload", formData);

export const generateCoursesMaster = (formData) =>
  client.post("/generate_Courses_Master", formData);

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


