<template>

    <div class="tree-menu">
        <div class="title" :style="indent(indentDistance)" v-if="label != itemFlag">
            {{ label }}
        </div>
        <div class="items" :style="indent(indentDistance)" v-if="label == itemFlag">
            <div v-for="(item, index) in nodes" :key="index">
                {{ item }}
            </div>
        </div>
        <div v-if="label != itemFlag">
            <catalog-tree v-for="(next_nodes, node) in nodes" :key="node" :nodes="next_nodes" :label="node" :depth="depth + 1"></catalog-tree>
        </div>
    </div>

</template>

<script>
export default {
    props: ['label', 'nodes', 'depth'],
    name: 'catalog-tree',
    data() {
      return {
        indentDistance: 8,
        itemFlag: '$items',
      };
    },
  
    methods: {
        indent(amount) {
            return {
                transform: `translate(${this.depth * amount}px)`
            }
        }
    },

    async created() {
    },  
}
</script>

<style scoped>
    .title {
        font-size: 18px;
    }
    .items {
        font-size: 12px;
    }
</style>
