<template>
  <div id='footer'>
    <hr>
    <section id='main-block'>
      <b-container>
        <b-row>
          <b-col>
            <!-- TODO: Autogenerate these when doing the user side, semester select -->
            <strong class="section-head">Other Semesters</strong>
            <a class="link" id="current">
              {{ currentSemester }}
            </a>
            <a 
              v-for="semester in otherSemesters"
              :key="semester.text"
              :value="semester.value"
              :href="`/?semester=${semester.text}`"
              class="link"
              > {{semester.value}}
            </a>
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

import { getDefaultSemester }  from '@/services/AdminService';

export default {
    name: 'Footer',
    data() {
      return {
        semesterOptions: [],
        currentSemester: ''
      }
    },
    methods: {
    },
    created () {
      if(this.$route.query.semester){
        this.currentSemester = this.$route.query.semester;
      }
      else{
        getDefaultSemester().then(semester => {
          this.currentSemester = semester;
        });
      }
      getSemesters().then(data  => {
        this.semesterOptions.push(...data.map(s => ({text: s.semester, value: s.semester})));
        });
    },
    computed: {
      otherSemesters: function() {
        var retSemesters = [];
        for(var item of this.semesterOptions){
          if(item.value != this.currentSemester){
            retSemesters.push(item);
          }
        }
        return retSemesters;
      } 
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

    a.link#current {
      color: grey;
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
