export type Title = string

export type CRN = string

export type Semester = Map<Title, Course>

export interface Course {
  sections: Map<CRN, Section> | any
}

export interface Section {
  sessions: number[] | any
}
