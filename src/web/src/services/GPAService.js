const mp = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2,
    "D+": 1.3,
    "D": 1,
    "F": 0,
};

export const calculateGPA = (courses) => {
    let points = 0.0;
    let credits = 0;
    for(const course in courses) {
        points += mp[course['grade']];
        credits += course['credits'];
    }

    return 4 * (points / credits);
};

export const calculateGPABulk = (pastGPA, pastCredits, currentGPA, currentCredits) => {
    const totalCredits = pastCredits + currentCredits;
    const pastPercentage = pastGPA / 4.0;
    const currentPercentage = currentGPA / 4.0;
    
    newGPA = 4 *(pastPercentage * pastCredits + currentPercentage * currentCredits) / totalCredits;

    return newGPA;
};