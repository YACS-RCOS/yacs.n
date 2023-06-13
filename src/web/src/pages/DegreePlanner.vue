<template>
    <b-container fluid>
        <div class="heading">
            <h1>Degree Planner</h1>
            <h2>Requirements</h2>
        </div>
        <div class="container">
            <div class="text-block" v-for="(item, index) in requirements" :key="index">
                <h3>{{ item.name }}</h3>
                <h6>specifications: {{ item.specifications }}</h6>
                <div v-bind:class="{fulfillment:item.actual_count >= item.required_count, unfulfilled_fulfillment:item.actual_count < item.required_count}">
                    <h4>Fulfillment:</h4>
                    <div v-bind:class="{req_fulfilled:item.actual_count >= item.required_count, req_unfulfilled:item.actual_count < item.required_count}">
                        <h5>{{ item.actual_count }} / {{ item.required_count }}</h5>
                    </div>
                    <div class="fulfilled-list">
                        <li v-for="course in item.fulfillment_set" :key="course">
                            {{ course }}
                        </li>
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
    </b-container>
</template>
  
<script>
  export default {
    data() {
      return {
        requirements: [],
        recommendations: {}
      };
    },
    async created() {
        let userid = 'testuser'
        let degree = 'computer science'
        let schedule_name = 'schedule1'
        let courses = {'data structures':1, 'int algorithm':2, '4100 csci':3, 'data science 4350 csci':3, 'adv com graph 4530': 4, 'graph theory 4260': 4}

        await fetch('/api/dp/newuser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({userid, degree, schedule_name, courses}),
        });
        const response1 = await fetch('/api/dp/users/testuser/fulfillment/schedule1');
        this.requirements = await response1.json();

        const response2 = await fetch('/api/dp/users/testuser/recommend/schedule1');
        this.recommendations = await response2.json();
    },
  };
</script>
  
<style scoped>
  .container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }
  .column {
    flex: 0;
    margin: 20px;
  }
  .text-block {
    border: 8px solid #43494f;
    border-radius: 16px;
    padding: 15px;
    margin: 10px;
    min-width:200px;
    width: 50vw;
    max-width: 500px;
    min-height: 80px;
    align-items: center;
    font-size: 1em;
    background-color: #21242b;
  }
  .text-block h3 {
    color:cornflowerblue;
    font-size: 1.7em;
  }
  .text-block h6 {
    color:rgb(129, 145, 161);
    font-size: 0.8em;
  }
  .fulfillment {
    padding: 15px;
    margin: 2px;
    border-radius: 8px;
    color: #e3e8e4;
    background-color: #434f41;
  }
  .unfulfilled_fulfillment {
    padding: 15px;
    margin: 2px;
    border-radius: 8px;
    color: #e3e8e4;
    background-color: #4f433e;
  }
  .recommendations {
    padding: 15px;
    margin: 2px;
    border-radius: 8px;
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
  