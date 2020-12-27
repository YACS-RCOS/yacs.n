import "@/typedef";

import Logic from "logic-solver";

import { hasSessionConflict } from "@/utils";
import Scheduler from "./Scheduler";
import Schedule from "./Schedule";

const SECTION_ID_SPLIT_CHAR = "-";

/**
 *
 * @param {Course} course
 * @param {CourseSection} section
 * @returns {string}
 */
const getSectionId = (course, section) =>
  `${course.name}${SECTION_ID_SPLIT_CHAR}${section.crn}`;

/**
 *
 * @param {string} sectionId
 * @returns {string[]}
 */
const parseSectionId = (sectionId) => {
  const index = sectionId.lastIndexOf(SECTION_ID_SPLIT_CHAR);

  return [sectionId.substring(0, index), sectionId.substring(index + 1)];
};

/**
 *
 * @param {() => Scheduler} scheduleFactory
 * @returns {(courses: Course[], sections: CourseSection[]) => Scheduler}
 */
const scheduleFactoryFactory = (scheduleFactory) => (courses, sections) => {
  const schedule = scheduleFactory();

  new Set(courses).forEach((course) => schedule.addCourse(course));

  sections.forEach((section, i) =>
    schedule.addCourseSection(courses[i], section)
  );

  return schedule;
};
/**
 * The CourseScheduler class has three invariants:
 * 1. Every schedule contains exactly one course section from each course
 * in `courses`
 * 2. No two schedules contain the same set of course sections
 * 3. None of the selected course section time blocks overlap
 *
 * Given a set of courses, the CourseScheduler builds a set
 * of possible schedules for all non-conflicting course sections.
 */
class CourseScheduler extends Scheduler {
  /** @type {Course[]} */
  courses;

  /** @type {string[][]} */
  conflicts;

  /** @type {Set<string>} */
  selectedCourseSections;

  /** @type {(courses: Course[], sections: CourseSection[]) => Scheduler} */
  scheduleFactory;

  constructor(scheduleFactory = () => new Schedule()) {
    super();
    this.courses = [];
    this.selectedCourseSections = new Set([]);
    this.conflicts = [];
    this.scheduleFactory = scheduleFactoryFactory(scheduleFactory);
  }

  /**
   *
   * @param {Course} newCourse
   */
  addCourse(newCourse) {
    console.log("adding course");
    // O(n^3) ;( could probably cache this or something
    for (const course of this.courses) {
      for (const section of course.sections) {
        for (const newSection of newCourse.sections) {
          if (hasSessionConflict(newSection, section)) {
            this.conflicts.push([
              getSectionId(newCourse, newSection),
              getSectionId(course, section),
            ]);
          }
        }
      }
    }

    this.courses.push(newCourse);

    this.computeSchedules();
  }

  computeSchedules() {
    /** @type {Logic.Solver} */
    const solver = new Logic.Solver();

    this.courses.forEach((course) => {
      solver.require(
        Logic.exactlyOne(
          course.sections.map((section) =>
            solver.toNameTerm(getSectionId(course, section))
          )
        )
      );
    });

    this.conflicts.forEach((conflictingSections) => {
      solver.require(
        Logic.not(Logic.and(...conflictingSections.map(solver.toNameTerm)))
      );
    });

    const solve =
      this.selectedCourseSections.size > 0
        ? () =>
            solver.solveAssuming(
              Logic.and(
                ...[...this.selectedCourseSections].map(solver.toNameTerm)
              )
            )
        : () => solver.solve();

    /** @type {string[][]} */
    const solutions = [];
    let currentSolution;
    const limit = 100;
    let i = 0;
    while ((currentSolution = solve()) && i < limit) {
      i++;
      solutions.push(currentSolution.getTrueVars());
      solver.forbid(currentSolution.getFormula());
    }

    // console.log(this.courses.map((course) => course.name));
    // console.log(this.selectedCourseSections);
    // console.log(solutions);

    this.schedules.splice(
      0,
      this.schedules.length,
      ...solutions.map((sectionIds) => {
        const courseSectionMappings = sectionIds
          .map(parseSectionId)
          .map(([courseName, sectionCrn]) => {
            const course = this.courses.find(
              (course) => course.name === courseName
            );
            const section = course.sections.find(
              (section) => section.crn === sectionCrn
            );

            return [course, section];
          });

        return this.scheduleFactory(
          courseSectionMappings.map((mapping) => mapping[0]),
          courseSectionMappings.map((mapping) => mapping[1])
        );
      })
    );
  }

  /**
   *
   * @param {Course} course
   * @param {CourseSection} section
   */
  addCourseSection(course, section) {
    console.log("adding course section");
    this.selectedCourseSections.add(getSectionId(course, section));

    this.computeSchedules();
  }

  /**
   *
   * @param {Course} course
   * @param {CourseSection} section
   */
  removeCourseSection(course, section) {
    console.log("removing course section");
    this.selectedCourseSections.delete(getSectionId(course, section));

    this.computeSchedules();
  }

  /**
   *
   * @param {Course} course
   */
  removeAllCourseSections(course) {
    console.log("removing course");
    this.courses.splice(
      this.courses.findIndex((selectedCourse) => selectedCourse === course)
    );

    const courseSections = new Set(
      course.sections.map((section) => getSectionId(course, section)).flat()
    );
    this.conflicts = this.conflicts.filter(
      (crns) => !crns.some((crn) => courseSections.has(crn))
    );

    this.computeSchedules();
  }
}

export default CourseScheduler;
