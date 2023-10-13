import axios from "axios";
import { api } from "./baseService";

export const uploadCsv = (formData) => api.post("/bulkCourseUpload", formData);

export const mapDateRangeToSemesterPart = (formData) =>
  api.post("/mapDateRangeToSemesterPart", formData);

export const updateSemester = (semester) =>
  api.post("/defaultsemesterset", { default: semester });

export const getAllSemesterInfo = () =>
  api.get("/semesterInfo").then((res) => res.data);

export const getDefaultSemester = () =>
  api.get("/defaultsemester").then((res) => res.data);

export const remove_professor = (email) =>
  api.delete("/professor/remove/" + email).then((res) => res.data);

export const addProfessors = (msg) =>
  api.post("/professor/add/" + msg).then((res) => res.data);

export const addProfessorsTest = () =>
  api.post("/professor/add/test").then((res) => res.data);
