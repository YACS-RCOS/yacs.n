# -*- coding: utf-8 -*-
import getAllCourseToJSON
import LoadJSONWithRCS
import getAllFaculty
import requests


def main():
    session = requests.Session()
    getAllCourseToJSON.CreateCoursesJSON(session)
    print("Courses.json created")
    AllFaculty = LoadJSONWithRCS.FillJSONWithRCSIDs(session)
    print("Courses.json filled with RCSIDs")
    FilledAllFaculty = getAllFaculty.FacultyToJSON(AllFaculty, session)
    print("Faculty.json created")
    getAllFaculty.FacultyToList(FilledAllFaculty)
    print("Faculty.txt created")



if __name__ == "__main__":
    # TODO: Add more options and command line arguments support
    main()
    print("Done")
