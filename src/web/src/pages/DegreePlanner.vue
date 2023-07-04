<template>
    <b-container fluid>
        <div class="heading">
            <h1>Degree Planner</h1>
        </div>
        <div class="main-loading" v-if="main_loading">
          YACS<h1>&#32; &#32;Degree Planner</h1>
        </div>

        <div>
          <input class="text-input" v-model="textInput" type="text" placeholder="enter command for degree planner" @keyup.enter="dp_command">
        </div>

        <div>
          <h4 class="schedule-selection">
            <font color="#e6bc8a">Schedule:</font> {{ schedule_name }} <br>
            <font color="#e6bc8a">Degree:</font> {{ degree }}
          </h4>
        </div>

        <div class="columns">

          <div class="column-left">
            <div class="courses-grid">
              <div class="semester-block" v-for="(semester, index) in courses" :key="index">
                <h3>Semester {{ index + 1 }}</h3>

                <div>
                  <input class="course-input" v-model="course_inputs[index]" type="text" placeholder="add course" @keyup.enter="add_from_input(index)">
                </div>

                <div class="schedule-button-container" v-for="course in semester" :key="course">
                  <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                    &#10148; {{ course }}
                  </button>
                  <button class="course-remove-button" type="button" @click="remove(index, course)">
                    &#10008;
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <div class="column-center">
            <div class="requirements-dyngrid">
              <div class="text-block" v-for="(item, index) in requirements" :key="index">
                <h3>{{ item.name }}</h3>
                <div v-if="item.content">

                  <div class="alternatives" v-if="Object.keys(item.wildcard_resolutions).length > 0">
                    <div v-for="(alternative_choices, alternative_orig) in item.wildcard_resolutions" :key="alternative_orig">
                      <div v-for="alternative_choice in alternative_choices" :key="alternative_choice">
                        <button v-bind:class="{'alternative-buttons':!alternative_choice.includes('*'), 'alternative-buttons-wildcard':alternative_choice.includes('*')}" type="button" @click="fulfillment([alternative_orig, alternative_choice])">
                          {{ format_alternative(alternative_choice) }}
                        </button>
                      </div>
                    </div>
                  </div>

                  <div v-if="'specifications' in item">
                    <h6>specifications: {{ item.specifications }}</h6>
                  </div>

                  <div v-bind:class="{fulfillment:item.actual_count >= item.required_count, unfulfilled_fulfillment:item.actual_count < item.required_count}">
                      <div v-bind:class="{req_fulfilled:item.actual_count >= item.required_count, req_unfulfilled:item.actual_count < item.required_count}">
                          <h5>{{ item.actual_count }} / {{ item.required_count }}</h5>
                      </div>
                      <div class="fulfilled-list">
                          <div v-for="(course, index) in item.fulfillment_set" :key="index">
                            <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                              &#10148; {{ course }}
                            </button>
                          </div>
                      </div>
                  </div>
                  <br>

                  <div class="recommendations" v-if="recommendations[item.name].length > 0 && recommendations[item.name][0].fulfillment_set.length > 0">
                    <h4>Recommendations:</h4>
                    <div class="recommendation-list" v-for="recommendation in recommendations[item.name]" :key="recommendation">
                      <h6>specifications: {{ recommendation.specifications }}</h6>
                      <div v-for="(course, index) in recommendation.fulfillment_set" :key="index">
                        <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                          &#10148; {{ course }}
                        </button>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

          <div class="column">
            column 3
          </div>

        </div>
    </b-container>
</template>
  
<script>

  export default {
    data() {
      return {
        loading: true,
        main_loading: true,
        userid: 'testuser',
        degree: 'computer science',
        schedule_name: "new schedule",
        requirements: [],
        recommendations: {},
        courses: [],

        SEM_MAX: 12,
        course_inputs: [],
      };
    },
    methods: {

      // HELPER FUNCTIONS

      navigate_to_course_page(course) {
        let page = course.substring(0, 4).toUpperCase() + "/" + course.substring(0, 4).toUpperCase() + "-" + course.substring(5, 9);
        this.$router.push("/explore/" + page);
      },

      format_alternative(str) {
        if (str.includes('*')) {
          str = str.split('*')[0] + " automatically select"
        }
        str = str.replace('.', ': ');
        return str
      },

      async update_variables(variable_updates) {
        // helper function that updates variables of this page from API reply
        for(let [key, value] of Object.entries(variable_updates)) {
          if (this[key] !== undefined) {
            this[key] = value;
          }
        }
      },


      // API CALLING

      async dp_command() {
          let command = this.textInput;
          let userid = this.userid;
          const updates = await fetch('/api/dp/users/command', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({userid, command}),
          });
          let variable_updates = await updates.json();

          this.update_variables(variable_updates).then(this.fetch_data());
          this.textInput = "";
      },

      async fetch_data() {
        this.loading = true;
        // fetch fulfillment and recommendations
        this.print();
        this.fulfillment([]);
        this.recommend();
      },

      async newuser() {
        let userid = this.userid;
        let degree = this.degree;
        let schedule_name = this.schedule_name;
        let courses = {};

        await fetch('/api/dp/newuser', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({userid, degree, schedule_name, courses}),
        });
      },

      async fulfillment(attributes_replacement) {
        let userid = this.userid;

        const response1 = await fetch('/api/dp/fulfillment', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({userid, attributes_replacement}),
        });

        this.requirements = await response1.json();
      },

      async recommend() {
        let userid = this.userid;

        const response2 = await fetch('/api/dp/recommend', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(userid),
        });
        this.recommendations = await response2.json().then(this.loading = false).then(this.main_loading = false);
      },

      async add_from_input(semester) {
        this.add(semester, this.course_inputs[semester]);
        this.course_inputs[semester] = "";
      },

      async add(semester, course) {
        let userid = this.userid;
        let command = "add, " + semester + ", " + course;

        const updates = await fetch('/api/dp/users/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, command}),
        });
        let variable_updates = await updates.json();
        this.update_variables(variable_updates).then(this.fetch_data());
      },

      async remove(semester, course) {
        let userid = this.userid;
        let command = "remove, " + semester + ", " + course;

        const updates = await fetch('/api/dp/users/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, command}),
        });
        let variable_updates = await updates.json();
        this.update_variables(variable_updates).then(this.fetch_data());
      },

      async print() {
        let userid = this.userid;

        const response = await fetch('/api/dp/print', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(userid),
        });
        this.courses = await response.json();
      }

    },

    async created() {
      this.main_loading = true;
      await this.newuser();
      await this.fetch_data();

      this.course_inputs = new Array(this.SEM_MAX).fill('')
    },
  };
