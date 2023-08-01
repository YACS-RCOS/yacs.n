<template>
    <b-container fluid>
        <div class="main-loading" v-if="main_loading">
          YACS<h1>&#32; &#32;Degree Planner</h1>
        </div>

        <div class="columns">

          <div class="column-left">
            <div class="courses-grid">
              <div v-for="(semester, index) in courses" :key="index" 
                  v-bind:class="{'semester-block':hoverOverSemester!=index, 'semester-block-highlighted':hoverOverSemester==index}" 
                  @dragenter="schedulerDragEnter($event, index)" 
                  @dragleave="schedulerDragLeave()" 
                  @dragover.prevent 
                  @drop="schedulerDrop($event, index)">
                <h3>Semester {{ index + 1 }}</h3>

                <div>
                  <input class="course-input" v-model="course_inputs[index]" type="text" placeholder="add course" @keyup.enter="add_from_input(index)">
                </div>

                <div class="schedule-button-container" v-for="(course, course_index) in semester" :key="course_index">
                  <button class="course-buttons" type="button" @click="navigate_to_course_page(course)" draggable="true" @dragstart="schedulerDrag($event, course, index)">
                    <font color="#ffc680">{{ course.substring(0, 10) }}</font> {{ course.substring(10) }}
                  </button>
                  <button class="course-remove-button" type="button" @click="remove(index, course)">
                    <font color="#b05f6e">&#10008;</font>
                  </button>
                </div>

              </div>
            </div>
          </div>
          
          <div class="column-center">

            <div class="requirements-orggrid">
              <div class="fulfillment-org-block" v-for="(group, group_index) in requirement_groups" :key="group_index">
                <div v-if="true">
                  <div class="group-heading">
                    <span class="group-title"> {{ group.name }} </span> 
                    <span v-if="group.minimum_requirements.credits > 0" 
                      v-bind:class="{'group-credit-stats-fulfilled':get_tallied_amount(group.name, 'credits') >= group.minimum_requirements.credits, 'group-credit-stats-unfulfilled':get_tallied_amount(group.name, 'credits') < group.minimum_requirements.credits}">
                      <font color="#707a7a"> credits:&nbsp;&nbsp; </font> {{ get_tallied_amount(group.name, 'credits') }} / {{ group.minimum_requirements.credits }} </span>
                  </div>
                  <div v-for="(requirement, index) in group.requirements" :key="index">
                    
                    <div v-if="Object.keys(requirements[requirement].wildcard_resolutions).length > 0">
                      <div v-for="(alternative_choices, alternative_orig) in requirements[requirement].wildcard_resolutions" :key="alternative_orig">
                        <div v-for="(alternative_choice, alternative_choice_index) in alternative_choices" :key="alternative_choice_index">
                          <button v-bind:class="{'alternative-buttons':!alternative_choice.includes('*'), 'alternative-buttons-wildcard':alternative_choice.includes('*')}" type="button" @click="get_fulfillment({[alternative_orig]:alternative_choice})">
                            {{ format_alternative(alternative_choice) }}
                          </button>
                        </div>
                      </div>
                    </div>

                    <div v-bind:class="{'minimal-fulfillment':requirements[requirement].actual_count >= requirements[requirement].required_count, 'minimal-unfulfilled-fulfillment':requirements[requirement].actual_count < requirements[requirement].required_count}">
                      <div v-bind:class="{'req-fulfilled':requirements[requirement].actual_count >= requirements[requirement].required_count, 'req-unfulfilled':requirements[requirement].actual_count < requirements[requirement].required_count}">
                        <div class="req-fulfillment-text">
                          <span class="req-fulfillment-name"> {{ format_fulfillment_name(requirements[requirement].name) }} </span> <span class="req-fulfillment-count"> {{ requirements[requirement].actual_count }} / {{ requirements[requirement].required_count }}</span>
                        </div>
                      </div>

                      <div v-for="(course, index) in requirements[requirement].fulfillment_set" :key="index">
                        <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                          &#10148; {{ course }}
                        </button>
                      </div>
                    </div>

                    <div class="req-recommendations" v-if="requirement in recommendations && recommendations[requirement].length > 0 && recommendations[requirement][0].fulfillment_set.length > 0">
                      <div class="minimal-recommendations" v-for="(recommendation, recommendation_index) in recommendations[requirement]" :key="recommendation_index">
                        <div v-if="recommendations[requirement].length > 1">
                          <h5>{{ recommendation.specifications }}</h5>
                        </div>
                        <div class="minimal-recommendations-courses" v-for="(course, index) in recommendation.fulfillment_set" :key="index">
                          <button class="minimal-course-buttons" type="button" @click="navigate_to_course_page(course)" draggable="true" @dragstart="schedulerDrag($event, course, -1)">
                            <font color = #a9a9a9> {{ course }} </font>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="column-right">
            <div>
              <input class="text-input" v-model="cmdInput" type="text" placeholder="enter command for degree planner" @keyup.enter="dp_command">
            </div>
            <div class="schedule-selection">
              <font color="#eb8d75">Schedule:</font> {{ schedule_name }} <br>
              <font color="#e6bc8a">Degree:</font> {{ degree }}
            </div>
            
            <div class="details-panel" v-for="(fulfillments, requirement) in display" :key="requirement">
              <p> <font color="#707a7a">Details</font></p>
              <h5>{{ requirement }}:</h5>
              <div class="details-wildcard-title" v-for="(fulfillment, fulfillment_index) in fulfillments" :key="fulfillment_index">
                {{ fulfillment[0] }}
                <div class="details-info" v-for="(course, index) in fulfillment[1]" :key="index">
                  <button class="course-buttons" type="button" @click="navigate_to_course_page(course)">
                    &#10148; <font color="#ffc680">{{ course.substring(0, 10) }}</font> {{ course.substring(10) }}
                  </button>
                </div>
              </div>
            </div>
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
        courses: [],
        cmdInput: '',

        requirement_groups: [],
        tally: {},
        requirements: {},
        recommendations: {},
        display: {},

        SEM_MAX: 12,
        course_inputs: [],

        recommend_pause_token: 1,

        dragElement: null,
        dragFromSemester: 0,
        hoverOverSemester: -1,
        hoverCounter: 0, // to fix the problem where hovering over child elements creates a dragenter + dragleave event
      };
    },
    methods: {

      // HELPER FUNCTIONS

      schedulerDrag(event, item, semester) {
        this.dragElement = item;
        this.dragFromSemester = semester;
        event.dataTransfer.effectAllowed = "move";
      },

      schedulerDrop(event, dragToSemester) {
        event.preventDefault();
        if (this.dragElement != null) {
          if (this.dragFromSemester != -1) {
            this.remove(this.dragFromSemester, this.dragElement, false, false);
            this.add(dragToSemester, this.dragElement, false, false);
          } else {
            this.add(dragToSemester, this.dragElement, true, true);
          }
        }
        this.hoverCounter--;
        this.hoverOverSemester = -1;
      },

      schedulerDragEnter(event, hoverOverSemester) {
        event.preventDefault();
        this.hoverOverSemester = hoverOverSemester;
        this.hoverCounter++;
      },

      schedulerDragLeave() {
        this.hoverCounter--;
        if (this.hoverCounter == 0) {
          this.hoverOverSemester = -1;
        }
      },

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

      format_fulfillment_name(str) {
        if (str.includes('-')) {
          str = str.substring(str.indexOf('-') + 1)
        }
        return str
      },

      get_tallied_amount(group_name, tally) {
        if (this.tally[group_name][tally] == null) {
          return 0
        }
        return this.tally[group_name][tally]
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
          let command = this.cmdInput;
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
          this.cmdInput = "";
      },

      async fetch_data(fulfill=true, recommend=true) {
        this.loading = true;
        // fetch fulfillment and recommendations
        this.print();
        if (fulfill) {
          this.get_fulfillment().then(this.main_loading = false);
        }
        if (recommend) {
          this.get_recommendation();
        }
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

      async get_fulfillment(attributes_replacement=null) {
        let userid = this.userid;

        if (attributes_replacement == null) {
          attributes_replacement = {};
        }

        const response1 = await fetch('/api/dp/fulfillment', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({userid, attributes_replacement}),
        });
        let fulfillment_tuple = await response1.json();
        this.requirements = fulfillment_tuple[0];
        this.requirement_groups = fulfillment_tuple[1];
        this.tally = fulfillment_tuple[2];
        this.display = fulfillment_tuple[3];
      },

      async get_recommendation() {
        let userid = this.userid;

        await fetch('/api/dp/recommend/' + userid, {
          method: 'POST'
        });

        const response2 = await fetch('/api/dp/recommend/' + userid);
        this.recommendations = await response2.json().then(this.loading = false)
      },

      async add_from_input(semester) {
        this.add(semester, this.course_inputs[semester]);
        this.course_inputs[semester] = "";
      },

      async add(semester, course, fulfill=true, recommend=true) {
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
        this.update_variables(variable_updates).then(this.fetch_data(fulfill, recommend));
      },

      async remove(semester, course, fulfill=true, recommend=true) {
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
        this.update_variables(variable_updates).then(this.fetch_data(fulfill, recommend));
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
    color:#d65252;
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
    background-color: rgba(8, 26, 32, 0.85);
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
    height: 90vh;
    width: 100%;
  }
  .column-left {
    flex: 6;
    overflow-y: auto;
    padding: 4px;
    border: 1px solid #171d1a;
    font-size: 0.8em;
    min-width: 400px;
    max-width: 600px;
  }
  .column-left::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-center {
    flex: 11;
    overflow-y: auto;
    padding: 8px;
    border: 1px solid #171d1a;
  }
  .column-center::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .column-right {
    flex: 4;
    overflow-y: auto;
    padding: 4px;
    border: 1px solid #171d1a;
    font-size: 0.8em;
    min-width: 300px;
    max-width: 400px;
  }
  .column-right::-webkit-scrollbar {
    display: none; /* Chrome, Safari and Opera */
  }
  .requirements-dyngrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
    justify-content: center;
    gap: 4px;
  }
  .requirements-orggrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    justify-content: center;
    gap: 4px;
  }
  .courses-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap:0px;
  }
  .semester-block {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
    font-size: 0.75em;
    background-color: rgba(8, 26, 32, 0.35);
    backdrop-filter: blur(4px);
  }
  .semester-block h3 {
    font-size: 1.5em;
    color: #98bdd4;
  }
  .semester-block-highlighted {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
    font-size: 0.75em;
    background-color: rgba(69, 94, 104, 0.35);
  }
  .semester-block-highlighted h3 {
    font-size: 1.5em;
    color: #98bdd4;
  }
  .schedule-button-container {
    display: flex;
  }
  .text-input{
    border:2px solid #21242b;
    border-radius:4px;
    width:100%;
    padding:4px;
    background-color:#393b40;
  }
  .course-input{
    border:2px solid #21242b;
    border-radius:2px;
    width:75%;
    padding:2px;
    background-color:#393b40;
  }
  .fulfillment-org-block {
    border: 2px solid #43494f;
    border-radius: 8px;
    padding: 8px;
    margin: 2px;
    width: 345px;
    min-height: 60px;
    align-items: center;
    font-size: 0.65em;
    background-color: rgba(8, 26, 32, 0.35);
    backdrop-filter: blur(4px);
  }
  .fulfillment-org-block h3 {
    font-size: 1.2em;
  }
  .fulfillment-org-block h5 {
    font-size: 1.1em;
    margin: 0px;
    color: #beb8b1;
  }
  .group-heading {
    display: flex;
  }
  .group-heading .group-title {
    color:#78b2d9; 
    font-size: 1.8em;
    flex: 0.97;
    padding-left: 2%;
  }
  .group-heading .group-credit-stats-fulfilled {
    font-size: 1.8em;
    font-weight: 700;
    color: #86bea9;
  }
  .group-heading .group-credit-stats-unfulfilled {
    font-size: 1.8em;
    font-weight: 700;
    color: #be8886;
  }
  .course-schedule-buttons {
    border: none;
    border-radius: 4px;
    width: 80%;
    padding: 0px;
    margin: 1px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.2s ease;
    text-align: left;
  }
  .course-buttons {
    border: none;
    border-radius: 4px;
    flex: 1;
    padding: 0px;
    width: 99%;
    margin: 1px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.2s ease;
    text-align: left;
  }
  .course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .req-fulfillment-text {
    display:flex;
    margin-left: 4px;
    margin-right: 4px;
    font-size: 1.3em;
    font-weight: 500;
  }
  .req-fulfillment-text .req-fulfillment-name {
    color: rgb(163, 185, 189);
    flex: 1;
  }
  .req-fulfillment-text .req-fulfillment-count {
    font-weight: 650;
    font-size: 1.2em;
  }
  .minimal-fulfillment {
    padding-left: 4px;
    padding-right: 4px;
    padding: 1px;
    margin: 0px;
    border-radius: 4px;
    background-color: #434f41;
  }
  .minimal-unfulfilled-fulfillment {
    padding-left: 4px;
    padding-right: 4px;
    padding: 1px;
    margin: 0px;
    border-radius: 4px;
    background-color: #4f433e;
  }
  .req-recommendations {
    margin-bottom: 10px;
  }
  .minimal-course-buttons {
    border: none;
    border-radius: 2px;
    flex: 1;
    padding: 0px;
    margin: 1px;
    margin-right: 5px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: left;
  }
  .minimal-course-buttons:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .minimal-recommendations {
    margin-left: 8px;
  }
  .minimal-recommendations-courses {
    margin-left: 14px;
  }
  .course-remove-button {
    border: none;
    border-radius: 4px;
    flex: 0.1;
    padding: 0px;
    margin: 1px;
    background-color: rgba(197, 211, 218, 0.01);
    transition: background-color 0.15s ease;
    text-align: center;
  }
  .course-remove-button:hover {
    background-color: rgba(13, 23, 26, 0.78);
  }
  .alternative-buttons {
    border-radius: 2px;
    width: 99%;
    border: none;
    padding: 2px;
    margin: 1px;
    color:#e3e8e4;
    background-color: #3e4041;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons:hover {
    background-color:#21242b;
  }
  .alternative-buttons-wildcard {
    border-radius: 2px;
    width: 99%;
    border: none;
    padding: 2px;
    margin: 1px;
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
  .req-fulfilled {
    color: greenyellow;
    background-color: #434f41;
  }
  .req-unfulfilled {
    color: rgb(255, 149, 122);
    background-color: #4f433e;
  }

  .schedule-selection {
    margin: 4px;
    padding: 4px;
    text-align: left;
    font-size: 1.5em;
    color:#e3e8e4;
  }

  .details-panel {
    margin: 4px;
    margin-top: 16px;
    padding: 8px;
    border: 2px solid #43494f;
    border-radius: 8px;
    font-size: 18px;
    color: #b7c0c4;
    background-color: rgba(8, 26, 32, 0.35);
  }
  .details-wildcard-title {
    font-size: 10px;
    color: #769eb1;
  }
  .details-info {
    font-size: 10px;
    color: #769eb1;
  }
</style>
  