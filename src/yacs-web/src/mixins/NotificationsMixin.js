import { ColorService } from '@/services';
export default {
    methods: {
        notifyScheduleConflict (course, conflictSession, subsemester) {
            const vNodesMsg = this.$createElement(
                'p',
                { class: [ 'mb-0', ] },
                [
                    `${subsemester.text}: Conflict with ${conflictSession.crn} - ${conflictSession.section} `,
                    this.$createElement(
                        'div',
                        {
                            style: `
                                background-color:${ColorService.getBackgroundColor(conflictSession)};
                                border:1px solid ${ColorService.getBorderColor(conflictSession)};
                                width:13px;
                                height:13px;
                                display:inline-block;`
                        }
                    )
                ]
            );
            this.$bvToast.toast(vNodesMsg, {
                // title: `Cannot add ${section.crn} - ${section.sessions[0].section}`,
                title: `Cannot add ${course.title}`,
                variant: 'danger',
                noAutoHide: true,
            });
        }
    }
}