</script>
  
<style scoped>
  .heading {
    font-weight:400;
    color:#9fc6c6;
  }
  .schedule-selection {
    text-align: center;
    color:#e3e8e4;
  }
  .main-loading {
    text-align:center;
    font-size:8em;
    font-weight:600;
    color:#e19e8c;
    position: fixed;
    display: flex;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    background-color: rgba(8, 26, 32, 0.95);
    backdrop-filter: blur(4px);
    justify-content: center;
    align-items: center;
    z-index: 9999;
  }
  .main-loading h1 {
    font-size:0.9em;
    margin: 30px;
    color:#cadbdb;
  }
  .loading {
    text-align:center;
    font-size:1em;
    position:fixed;
  }
  .columns {
    display: flex;
    height: 100vh;
    width: 100%;
  }
  .column {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #171d1a;
  }
  .column-left {
    flex: 2;
    overflow-y: auto;
    padding: 4px;
    border: 1px solid #171d1a;
    font-size: 0.8em;
    min-width: 500px;
  }
  .column-left::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-center {
    flex: 5;
    overflow-y: auto;
    padding: 8px;
    border: 1px solid #171d1a;
  }
  .column-center::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .requirements-dyngrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    justify-content: center;
    gap: 4px;
  }
  .requirements-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 4px;
  }
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap:4px;
  }
  .semester-block {
    border: 2px;
    border-radius:12px;
    padding: 4px;
    margin: 4px;
    font-size: 0.75em;
    background-color: #21242b;
  }
  .semester-block h3 {
    font-size: 1.5em;
    color: #a2bbe0;
  }
  .schedule-button-container {
    display: flex;
  }
  .text-input{
    border:2px solid #21242b;
    border-radius:4px;
    width:150px;
    padding:4px;
    background-color:#393b40;
    position:fixed;
  }
  .course-input{
    border:2px solid #21242b;
    border-radius:2px;
    width:75%;
    padding:2px;
    background-color:#393b40;
  }
  .text-input:focus{
    width:300px;
    border:4px;
    background-color:#3f4146;
  }
  .text-block {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
    width: 350px;
    min-height: 60px;
    align-items: center;
    font-size: 0.7em;
    background-color: #21242b;
  }
  .course-schedule-buttons {
    border: none;
    border-radius: 4px;
    width: 80%;
    padding: 0px;
    margin: 1px;
    color:#e3e8e4;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: left;
  }
  .course-buttons {
    border: none;
    border-radius: 4px;
    flex: 1;
    padding: 0px;
    width: 99%;
    margin: 1px;
    color:#e3e8e4;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: left;
  }
  .course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .course-remove-button {
    border: none;
    border-radius: 4px;
    flex: 0.1;
    padding: 0px;
    margin: 1px;
    color:#e3e8e4;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: center;
  }
  .course-remove-button:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .text-block h3 {
    color:cornflowerblue;
    font-size: 1.5em;
  }
  .text-block h4 {
    font-size: 1.4em;
  }
  .text-block h6 {
    color:rgb(129, 145, 161);
    font-size: 0.8em;
  }
  .fulfillment {
    padding: 6px;
    margin: 2px;
    border-radius: 6px;
    color: #e3e8e4;
    background-color: #434f41;
  }
  .unfulfilled_fulfillment {
    padding: 6px;
    margin: 2px;
    border-radius: 6px;
    color: #e3e8e4;
    background-color: #4f433e;
  }
  .alternative-buttons {
    border-radius: 6px;
    width: 99%;
    border: none;
    padding: 4px;
    margin: 2px;
    color:#e3e8e4;
    background-color: #3e4041;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons:hover {
    background-color:#21242b;
  }
  .alternative-buttons-wildcard {
    border-radius: 6px;
    width: 99%;
    border: none;
    padding: 4px;
    margin: 2px;
    color:#d8e8dc;
    background-color: #497348;
    font-weight:500;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons-wildcard:hover {
    background-color:#171d1a;
    color: #c7e4e1;
    border: none;
  }
  .recommendations {
    padding: 4px;
    margin: 2px;
    border-radius: 6px;
    background-color: #393b40;
  }
  .recommendations-list {
    color: #e3e8e4;
  }
  .req_fulfilled {
    color: greenyellow;
    background-color: #434f41;
  }
  .req_unfulfilled {
    color: orangered;
    background-color: #4f433e;
  }
  .heading {
    text-align: center;
  }
</style>
  