<template>
  <div id="spinner">
    <b-spinner></b-spinner>
    <strong class="m-2">Loading Course...</strong>
  </div>
</template>

<script>
export default {
  name: 'CenterSpinner'
}
</script>

<style scope>
#spinner {
  text-align: center;
  padding-top: 30vh;
  font-size: 1.4em;
  height: 80vh;
}
</style>