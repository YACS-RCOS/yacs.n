<template>
  <b-badge
    v-if="$options.getNumOpenSections(props.course) > 0"
    variant="success"
  >
    {{ $options.getNumOpenSections(props.course) }}/{{
      props.course.sections.length
    }}
    Sections Open
  </b-badge>
  <b-badge v-else variant="danger">All Sections Full</b-badge>
</template>
<script>
export default {
  props: {
    course: Object,
  },
  getNumOpenSections(course) {
    return course.sections.filter((section) => section.seats_open > 0).length;
  },
};
</script>
