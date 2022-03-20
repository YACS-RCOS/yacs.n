import client from "./index"
import { localToUTCDate, readableDate } from "../../utils/common.js"

export const getSemesters = () =>
  client.get("/semester").then((res) => res.data);

export const getDefaultSemester = () =>
    client.get("/defaultsemester").then((res) => res.data);

export const getCourses = (semester, search = null) =>
    client.get("/class", { params: { semester, search } })

export const getDepartments = () =>
    client.get("/department")

export const uploadCsv = (formData) =>
    client.post("/bulkCourseUpload", formData);

export const getAllSemesterInfo = () =>
    client.get("/semesterInfo").then((res) => res.data);

export const mapDateRangeToSemesterPart = (formData) =>
    client.post("/mapDateRangeToSemesterPart", formData);

export const updateSemester = (semester) => 
    client.post("defaultsemesterset", { default: semester });

/**
 * Returns a list of all subsemesters
 * @returns {Promise<Subsemester[]>}
 */
export const getSubsemesters = (semester) =>
    client.get("/subsemester", {
        params: {
            semester: semester,
        },
    })
    .then(({ data }) => {
        return data.map((subsemester) => {
            subsemester.date_start = localToUTCDate(
                new Date(subsemester.date_start)
            );
            subsemester.date_end = localToUTCDate(new Date(subsemester.date_end));
            subsemester.date_start_display = readableDate(subsemester.date_start);
            subsemester.date_end_display = readableDate(subsemester.date_end);
            // Used to determine what semester the subsemester is part of
            subsemester.semester_name = subsemester.parent_semester_name;
            subsemester.display_string = subsemester.semester_part_name
                ? subsemester.semester_part_name
                : `${subsemester.date_start_display} - ${subsemester.date_end_display}`;

            return subsemester;
        });
    });