<template>
  <div id='footer'>
    <hr>
    <section id='main-block'>
      <b-container>
        <b-row>
          <b-col>
            <!-- TODO: Autogenerate these when doing the user side, semester select -->
            <strong class="section-head">Other Semesters</strong>
            <button
              v-for="option of semesterOptions"
              :key="option.text"
              class="btn link"
              :disabled="option.text === semester"
              @click="updateCurrentSemester(option.text)"
            >
              {{option.value}}
            </button>
          </b-col>

          <b-col>
            <strong class="section-head">Contact Us</strong>
            <a class="link" href="https://github.com/YACS-RCOS/yacs.n"  target="_blank" >Contribute (GitHub)</a>
            <a class="link" href="https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=Feature+Request&template=feature-request.md&title=Feature+Request+—+Make+YACS+Great" target="_blank" >Request a Feature</a>
            <a class="link" href= "https://github.com/YACS-RCOS/yacs.n/issues/new?assignees=&labels=bug&template=bug_report.md&title=Bug+—+Someone+made+an+oopsie" target="_blank" >Report a Bug</a>
          </b-col>

          <b-col>
            <strong class="section-head">Legal Stuff</strong>
            <a class="link" href="http://opensource-template.wikidot.com/legal:terms-of-use" target="_blank">Terms of Use</a>
            <!-- <a class="link" href=#>Cookies</a> -->
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
    props: {
      semester: String
    },
    data() {
      return {
        semesterOptions: []
      }
    },
    methods: {
      updateCurrentSemester(to) {
        console.log("in change emit of footer");
        this.$emit("changeCurrentSemester", to);
      }
    },
    created () {
      getSemesters().then(data  => {
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

    button.link {
      color: inherit;
      border-style: none;
      display: block;
      font-weight: bold;
    }

    button.link:enabled:hover{
      text-decoration: underline;
    }

    a.link {
      color: inherit;
      display: block;
    }

    a.link#current {
      color: grey;
    }

    button:disabled {
      cursor: inherit;
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
