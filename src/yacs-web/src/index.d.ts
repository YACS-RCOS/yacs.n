// Just a itty bit of typescript for some
// good ole autocomplete

export interface CourseSession {
  crn: string;
  day_of_week: number;
  section: string;
  semester: string;
  time_end: string;
  time_start: string;
}

export interface CourseSection {
  crn: string;
  department: string;
  level: number;
  semester: string;
  sessions: CourseSession[];
  selected: boolean;
}

export interface Course {
  department: string;
  level: number;
  sections: CourseSection[];
  title: string;
  date_start: Date;
  date_end: Date;
  id: string;
  selected: boolean;
}

export interface Subsemester {
  date_start: Date;
  date_end: Date;
  date_start_display: string;
  date_end_display: string;
  display_string: string;
}

export interface Department {
  department: string;
}
