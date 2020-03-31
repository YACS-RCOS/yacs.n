<template>
  <div id='header'>
    <b-navbar variant="light">
        <b-navbar-brand href="#">YACS</b-navbar-brand>
        <b-navbar-nav class="ml-auto">
            <div>
            <b-button v-b-modal.modal-1 size="sm" variant="light">Log In</b-button>

            <b-modal id="modal-1" ref="modal-1" hide-footer title="Log In">
                <div>
                    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
                    <b-form-group
                        id="input-group-1"
                        label="Email address:"
                        label-for="input-1"
                        description="We'll never share your email with anyone else."
                    >
                        <b-form-input
                        id="input-1"
                        v-model="form.email"
                        type="email"
                        required
                        placeholder="Enter email"
                        ></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
                        <b-form-input
                        id="input-2"
                        v-model="form.name"
                        required
                        placeholder="Enter name"
                        ></b-form-input>
                    </b-form-group>

                    <b-button type="submit" variant="primary">Submit</b-button>
                    <b-button type="reset" variant="danger">Reset</b-button>
                    </b-form>
                    <b-card class="mt-3" header="Form Data Result">
                    <pre class="m-0">{{ form }}</pre>
                    </b-card>
                </div>

                <b-button class="mt-2"  block @click="toggleModal">Toggle Me</b-button>
            </b-modal>
            </div>
        </b-navbar-nav>

      </b-navbar>
      <hr>
    </div>
</template>

<script>
// import { getSemesters } from '../services/YacsService';

export default {
    name: 'Header',
    data() {
      return {
        form: {
          email: '',
          name: '',
        },
        show: true
      }
    },
    methods: {
      toggleModal() {
        // We pass the ID of the button that we want to return focus to
        // when the modal has hidden
        this.$refs['modal-1'].hide()
      },
      onSubmit(evt) {
        evt.preventDefault()
        alert(JSON.stringify(this.form))
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.email = ''
        this.form.name = ''
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
}
</script>

<style>

.navbar {
  background: white !important;
  margin-bottom: none !important;
}

hr {
  margin: 0em;
  border-width: 1px;
}


</style>
