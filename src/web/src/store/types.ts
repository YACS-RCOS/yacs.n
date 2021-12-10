export type Title = string;

export type CRN = string;

export type Semester = Map<Title, Course>;

export interface Course {
  title: string;
  full_title: string;
  sections: Map<CRN, Section> | (Record<string, any> | null)[];
}

export interface Section {
  crn: string;
  sessions: number[] | any;
}
