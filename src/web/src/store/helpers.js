import store from './index';

import { NEXT_SCHEDULE_INDEX } from './mutations';

/**
 * Generates next available schedule ID
 * @returns {number}
 */
export const generateScheduleId = () => {
  store.commit(NEXT_SCHEDULE_INDEX);
  return store.state.scheduleIdIndex;
};
