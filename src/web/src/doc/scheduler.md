data structures (in TS)

    interface Possibility {
        sections: Section[]
        time: number[]
    }

    interface Course {
        name: string
        sections: Section[]
    }

    interface Section {
        crn: number
        sessions: Session
    }

    type Session: number[]

Normally, courses contain multiple sections, and sections contain multiple sessions.
There are some implications or prerequisites on representing the data in this format.
That is, all sessions are normal time blocks that start either at the top of the hour or on the half hour, and ends on 20 or 50 of an hour
Consequently, in this data representation, I divide all possible session time into 26 blocks of 30 minutes.
Since sessions can be scattered across the weekdays, a list of five numbers will be sufficient to represent the session time coverage of the section selection.
Representing all sessions in a certain section using a binary number where a 1 meaning this half hour is occupied, and a 0 meaning this half hour is available.

    [
        0b00000011110000,
        0b00000000000000,
        0b00000011110000
        0b00000011110000,
        0b00000000000000,
    ]
a section with sessions that is represented like this indicates that
on Monday, Wednesday, Thursday, some 2 hour slot is occupied.