class Fulfillment_Status():
    '''
    A data structure to store information on fulfillment status of a template
    '''
    def __init__(self, requirement, fulfillment_set:set=None):
        if fulfillment_set == None: fulfillment_set = set()
        self.requirement = requirement
        self.fulfillment_set = fulfillment_set

    def fulfilled(self):
        return self.get_actual_count() - self.get_required_count() >= 0

    def get_required_count(self) -> int:
        return self.requirement.elements_required

    def get_actual_count(self) -> int:
        return len(self.fulfillment_set)
    
    def get_total_credits(self) -> int:
        count = 0
        for course in self.fulfillment_set:
            count += int(course.attr('credits'))
        return count

    """
    returns whether the element is added (not previously present)
    """
    def add_element(self, element) -> bool:
        len_original = len(self.fulfillment_set)
        self.fulfillment_set.add(element)
        return len_original != len(self.fulfillment_set)

    """
    returns whether the element requested to be removed is present (successful removal)
    """
    def remove_element(self, element) -> bool:
        len_original = len(self.fulfillment_set)
        self.fulfillment_set.discard(element)
        return len_original != len(self.fulfillment_set)

    def unfulfilled_count(self) -> int:
        return max(0, self.get_required_count() - self.get_actual_count())

    def excess_count(self) -> int:
        return max(0, self.get_actual_count() - self.get_required_count())

    def __repr__(self) -> str:
        return f"requirement {self.requirement.name} specifications: {self.requirement.specifications}  required count: {self.get_required_count()}  fulfillment set: {[str(e) for e in self.fulfillment_set]}"

    def __str__(self):
        return f"{self.requirement.name} fulfillment set: {[str(e) for e in self.fulfillment_set]}"

    def __eq__(self, other):
        if not isinstance(other, Fulfillment_Status):
            return False
        return self.requirement == other.requirement

    def __gt__(self, other):
        return self.requirement.importance < other.requirement.importance

    def __lt__(self, other):
        return self.requirement.importance > other.requirement.importance

    def __ge__(self, other):
        return self.requirement.importance <= other.requirement.importance

    def __le__(self, other):
        return self.requirement.importance >= other.requirement.importance

    def __len__(self):
        return self.get_actual_count()

    def __hash__(self):
        return hash(self.requirement)
