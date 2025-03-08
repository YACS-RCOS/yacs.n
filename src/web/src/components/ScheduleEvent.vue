<template functional>
  <div
    class="schedule-event"
    data-cy="schedule-event"
    tabindex="-1"
    :style="data.style"
    :id="props.crn + props.day + props.startTime"
  >
    <a :href="$options.getExploreCourseLink(props.name)" class="course-link">
      <div class="event-text">
        <span data-cy="title">{{ props.title }}</span>
        <br />
        <span data-cy="name">{{ props.name }}</span>
        &nbsp;–&nbsp;
        <span data-cy="section">{{ props.section }}</span>
        (
        <span data-cy="crn">{{ props.crn }}</span>
        )
        <br />
        <span data-cy="location">{{ props.location }}</span>
        <br />
        <span data-cy="instructor">{{ props.instructor }}</span>
      </div>
      <b-popover
        :title="props.name + ' – ' + props.section"
        :target="props.crn + props.day + props.startTime"
        triggers="hover"
        placement="top"
      >
        <h6 data-cy="title">
          <a v-bind:href="$options.getExploreCourseLink(props.name)">
            {{ props.title }}
          </a>
        </h6>
        <b>Session Type</b>
        <br />
        <span data-cy="sessionType">{{ props.sessionType }}</span>
        <br />
        <b>Instructor</b>
        <br />
        <span data-cy="instructor">{{ props.instructor }}</span>
        <br />
        <b>Location</b>
        <br />
        <span data-cy="location">{{ props.location }}</span>
        <br />
        <b>Session Time</b>
        <br />
        <span data-cy="time">{{ props.startTime }}–{{ props.endTime }}</span>
        <br />
        <b>CRN</b>
        <br />
        <span data-cy="crn">{{ props.crn }}</span>
        <br />
      </b-popover>
    </a>
  </div>
</template>
<script>
export default {
  getExploreCourseLink(courseName) {
    var subject = courseName.split(" ")[0];
    var courseNumber = courseName.split(" ")[1];
    return `/explore/${subject}/${subject}-${courseNumber}`;
  },
};
</script>
<style lang="scss">
.schedule-event {
  display: block;
  box-sizing: border-box;
  position: absolute;
  overflow: hidden;
  height: 100%;
  cursor: pointer;
  pointer-events: auto;

  .event-text {
    padding: 4px;
    font-weight: bold;
    font-size: 65%;
    box-sizing: border-box;
    height: 100%;
    overflow: hidden;

    span[data-cy="title"] {
      color: #000;
      font-size: 105%;
    }
  }

  .course-link {
    text-decoration: none;
    color: inherit;

    &:hover {
      text-decoration: none;
      color: inherit;
    }
  }
}
</style>
