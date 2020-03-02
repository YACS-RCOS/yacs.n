// export class ColorAssignment {
//     primary
// 	constructor (
// 		public readonly primary: string,
// 		public readonly text: string,
// 		public readonly border: string
// 	) { }
// }

export default class ColorService {
    static COLORS = ['#ffd4df', '#ceeffc', '#fff4d0', '#dcf7da', '#f7e2f7', '#ede6df', '#ffe9cf'];
    static TEXT_COLORS = ['#d1265d', '#1577aa', '#bf8a2e', '#008a2e', '#853d80', '#9d5733', '#d9652b'];
    static BORDER_COLORS = ['#ff2066', '#00aff2', '#ffcb45', '#48da58', '#d373da', '#a48363', '#ff9332'];
    static NUM_COLORS = 7;

    // TODO: use something persistent
    assignmentIncr = 0;
    colorAssignments = new Map();

    getColor (id) {
        const assignment = this.assign(id);
        return {
            primary: ColorService.COLORS[assignment],
            text: ColorService.TEXT_COLORS[assignment],
            border: ColorService.BORDER_COLORS[assignment]
        };
    }

    assign (id) {
        if (this.colorAssignments.has(id))
            return this.colorAssignments.get(id);
        else
            return this.colorAssignments.set(id, this.nextAssignment()).get(id);
    }

    nextAssignment () {
        return (++this.assignmentIncr) % ColorService.NUM_COLORS;
    }
}
