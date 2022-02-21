import { computed, ref } from 'vue'

const COLORS = [
    // H    S    L
    [345, 1  , .92], // "#ffd4df", red
    [197, .88, .90], // "#ceeffc", blue
    [ 46, 1  , .91], // "#fff4d0", yellow
    [116, .64, .91], // "#dcf7da", green
    [300, .57, .93], // "#f7e2f7", purple
    [ 30, .28, .90], // "#ede6df", brown
    [ 33, 1  , .91], // "#ffe9cf", orange
    [304, 1  , .91], // "#ffd1fc", pink
    [178, .90, .92], // "#d9fdfc", aquamarine
    [  0, .29, .90], // "#e2caca", maroon, changed
    [197, .51, .85], // "#a3cfe1", dark blue, changed
    [116, .41, .85], // "#acdba9", dark green, changed
];
const TEXT_COLORS = [
    [341, .69, .48], // "#d1265d", red
    [201, .78, .37], // "#1577aa", blue
    [ 38, .61, .46], // "#bf8a2e", yellow
    [140, 1  , .27], // "#008a2e", green
    [304, .37, .38], // "#853d80", purple
    [ 20, .51, .41], // "#9d5733", brown
    [ 20, .70, .51], // "#d9652b", orange
    [304, 1  , .50], // "#ff00ef", pink
    [176, 1  , .32], // "#00a499", aquamarine
    [  0, .82, .37], // "#ab1111", maroon
    [205, .98, .24], // "#014779", dark blue
    [152, .72, .24], // "#116940", dark green
];
const BORDER_COLORS = [
    [341, 1  , .56], // "#ff2066", red
    [197, 1  , .47], // "#00aff2", blue
    [ 43, 1  , .64], // "#ffcb45", yellow
    [127, .66, .57], // "#48da58", green
    [296, .58, .65], // "#d373da", purple
    [ 30, .26, .52], // "#a48363", brown
    [ 28, 1  , .60], // "#ff9332", orange
    [304, 1  , .50], // "#ff00ef", pink
    [179, 1  , .50], // "#00fff9", aquamarine
    [  0, 1  , .37], // "#ab0000", maroon, changed
    [205, .99, .36], // "#015fa2", dark blue, changed
    [126, .55, .38], // "#298e33", dark green, changed
];

/**
 * Color Blind Friendly Colors
 *
 * Adapted from Paul Tot's discrete rainbow scheme
 * https://personal.sron.nl/~pault/#fig:scheme_rainbow_discrete
 *
 * Colors adjusted using https://davidmathlogic.com/colorblind/
 *
 * Color palette tested using
 * https://www.color-blindness.com/coblis-color-blindness-simulator/
 */
const COLOR_BLIND_COLORS = [
    [358, .96, .60], // "#fb373e", red
    [208, .61, .72], // "#8cbbe3", blue
    [ 57, .91, .65], // "#f7f056", yellow
    [ 85, .46, .77], // "#cae0ab", green
    [286, .26, .84], // "#dccce1", purple
    [ 30, .28, .90], // "#ede6df", brown
    [ 42, .91, .61], // "#f6c141", orange
    [303, 1  , .96], // "#ffebfe", pink
    [212, .51, .60], // "#6596cd", aquamarine
    [  0, .29, .84], // "#e2caca", maroon
    [196, .67, .55], // "#2286aa", dark blue, changed
    [112, .38, .66], // "#90c987", dark green
];
const COLOR_BLIND_BORDER_COLORS = [
    [341, 1  , .32], //"#a30034", red
    [197, 1  , .47], //"#00aff2", blue
    [ 43, 1  , .64], //"#ffcb45", yellow
    [ 85, .46, .56], //"#97c25b", green
    [296, .58, .65], //"#d373da", purple
    [ 30, .26, .52], //"#a48363", brown
    [ 28, 1  , .60], //"#ff9332", orange
    [304, 1  , .84], //"#ffadfa", pink
    [212, .51, .40], //"#32639a", aquamarine
    [  0, 1  , .34], //"#ab0000", maroon
    [205, .99, .32], //"#015fa2", dark blue
    [126, .55, .36], //"#298e33", dark green
];

const occupied = ref(new Set())
const NUM_COLORS = 12;
const NUM_INDEX = ref(0)


export const occupyColor = () => {
    while (occupied.value.has(NUM_INDEX.value)) {
        NUM_INDEX.value = NUM_INDEX.value >= NUM_COLORS - 1 ? 0 : NUM_INDEX.value + 1
    }
    occupied.value.add(NUM_INDEX.value)
    return {
        index: NUM_INDEX.value,
        color: COLORS[NUM_INDEX.value].map(color => color <= 1 ? color * 100 : color),
        text: TEXT_COLORS[NUM_INDEX.value].map(color => color <= 1 ? color * 100 : color),
        border: BORDER_COLORS[NUM_INDEX.value].map(color => color <= 1 ? color * 100 : color),
    }
}

export const unOccupyColor = (index) => {
    occupied.value.delete(index)
}