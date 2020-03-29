import { getCourses } from '@/services/YacsService';

import { INIT_COURSES } from './mutations';

export const LOAD_CLASSES = 'LOAD_COURSES_SECTIONS_SESSIONS';

export default {
  async [LOAD_CLASSES]({ commit }) {
    const courses = await getCourses();
    console.log(`received ${courses.length} courses`);

    const normalizedCourses = {},
      normalizedSections = {},
      normalizedSessions = {};

    courses.forEach(course => {
      if (normalizedCourses[course.id]) {
        console.error(
          `Duplicate course id \n${JSON.stringify(normalizedSessions[course.id])}\n${JSON.stringify(
            course
          )}`
        );
      } else {
        course.sections.forEach(section => {
          if (normalizedSections[section.id]) {
            console.error(
              `Duplicate section id \n${JSON.stringify(
                normalizedSessions[section.id]
              )}\n${JSON.stringify(section)}`
            );
          } else {
            section.sessions.forEach(session => {
              if (normalizedSessions[session.id]) {
                console.error(
                  `Duplicate session id \n${JSON.stringify(
                    normalizedSessions[session.id]
                  )}\n${JSON.stringify(session)}`
                );
              } else {
                normalizedSessions[session.id] = session;
              }
            });
            section.sessionIds = section.sessions.map(s => s.id);
            // eslint-disable-next-line no-unused-vars
            const { sessions, ...normalizedSection } = section;
            normalizedSections[section.id] = normalizedSection;
          }
        });
        course.sectionIds = course.sections.map(s => s.id);
        // eslint-disable-next-line no-unused-vars
        const { sections, ...normalizedCourse } = course;
        normalizedCourses[course.id] = normalizedCourse;
      }
    });

    commit(INIT_COURSES, {
      courses: normalizedCourses,
      sections: normalizedSections,
      sessions: normalizedSessions
    });
  }
};
