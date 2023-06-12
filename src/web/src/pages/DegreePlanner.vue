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
                </div>
            </div>
            <div class="column">
                <h1>Recommendations</h1>
                <div class="text-block" v-for="(item, index) in recommendations" :key="index">
                    <h3>{{ item.head }}</h3>
                    <p>{{ item.text }}</p>
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
        recommendations: []
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
    flex: 1;
    margin: 30px;
  }
  .text-block {
    border: 2px solid #000;
    padding: 20px;
    width: 40vw;
    max-width: 600px;
    min-height: 160px;
    align-items: center;
    font-size: 1.2em;
  }
  .text-block h3 {
    color:cornflowerblue;
  }
  .column h1 {
    text-align: center;
  }
</style>
  