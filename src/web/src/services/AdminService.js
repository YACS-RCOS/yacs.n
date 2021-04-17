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

export const uploadCreditCap = (creditCap, message, creditCap2, message2) =>
  client.post("/creditCap", { cc: creditCap, wm: message , 
  	cc2: creditCap2, wm2: message2});
