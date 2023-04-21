<template>
    <b-container fluid class="py-3 h-100 main-body">
      <b-row class="h-100">
        <b-col md="4" class="d-flex flex-column">
          <b-card no-body class="h-100">
            <b-tabs card class="h-100 d-flex flex-column flex-grow-1">
              <b-tab
                title="Select Term"
                active
                class="flex-grow-1 w-100"
                data-cy="course-search-tab"
              >
              <!-- <section class="d-flex flex-column w-30">
                <section class="d-flex flex-row justify-content-center">
                  <p class="me-3 text-center w-30">Dept</p>
                  <p class="me-3 text-center w-30">Number</p>
                  <p class="me-3 text-center w-30">Section</p>
                </section>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
                <section class="d-flex flex-row justify-content-center">
                  <input type="text" class="w-30 me-3">
                  <input type="text" name="number" class="w-30 me-3">
                  <input type="text" name="section" class="w-30 me-3">
                </section>
                <hr>
              </section> -->
              <section class="d-flex flex-column w-30">
                <section class="d-flex flex-row justify-content-center">
                  <div class="d-flex flex-column justify-content-center align-items-center w-30">
                    <p class="text-center">Dept</p>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>
                    <b-form-group for="department">
                      <b-form-select
                        v-model="selectedDepartment"
                        :options="departmentOptions"
                        class="h-120"
                      ></b-form-select>
                    </b-form-group>    
                  </div>
                  <div class="d-flex flex-column justify-content-center align-items-center w-30">
                    <p class="text-center">Number</p>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                  </div>
                  <div class="d-flex flex-column justify-content-center align-items-center w-30">
                    <p class="text-center">Section</p>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                    <hr>
                    <input type="text" class="w-100 me-3">
                  </div>
                </section>
                <hr>
              </section>
              
              </b-tab>
              <b-tab class="flex-grow-1" data-cy="selected-courses-tab">
                Form
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <div class="col-md-8">
            Final Schdule Generator

            <template>
              <table class="final-table">
                <tr>
                  <th>Monday</th>
                  <th>Tuesday</th>
                  <th>Wednesday</th>
                  <th>Thursday</th>
                  <th>Friday</th>
                </tr>
                <tr>
                  <td>{{ Final_exam[0] }}</td>
                  <td>{{ Final_exam[1] }}</td>
                  <td>{{ Final_exam[2] }}</td>
                  <td>{{ Final_exam[3] }}</td>
                  <td>{{ Final_exam[4] }}</td>
                </tr>
              </table>
            </template>
   
   

            <!-- <v-calendar
              :attributes="attributes"
              :events="events"
              :min-date="minDate"
              :max-date="maxDate"
              :first-day-of-week="1"
            /> -->
          <!-- <b-form-select
            v-if="
              !loading &&
              scheduler.scheduleSubsemesters &&
              scheduler.scheduleSubsemesters.length > 1
            "
            v-model="selectedScheduleSubsemester"
            :options="scheduler.scheduleSubsemesters"
            text-field="display_string"
            value-field="display_string"
          ></b-form-select>
          <div id="allScheduleData">
            <div>
              <b-row>
                <b-col class="m-2">
                  <b-button
                    @click="
                      changeSchedule(-1);
                      updateIndexCookie();
                    "
                    size="sm"
                  >
                    Prev
                  </b-button>
                </b-col>
                <b-col cols="8" class="m-2 text-center">
                  <span v-if="scheduleDisplayMessage === 2">
                    Add some sections to generate schedules!
                  </span>
                  <span v-else-if="scheduleDisplayMessage === 3">
                    Can't display because of course conflict!
                  </span>
                  <span v-else>
                    Displaying schedule {{ this.index + 1 }} out of
                    {{ this.possibilities.length }}
                  </span>
                </b-col>
                <b-col class="m-2 text-right">
                  <b-button
                    @click="
                      changeSchedule(1);
                      updateIndexCookie();
                    "
                    size="sm"
                  >
                    Next
                  </b-button>
                </b-col>
              </b-row>
              <Schedule v-if="loading" />
              <Schedule v-else :possibility="possibilities[index]"></Schedule>
  
              <b-row>
                <b-col class="m-2">
                  <h5>CRNs: {{ selectedCrns }}</h5>
                  <h5>Credits: {{ totalCredits }}</h5>
                </b-col>
  
                <b-col md="3" justify="end">
                  <b-row>
                    <b-form-checkbox
                      class="mt-2"
                      size="sm"
                      :checked="$store.state.colorBlindAssist"
                      @change="toggleColors()"
                      switch
                    >
                      Color Blind Assistance
                    </b-form-checkbox>
                  </b-row>
                  <b-row>
                    <b-dropdown text="Export Data" class="mt-2">
                      <b-dropdown-item @click="exportScheduleToIcs">
                        <font-awesome-icon :icon="exportIcon" />
                        Export To ICS
                      </b-dropdown-item>
                      <b-dropdown-item @click="exportScheduleToImage">
                        <font-awesome-icon :icon="exportIcon" />
                        Export To Image
                      </b-dropdown-item>
                    </b-dropdown>
                  </b-row>
                </b-col>
              </b-row>
            </div>
          </div> -->
        </div>
      </b-row>
    </b-container>
  </template>

<script>
// import VueCalendar from 'vue-calendar';
// // const Vue = require('vue');
// // Vue.use(VueCalendar);
// const form = document.querySelector('form');
// const deptData = [];
// const numberData = [];
// const sectionData = [];

// form.addEventListener('submit', (event) => {
//   event.preventDefault();

//   const deptInputs = document.querySelectorAll('.w-30:first-child input');
//   const numberInputs = document.querySelectorAll('.w-30:nth-child(2) input');
//   const sectionInputs = document.querySelectorAll('.w-30:last-child input');

//   for (let i = 0; i < deptInputs.length; i++) {
//     const dept = deptInputs[i].value;
//     const number = numberInputs[i].value;
//     const section = sectionInputs[i].value;

//     deptData.push(dept);
//     numberData.push(number);
//     sectionData.push(section);
//   }

//   console.log(deptData);
//   console.log(numberData);
//   console.log(sectionData);

  // Do something else with the data, such as sending it to a server
// });
import { mapState } from "vuex";
import { getDepartments } from "@/services/YacsService";
export default {
  data() {
    return {
      selectedDepartment: null,
      attributes: [
        {
          key: 'start',
          highlight: true,
          backgroundColor: '#f9d6c1',
        },
      ],
      events: [
        {
          start: new Date(2023, 3, 25),
          end: new Date(2023, 3, 28),
          title: 'Event 1',
        },
        {
          start: new Date(2023, 3, 28),
          title: 'Event 2',
        },
      ],
      minDate: new Date(2023, 3, 1),
      maxDate: new Date(2023, 4, 31),
      Final_exam:  ["None", "None", "None", "None", "None"],
    };
  },
  
  created() {
    getDepartments().then((departments) => {
      this.departmentOptions.push(...departments.map((d) => d.department));
    });
  },
  computed: {
    ...mapState(["selectedSemester", "subsemesters", "departments"]),
    fullList() {
      return this.$store.getters.courses;
    },
    departmentOptions() {
      return [{ text: "All", value: null }].concat(
        ...this.departments.map(({ department }) => department)
      );
    },
  }
};
</script>

<style scoped>
.final-table {
  border-collapse: collapse;
  border: 2px solid black;
  width: 100%;
}

.final-table th,
.final-table td {
  border: 1px solid black;
  padding: 8px;
  text-align: center;
}

.final-table th {
  font-weight: bold;
  background-color: #ccc;
}




</style>
