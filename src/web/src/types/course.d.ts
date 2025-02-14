export enum DayOfWeek {
  Sunday = 7,
  Monday = 0,
  Tuesday,
  Wednesday,
  Thursday,
  Friday,
  Saturday
}

export interface CourseSession {
  crn: string;
  section: number;
  semester: string;
  time_start: string;
  time_end: string;
  day_of_week: DayOfWeek;
  location: string;
  instructor: string;
  session_type: string;
}

export interface CourseSection {
  crn: string;
  seats_open: number;
  seats_filled: number;
  seats_total: number;
  semester: string;
  min_credits: number;
  max_credits: number;
  department: string;
  level: number;
  sessions: CourseSession[];
}

export interface Course {
  department: string;
  level: number;
  name: string;
  title: string;
  full_title: string;
  min_credits: number;
  max_credits: number;
  description: string;
  frequency: string;
  prerequisites: string[];
  corequisites: string[];
  date_start: Date;
  date_end: Date;
  sections: CourseSection[];
  semester: string;
  school: string;
}
