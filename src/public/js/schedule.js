function nullSession() {
  return { crn: null, department: null, moreFields: null }
}

class Schedule {
  constructor(someNumber) {
    this.something = someNumber
    // example schedule blocks with O(1) lookup
    this.timeBlocks = []
    for (var i = 0; i < 5; i++) {
      // day
      for (var j = 0; j < (20-8); j++) {
        this.blocks[i][j] = nullSession()
      }
    }
  }
  method() {
    console.log(this.something)
  }
}
