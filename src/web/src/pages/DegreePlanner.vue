<template>
    <b-container fluid>
        <h1>Degree Planner</h1>
        <div class="container">
            <div class="column">
                <h1>Requirements</h1>
                <div class="text-block" v-for="(item, index) in requirements" :key="index">
                    <h3>{{ item.head }}</h3>
                    <p>{{ item.text }}</p>
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
        requirements: [
            {"head": "req1",
            "text": "jwefo ajweif aojewfji aowei jfaoiwe jfoawe jfioawj efoiawejfoiaj ewofi ajewf haiewuo fhaioewuhf oiahue foaiuwehfoiauewhofau wfioa wehofi uahewoifu ahweoifu ahoewifu haoewiu fhaoiewu fhoaiue fhoaiu ewaiowue aoiuwefhoaiuwe aiouew fho"}, 
            {"head": "req2",
            "text": "requirement 2"},
            {"head": "req3",
            "text": "requirement 3"},
            {"head": "req4",
            "text": "requirement 4"}],
        recommendations: [
            {"head": "recommend1",
            "text": "recommendation 1"},
            {"head": "recommend2",
            "text": "recommendation 2"},
            {"head": "recommend3",
            "text": "recommendation 3"}]
      };
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
  