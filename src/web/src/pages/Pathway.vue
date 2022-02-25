
<template>
  <b-container fluid>
    <b-breadcrumb :items="breadcrumbNav"></b-breadcrumb>
    <div v-if="categories.length > 0" class="mx-auto w-75">
      <b-row>
        <!-- splited categories into 2 arrays, so we can have 2 columns -->
        <b-col
          v-for="(catCol, index) in categoryCols"
          :key="`catCol-${index}`"
          md="6"
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
              <!-- Pathway Title  -->
              <b-row>
                <PathwayCategoriesList
                  :pathways="categoryObj['Pathways']"
                ></PathwayCategoriesList>
              </b-row>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </div>
    <CenterSpinner
      v-else
      :height="80"
      :fontSize="1.3"
      loadingMessage="Pathways"
      :topSpacing="30"
    />
  </b-container>
</template>



<script>
import json from './pathwayV2.json'
import PathwayCategoriesListComponenet from "@/components/PathwayCategoriesList";
import CenterSpinnerComponent from "../components/CenterSpinner";

export default {
  name: "Pathway",
  components: {
    PathwayCategoriesList: PathwayCategoriesListComponenet,
    CenterSpinner: CenterSpinnerComponent,
  },
  data() {
    return {
      breadcrumbNav: [
        {
          text: "YACS",
          to: "/",
        },
        {
          text: "Pathways"
        }
      ],
      categories: json,
      showPath: null
    };
  },
  computed:{
    categoryCols() {
      let ret = [];
      let col1 = [];
      let col2 = [];
      for (var i = 0; i < this.categories.length; i++) {
        if (i%2 == 0) {
          col1.push(this.categories[i]);
        } else {
          col2.push(this.categories[i])
        }
      }
      ret.push(col1);
      ret.push(col2);
      return ret;
    }
  }
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
  background: rgba(108, 90, 90, 0.15);
  border-bottom: rgba(108, 90, 90, 0.1), solid, 1px;
}
</style>
