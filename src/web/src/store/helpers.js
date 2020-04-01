import store from './index';

import { NEXT_SCHEDULE_INDEX } from './mutations';

export const generateScheduleId = () => {
  store.commit(NEXT_SCHEDULE_INDEX);
  return store.state.scheduleIdIndex;
};
