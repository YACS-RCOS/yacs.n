<template>
    <div class="schedule-event">
        <div class="event-text">
            <!-- {{ period.section.listing.subjectShortname }} {{ period.section.listing.courseShortname }} - {{ period.section.shortname }}<br> -->
            {{ crn }} -
            <!-- {{ semester }} <br> -->
            {{ section }}<br>
            <!-- {{ period.section.instructors.join(', ') }}<br> -->
            <!-- {{ period.location }} -->
        </div>
    </div>
</template>

<script>
export default {
    name: 'ScheduleEvent',
    props: {
        crn: String,
        semester: String,
        section: String
    }
}
</script>

<style scoped lang="scss">
.schedule-event {
  //margin-top: 1px;
  border-left: 4px solid;
//   border-opacity: 1;
  overflow: hidden;
  height: 100%;
}

.event-text {
  padding: 4px;
  font-weight: bold;
  font-size: small;
  box-sizing: border-box;
}
</style>