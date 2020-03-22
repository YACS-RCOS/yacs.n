<template>
    <b-card
        :class="`admin-link-card ${type}`"
        :title="type"
    >
        <button class="btn help-btn"><font-awesome-icon :icon="helpIcon"/></button>
        {{ getCardDescription(type) }}
        <font-awesome-icon class="card-type-icon" :icon="getCardIcon(type)" />
        <button class="btn add-btn" @click="$emit('click', type)">
            <font-awesome-icon :icon="openIcon" />
        </button>
    </b-card>
</template>

<script>
import { faDatabase, faInfo, faPlus, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons';

export default {
    name: "AdminPageLink",
    props: {
        type: String
    },
    components: {},
    data () {
        return {
            helpIcon: faInfo,
            openIcon: faExternalLinkAlt,
            faPlus
        }
    },
    methods: {
        getCardDescription(type) {
            if (type === 'csv') {
                return `
                    An easy way to import course data
                    into the YACS backend system.
                `;
            }
            else if (type === 'date') {
                return `
                    Map date ranges to semester parts.
                `;
            }
        },
        getCardIcon(type) {
            if (type === 'csv' || type === 'date') {
                return faDatabase;
            }
        }
    }
}
</script>

<style lang="scss">
$csvCardBgG1: #2f00ff;
$csvCardBgG2: #0070ff;
$dateCardBgG1: rgb(9, 161, 9);
$dateCardBgG2: rgb(11, 207, 11);
.admin-link-card {
    position: relative;
    display: flex;
    color: white;
    min-height: 200px;
    max-width: 200px;
    margin-left: 3em;
    border-radius: 0 10% 0 0;
    box-shadow: 0px 1px 10px 2px #0006;
}
.admin-link-card.csv {
    background: linear-gradient(45deg, $csvCardBgG1, $csvCardBgG2);
}
.admin-link-card.date {
    background: linear-gradient(45deg, $dateCardBgG1, $dateCardBgG2);
}
.card-type-icon {
    position: absolute;
    bottom: 5px;
    right: 5px;
    opacity: 0.5;
    font-size: 5rem;
}
.help-btn {
    position: absolute;
    // top: -1px;
    // right: -1px;
    // border-radius: 0 56% 0 27%;
    color: white;
    top: 0px;
    right: 0px;
    border-radius: 100%;
    background-clip: padding-box;
    // background-color: #0000ffCF;
    // border: solid #00000021 1px;
    border: 0;
    justify-content: center;
    display: flex;
    width: 15%;
    height: 15%;
}
.add-btn {
    color: #09fb09;
    background-color: white;
    box-shadow: 1px 1px 10px 1px #000000AF;
    font-size: 1em;
    border-radius: 100%;
    position: absolute;
    border: transparent;
    font-size: 1em;
    bottom: calc(50% - 1em);
    right: calc(0px - 1em);
}
</style>