<template functional>
  <b-badge v-if="props.seatsOpen <= 0" variant="danger">
    {{ props.seatsOpen }} / {{ props.seatsTotal }} Full
  </b-badge>
  <b-badge
    v-else-if="props.seatsOpen <= props.seatsTotal * 0.2"
    variant="warning"
  >
    {{ props.seatsOpen }} / {{ props.seatsTotal }} Open
  </b-badge>
  <b-badge v-else variant="success">
    {{ props.seatsOpen }} / {{ props.seatsTotal }} Open
  </b-badge>
</template>

<style></style>
