<template>
    <b-container fluid>
        <h1>Degree Planner</h1>
        <div class="container">
            <div class="column">
                <h1>Requirements</h1>
                <div class="text-block" v-for="(item, index) in requirements" :key="index">
                    <h3>{{ item.name }}</h3>
                    <h6>specifications: {{ item.specifications }}</h6>
                    <h6>{{ item.actual_count }} / {{ item.required_count }}</h6>
                    <li v-for="course in item.fulfillment_set" :key="course">
                        {{ course }}
                    </li>
                    <br>
                    <h4>Recommendations:</h4>
                    <div class="recommendations" v-for="recommendation in recommendations[item.name]" :key="recommendation">
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
    display: flex;
    justify-content: space-around;
    padding: 30px;
    justify-content: center;
    align-items: flex-start;
  }
  .column {
    flex: 0;
    margin: 30px;
  }
  .text-block {
    border: 10px solid #43494f;
    border-radius: 20px;
    padding: 20px;
    margin: 12px;
    min-width:400px;
    width: 50vw;
    max-width: 800px;
    min-height: 100px;
    align-items: center;
    font-size: 1em;
  }
  .text-block h3 {
    color:cornflowerblue;
  }
  .text-block h6 {
    color:lightslategray;
  }
  .column h1 {
    text-align: center;
  }
</style>
  