<template>
    <b-container>
       <section id="import-json">
        <h2>Import Data</h2>
        <div class="well well-sm">
          Input professor data as JSON
        </div>
        <form @submit.prevent="onSubmit" class="form-group">
          <div class="input-group">
            <label>
              Upload JSON file
              <input type="file" name="file" class="form-control-file" />
            </label>
            <br />
          </div>
          <div class="input-group">
            <label>
              <input type="checkbox" name="isPubliclyVisible" checked />
              Make Public
            </label>
          </div>
          <input
            type="Submit"
            label="submit"
            class="btn btn-success btn-sm"
            value="Submit"
          />
        </form>
      </section>
      <b-spinner v-show="loading" />
    </b-container>
  </template>
  
<script>

export default {
  name: "UploadCsv",
  components: {},
  props: {},
  data() {
    return {
      loading: false,
      isPublic: false,
    };
  },
  methods: {
    // onSubmit(event) 
    // {}
  }
}

</script>

<style lang="scss" scoped></style>