<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>

    <!-- button to switch between alphabet order and category order -->
    <div style="float: left;" class="w-10">
      <b-button
        @click="listAlphabet()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        List by Alphabet
      </b-button>
      <br />
      <b-button
        @click="listCate()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >
        Button for all majors
      </b-button>
      <br />
      <b-button
        @click="Majors()"
        style="
          margin-top: 10px;
          color: #007bff;
          border: solid #007bff;
          background-color: transparent;
        "
      >

    <div class="container">
        <h3 class="p-3 text-center">Required Classes for Degree</h3>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Semester:</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{user.Classes}}</td>
                </tr>
            </tbody>
        </table>
    </div>    

        List by Category
      </b-button>
    </div>
    <div v-if="categories.length > 0" class="mx-auto w-75">
      <!-- pop-up window -->
      <b-modal ref="my-modal">
        <div class="block text-left" v-if="showPath != null" md="10">
          <h3
            class="text-center"
            style="color: #007bff; margin-top: -5px; margin-bottom: 5px;"
          >
            {{ showPath.Name[0] }}
          </h3>
          <br />
          <div v-for="(item, itemName) in showPath" :key="itemName">
            <h4 style="color: #3395ff; margin-top: -20px;">
              {{ itemName + ": " }}
            </h4>
            <li
              v-for="course in item"
              :key="course"
              v-on:click="goPage(course)"
              class="courseInPath"
            >
              {{ course }}
            </li>
            <br />
          </div>
        </div>
      </b-modal>

      <b-row>
        <!-- splitted categories into 2 arrays, so we can have 2 columns -->
        <b-col
          v-for="(catCol, index) in categoryCols"
          :key="`catCol-${index}`"
          md="6"
          v-show="cateShow"
        >
          <b-row
            v-for="categoryObj in catCol"
            :key="categoryObj['Category Name'][0]"
            class="categoryBox border m-2 mb-4"
          >
            <b-col>
              <!-- Category Title  -->
              <b-row class="category-title">
                <h3 class="m-1 ml-2">
                  {{ categoryObj["Category Name"][0] }}
                </h3>
              </b-row>
              <!-- degreetemplates Names  -->
              <b-row>
                <div class="d-flex flex-column flex-grow-1">
                  <!-- LOOP Through the degreetemplates Categories list -->
                  <div
                    v-for="degreetemplates in categoryObj['DegreeTemplates']"
                    :key="degreetemplates['Name'][0]"
                    role="tablist"
                  >
                    <div class="mt-1 mb-1 w-100">
                      <!-- degreetemplates button -->
                      <b-button
                        @click="ShowPath(degreetemplates)"
                        squared
                        variant="light"
                        class="degreetemplates-button m-0 ml-1"
                      >
                        {{ degreetemplates["Name"][0] }}
                      </b-button>
                    </div>
                  </div>
                </div>
              </b-row>
            </b-col>
          </b-row>
        </b-col>

        <!-- splitted DegreeTemplates in alphabet order -->
        
      </b-row>
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.3"
      loadingMessage="DegreeTemplates"
      :topSpacing="30"
    />
  </b-container>
</template>

<script>
import json from "./degreetemplatesV2.json";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "DegreeTemplates",
  components: {
    CenterSpinner: CenterSpinnerComponent,
  },
};
</script>

<style>
.gridContainer {
  display: inline-grid;
  grid-template-columns: auto auto;
  justify-content: center;
  align-content: center;
}

.categoryBox {
  text-align: center;
}

.category-title {
  color: hsl(211, 100%, 60%);
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}

.degreetemplates-button {
  display: inline-block;
  background: white;
  border-style: none;
  text-align: justify;
  width: 95%;
}

.degreetemplates-button:hover {
  background: rgba(108, 90, 90, 0.15) !important;
}

.courseInPath {
  cursor: pointer;
}

.courseInPath:hover {
  background-color: rgba(39, 130, 230, 0.5);
}
</style>

