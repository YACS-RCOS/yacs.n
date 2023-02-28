<template>
    <div id="togglebutton"
         :class="{ 'active' : isTBActive }"
         @click.prevent="toggle">
        <slot>
            <button type="button" class="toggle-button" title="Menu">
                <span class="toggle-bar toggle-bar--1"></span>
                <span class="toggle-bar toggle-bar--2"></span>
                <span class="toggle-bar toggle-bar--3"></span>
            </button>
        </slot>
    </div>
</template>

<script>
    export default {
        data: () => ({
            isTBActive: false
        }),
        methods: {
            toggle() {
                this.isTBActive = !this.isTBActive
            }
        }
    }
</script>

<style>
   .hidden {
        visibility: hidden;
    }

    button {
        cursor: pointer;
    }

    /* remove blue outline */
    button:focus {
        outline: 0;
    }

    .toggle-button {
        position: relative;
        height: 30px;
        width: 32px;
        display: block;
        z-index: 999;
        border: 0;
        border-radius: 0;
        background-color: transparent;
        pointer-events: all;
        transition: transform .6s cubic-bezier(.165,.84,.44,1);
    }

    .toggle-bar {
        background-color: #130f40;
        position: absolute;
        top: 50%;
        right: 6px;
        left: 6px;
        height: 2px;
        width: auto;
        margin-top: -1px;
        transition: transform .6s cubic-bezier(.165,.84,.44,1),opacity .3s cubic-bezier(.165,.84,.44,1),background-color .6s cubic-bezier(.165,.84,.44,1);
    }

    .toggle-bar--1 {
        -webkit-transform: translateY(-6px);
        transform: translateY(-6px);
    }

    .toggle-bar--2 {
        transform-origin: 100% 50%;
        transform: scaleX(.8);
    }

    .toggle-button:hover .toggle-bar--2 {
        transform: scaleX(1);
    }

    .no-touchevents .toggle-bar--2:hover {
        transform: scaleX(1);
    }

    .toggle-bar--3 {
        transform: translateY(6px);
    }

    #toggle.active .toggle-button {
        transform: rotate(-180deg);
    }

    #toggle.active .toggle-bar {
        background-color: #fff;
    }

    #toggle.active .toggle-bar--1 {
        transform: rotate(45deg)
    }

    #toggle.active .toggle-bar--2 {
        opacity: 0;
    }

    #toggle.active .toggle-bar--3 {
        transform: rotate(-45deg)
    }
</style>
