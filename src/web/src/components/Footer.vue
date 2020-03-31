<template>
  <div id='footer'>
    <hr>
    <section id='main-block'>
      <b-container>
        <b-row>
          <b-col>
            <!-- TODO: Autogenerate these when doing the user side, semester select -->
            <strong class="section-head">Other Semesters</strong>
            <!-- <div>
              <template v-for="semester in semesterOptions" >
                <a class="link" v-for="semester in semesterOptions" :class="link" :value="semester.value" :key="semester.text" :href="/?semester=FALL 2020">
                  {{ semester.text }}
                </a>
              </template>
            </div> -->
            <a class="link" href=#>Fall 2019</a>
            <a class="link" href=#>Fall 2020</a>
            <a class="link" href=#>Spring 2020</a>
            <a class="link" href=#>Summer 2020</a>
          </b-col>

          <b-col>
            <strong class="section-head">Contact Us</strong>
            <a class="link" href=#>Contribute (GitHub)</a>
            <a class="link" href=#>Request a Feature</a>
            <a class="link" href=#>Report a Bug</a>
          </b-col>

          <b-col>
            <strong class="section-head">Legal Stuff</strong>
            <a class="link" href=#>Terms of Use</a>
            <a class="link" href=#>Cookies</a>
            <a class="link" href=#>EULA</a>
          </b-col>

        </b-row>
      </b-container>
    </section>
    <!-- <hr> -->
    <section id='credits'>
      <p class='text-center'>Built by YACS under RCOS at RPI</p>
    </section>

  </div>
</template>

<script>

import { getSemesters } from '@/services/YacsService';

export default {
    name: 'Footer',
    data() {
      return {
        field: 0,
        semesterOptions: []
      }
    },
    methods: {
    },
    created () {
    getSemesters().then(({ data }) => {
            this.semesterOptions.push(...data.map(s => ({text: s.semester, value: s.semester})));
            });
    }

}
</script>

<style scoped lang="scss">

#footer {
  #main-block {
    background: white;
    color: black;
    padding: 25px 0;
    width: 100%;
    height: auto;
    padding-left: 150px;

    strong.section-head {
      color: #3D4959;
      margin-bottom: 2px;
    }

    a.link {
      color: inherit;
      display: block;
    }

  }

  #credits {
    /* background: #3D4959; */
    width: 100%;
    height: auto;
    padding: 0px;
    margin: 0px;
    padding: 10px 0px;

    p {
      color: #3D4959;
      margin: 0;
    }
  }

}

</style>
