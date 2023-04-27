<template>
    <div class="context-menu" :style="{ top: top + 'px', left: left + 'px' }">
        <slot></slot>
    </div>
</template>

<script>
export default {
    name: "TemplateMenu",
    props: {
        top: {
            type: Number,
            required: true
        },
        left: {
            type: Number,
            required: true
        }
    }
};
</script>

<style>
.context-menu {
    position: absolute;
    z-index: 1000;
    background-color: #fff;
    border: 1px solid #ccc;
    box-shadow: 0px 0px 5px #888888;
    padding: 5px;
}
</style>
