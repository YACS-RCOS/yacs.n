<template>
  <b-badge
    :variant="$options.getSeatStatusVariant(props.seatsOpen, props.seatsTotal)"
  >
    <slot
      :seatsOpen="props.seatsOpen"
      :seatsFilled="props.seatsFilled"
      :seatsTotal="props.seatsTotal"
    >
      {{ props.seatsOpen }} / {{ props.seatsTotal }}
      {{ $options.getSeatStatusText(props.seatsOpen) }}
    </slot>
  </b-badge>
</template>

<script>
export default {
  props: {
    seatsOpen: Number,
    seatsFilled: Number,
    seatsTotal: Number,
  },
  getSeatStatusText(seatsOpen) {
    return seatsOpen <= 0 ? "Full" : "Open";
  },
  getSeatStatusVariant(seatsOpen, seatsTotal) {
    if (seatsOpen <= 0) {
      return "danger";
    } else if (seatsOpen <= seatsTotal * 0.2) {
      return "warning";
    } else {
      return "success";
    }
  },
};
</script>

<style></style>
