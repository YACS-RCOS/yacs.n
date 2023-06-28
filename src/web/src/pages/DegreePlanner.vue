<template>
    <b-container fluid>
        <div class="heading">
            <h1>Degree Planner</h1>
            <h2>Requirements</h2>
        </div>

        <div>
          <input class="text-input" v-model="textInput" type="text" placeholder="enter command for degree planner" @keyup.enter="dp_command">
        </div>
        <div>
          <h4 class="schedule-selection">
            Schedule: {{ schedule_name }} <br>
            Degree: {{ degree }}
          </h4>
        </div>
        <div class="container">
            <div class="text-block" v-for="(item, index) in requirements" :key="index">
                <h3>{{ item.name }}</h3>
                <div v-if="item.content">
                  <div v-if="'specifications' in item">
                    <h6>specifications: {{ item.specifications }}</h6>
                  </div>
                  <div v-bind:class="{fulfillment:item.actual_count >= item.required_count, unfulfilled_fulfillment:item.actual_count < item.required_count}">
                      <div v-bind:class="{req_fulfilled:item.actual_count >= item.required_count, req_unfulfilled:item.actual_count < item.required_count}">
                          <h5>{{ item.actual_count }} / {{ item.required_count }}</h5>
                      </div>
                      <div class="fulfilled-list">
                          <li v-for="course in item.fulfillment_set" :key="course">
                              {{ course }}
                          </li>
                      </div>
                  </div>
                  <div class="alternatives" v-if="Object.keys(item.wildcard_resolutions).length > 0">
                    <div v-for="(alternative_choices, alternative_orig) in item.wildcard_resolutions" :key="alternative_orig">
                      <div v-for="alternative_choice in alternative_choices" :key="alternative_choice">
                        <button v-bind:class="{'alternative-buttons':!alternative_choice.endsWith('*'), 'alternative-buttons-wildcard':alternative_choice.endsWith('*')}" type="button" @click="fulfillment(userid, [alternative_orig, alternative_choice])">
                          {{ format_alternative(alternative_choice) }}
                      </button>
                      </div>
                    </div>
                  </div>
                  <br>
                  <div class="recommendations" v-if="recommendations[item.name].length > 0 && recommendations[item.name][0].fulfillment_set.length > 0">
                      <h4>Recommendations:</h4>
                      <div class="recommendation-list" v-for="recommendation in recommendations[item.name]" :key="recommendation">
                          <h6>specifications: {{ recommendation.specifications }}</h6>
                          <li v-for="course in recommendation.fulfillment_set" :key="course">
                              {{ course }}
                          </li>
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
        userid: 'testuser',
        degree: 'computer science',
        schedule_name: 'schedule1',
        requirements: [],
        recommendations: {}
      };
    },
    methods: {
        format_alternative(str) {
          if (str.includes('*')) {
            str = str.split('*')[0] + " automatically select"
          }
          str = str.replace('.', ': ');
          return str
        },
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
        async update_variables(variable_updates) {
          for(let [key, value] of Object.entries(variable_updates)) {
            if (this[key] !== undefined) {
              this[key] = value;
            }
          }
        },
        async fetch_data() {
            let userid = this.userid;

            this.fulfillment(userid, []);
            this.recommend(userid);
        },

        async newuser(userid, degree, schedule_name, courses) {
          await fetch('/api/dp/newuser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, degree, schedule_name, courses}),
          });
        },

        async fulfillment(userid, attributes_replacement) {
          const response1 = await fetch('/api/dp/fulfillment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, attributes_replacement}),
          });

          this.requirements = await response1.json();
        },

        async recommend(userid) {
          const response2 = await fetch('/api/dp/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userid),
          });
          this.recommendations = await response2.json();
        },
    },
    async created() {
      let courses = {};
      let userid = this.userid;
      let degree = this.degree;
      let schedule_name = this.schedule_name;

      this.newuser(userid, degree, schedule_name, courses);
      this.fulfillment(userid, []);
      this.recommend(userid);
    },
  };
</script>
  
<style scoped>
  .schedule-selection {
    text-align: center;
    color:#e3e8e4;
  }
  .container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 5px;
  }
  .text-input{
    border:2px solid #21242b;
    border-radius:5px;
    width:150px;
    padding:5px;
    background-color:#393b40;
    position:fixed;
  }
  .text-input:focus{
    width:300px;
    border:4px;
    background-color:#3f4146;
  }
  .text-block {
    border: 6px solid #43494f;
    border-radius: 12px;
    padding: 8px;
    margin: 8px;
    min-width:250px;
    width: 30vw;
    max-width: 550px;
    min-height: 70px;
    align-items: center;
    font-size: 0.8em;
    background-color: #21242b;
  }
  .text-block h3 {
    color:cornflowerblue;
    font-size: 1.6em;
  }
  .text-block h4 {
    font-size: 1.4em;
  }
  .text-block h6 {
    color:rgb(129, 145, 161);
    font-size: 0.8em;
  }
  .fulfillment {
    padding: 10px;
    margin: 2px;
    border-radius: 6px;
    color: #e3e8e4;
    background-color: #434f41;
  }
  .unfulfilled_fulfillment {
    padding: 10px;
    margin: 2px;
    border-radius: 6px;
    color: #e3e8e4;
    background-color: #4f433e;
  }
  .alternative-buttons {
    border-radius: 6px;
    border: none;
    padding: 4px;
    margin: 2px;
    color:#e3e8e4;
    background-color: #3f4146;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons:hover {
    background-color:#21242b;
    color: #c7e4e1;
    border: none;
  }
  .alternative-buttons-wildcard {
    border-radius: 6px;
    border: none;
    padding: 4px;
    margin: 2px;
    color:#d8e8dc;
    background-color: #497348;
    transition: background-color 0.2s ease;
  }
  .alternative-buttons-wildcard:hover {
    background-color:#171d1a;
    color: #c7e4e1;
    border: none;
  }
  .recommendations {
    padding: 5px;
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
  