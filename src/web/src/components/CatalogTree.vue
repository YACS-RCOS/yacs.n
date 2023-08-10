<template>
    <div>
        <div v-if="depth == 0">
            <div v-if="label != itemFlag && label != tagFlag">
                <div v-for="(next_nodes, node) in nodes" :key="node">
                    <div v-if="node == itemFlag">
                        <catalog-tree :nodes="next_nodes" :label="node" :depth="depth + 1" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :resolutionDict="resolutionDict" @setDegree="setDegree"></catalog-tree>
                    </div>
                    <div v-if="node != itemFlag" :style="getGridStyle()">
                        <catalog-tree :nodes="next_nodes" :label="node" :depth="depth + 1" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :resolutionDict="resolutionDict" @setDegree="setDegree"></catalog-tree>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="label == itemFlag">
            <div v-for="(item, index) in nodes" :key="index">
                <button class="degree-button" :style="getElementColor(item, 'backgroundColor', [0, -5, -10, -0.1])" type="button" @click="setDegree(item)">
                    {{ item }}
                </button>
            </div>
        </div>

        <div v-if="depth != 0 && label != itemFlag" class="tree-branch" :style="getElementColor(tag, 'backgroundColor', [0,0,-5,-0.05])">
            <div class="title" :style="[getElementColor(tag, 'backgroundColor', [0, -5, -20, -0.1]), getElementColor(label, 'color')]" v-if="label != itemFlag && label != tagFlag">
                {{ label }}
            </div>
            <div v-if="label != itemFlag && label != tagFlag">
                <div :style="getGridStyle()">
                    <div v-for="(next_nodes, node) in extractNodes()" :key="node">
                        <catalog-tree class="tree-branch-grid-item" :nodes="next_nodes" :label="node" :depth="depth + 1" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :resolutionDict="resolutionDict" @setDegree="setDegree"></catalog-tree>
                    </div>
                </div>
                <div v-for="(next_nodes, node) in extractItems()" :key="node">
                    <div>
                        <div>
                            <catalog-tree :nodes="next_nodes" :label="node" :depth="depth + 1" :subjectColors="subjectColors" :subjectGroupColors="subjectGroupColors" :resolutionDict="resolutionDict" @setDegree="setDegree"></catalog-tree>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    props: ['label', 'tags', 'nodes', 'depth', 'subjectColors', 'subjectGroupColors', 'resolutionDict'],
    name: 'catalog-tree',
    data() {
      return {
        baseWidth: 700,
        attenuation: 0.45,
        indentDistance: 8,
        itemFlag: '$items',
        tagFlag: '$properties',
        tag: '',
        color: '',
        textColor: 'rgba(0,0,0,1)',
      };
    },
  
    methods: {
        extractNodes() {
            let nodes = this.nodes;
            return Object.keys(nodes)
            .filter(key => key !== "$items" && key !== "$properties")
            .reduce((result, key) => {
            result[key] = nodes[key];
            return result;
            }, {});
        },
        extractItems() {
            let nodes = this.nodes;
            return Object.keys(nodes)
            .filter(key => key == "$items")
            .reduce((result, key) => {
            result[key] = nodes[key];
            return result;
            }, {});
        },
        setDegree(degree) {
            this.$emit('setDegree', degree);
        },
        getWidthStyle() {
            let layer_width = this.baseWidth * (this.attenuation ** (this.depth - 1));
            //console.log("layer width: " + layer_width);
            return {
                width: layer_width,
            }
        },
        getGridStyle() {
            let width = this.baseWidth * (this.attenuation ** this.depth)

            return {
                display: 'grid',
                gridTemplateColumns: `repeat(auto-fill, ${width}px)`,
                gap: '8px',
            }
        },
        getElementColor(element, type='backgroundColor', spice=null) {
            if (element == this.label) {
                if (this.textColor.length > 0) {
                    return {
                        [type]: `${this.textColor}`
                    };
                }
            }

            element = element.toLowerCase();
            if (spice == null) {
                spice = [0,0,0,0];
            }
            if (this.resolutionDict && element in this.resolutionDict) {
                element = this.resolutionDict[element];
            }
            if (element == '' && this.color == '') {
                return this.makeHSLColor(0,0,0,0)
            }
            // finding the color
            let element_color = '';
            if (this.color.length > 0) {
                element_color = this.color;
            }
            else if (element in this.subjectColors) {
                element_color = this.subjectColors[element];
            }
            else if (element in this.subjectGroupColors) {
                element_color = this.subjectGroupColors[element];
            }

            // setting the color
            if (typeof element_color === 'string') {
                return {
                    [type]: `${element_color}`
                };
            }
            if (element_color.length == 3) {
                return this.makeHSLColor((element_color[0] + spice[0]) % 360, element_color[1] + spice[1], element_color[2] + spice[2], -1, type)
            }
            else if (element_color.length == 4) {
                return this.makeHSLColor((element_color[0] + spice[0]) % 360, element_color[1] + spice[1], element_color[2] + spice[2], element_color[3] + spice[3], type)
            }
        },

        makeHSLColor(hue, saturation, lightness, alpha=-1, type='backgroundColor') {
            if (alpha != -1) {
                return {
                    [type]: `hsla(${hue}, ${saturation}%, ${lightness}%, ${alpha})`
                };
            }
            return {
                [type]: `hsl(${hue}, ${saturation}%, ${lightness}%)`
            };
        },

        indent(amount) {
            return {
                transform: `translate(${this.depth * amount}px)`
            }
        },
        parseProperties(properties) {
            for (let i = 0; i < properties.length; i++) {
                let property_split = properties[i].split('=');
                if (property_split.length != 2) {
                    continue
                }
                let property_head = property_split[0];
                let property_value = property_split[1].replace('!dot', '.');
                this.evaluateProperty(property_head, property_value);
            }
        },
        evaluateProperty(head, value) {
            //console.log("processing prop " + head + "," + value)
            if (head == 'tag') {
                this.tag = value;
            }
            if (head == 'color') {
                this.color = value;
            }
            if (head == 'textColor') {
                this.textColor = value;
            }
        },
    },

    async created() {
        if ("$properties" in this.nodes) {
            this.parseProperties(this.nodes['$properties']['$items']);
        }
    },  
}
</script>

<style scoped>
    .tree-branch-grid-item {
        width: 100;
        height: 100;
        display:flex;
    }
    .tree-branch {
        border-radius: 12px;
        padding: 8px;
        margin: 8px;
        width: 100%;
        height: 100%;
        backdrop-filter: blur(4px);
    }
    .title {
        font-size: 18px;
        font-weight: 700;
        color: #1f2121;
        border: none;
        border-radius: 12px;
        padding: 4px;
        padding-left: 10px;
        padding-right: 10px;
        margin: 4px;
    }
    .degree-button {
        text-justify: left;
        font-size: 14px;
        width: 100%;
        border: none;
        padding: 2px;
        border-radius: 12px;
        color: #1f2121;
        margin: 1px;
    }
    .degree-button:hover {
        text-justify: left;
        border: solid 2px #bec4c4;
        padding: 0px;
        border-radius: 12px;
        margin: 1px;
        color: #1f2121;
    }
</style>
