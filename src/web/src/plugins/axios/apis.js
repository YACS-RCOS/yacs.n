import client from "./index"

export const getSemesters = () =>
    client.get("/semester")

export const getDefaultSemester = () =>
    client.get("/defaultsemester")

export const getCourses = (semester, search = null) =>
    client.get("/class", { params: { semester, search } })

export const getDepartments = () =>
    client.get("/department")

export const uploadCsv = (formData) =>
    client.post("/bulkCourseUpload", formData)

export const getSubsemesters = (semester) =>
    client.get("/subsemester", { params: {semester: semester} })