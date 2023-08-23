import copy
import logging
import timeit
from enum import Enum

from ..math.dictionary_array import Dict_Array
from ..math.array_math import array_functions as af
from ..math.graph import Graph, Backwards_Overlap
from ..math.sorting import sorting
from ..dp.element import Element
from ..dp.requirement import Requirement, specification_parsing
from ..dp.fulfillment_status import Fulfillment_Status
from ..io.output import Output
from ..dp.requirement_group import Requirement_Group
from ..math.attributes import Attributes

class Bind_Type(Enum):
    NR = False
    R = True
    ALL = 2 # must be distinct in value since False gets converted to 1 in some instances

def get_element_match(requirement:Requirement, elements:set) -> list:
    '''
    Finds all courses that fulfills the given requirement
    '''
    fulfillment = Fulfillment_Status(requirement, set())

    for element in elements:
        good_match, _ = specification_parsing.attr_fulfills_specification(requirement.specifications, element.attributes)

        if good_match:
            fulfillment.add_element(element)

    return fulfillment

def get_branched_element_match(requirement:Requirement, elements:set) -> list:
    '''
    DEPRECATED, PLEASE USE specification_parsing IN REQUIREMENT.PY TO FIND ALL WILDCARD RESOLUTIONS

    
    Finds all elements that fulfills the given requirement

    Wildcards (*) may be used to dictate the fact that all courses within this template's fulfillment
    set must have the same values for that attribute. It doesn't matter which one, just so long as
    it's consistent. This is useful if we want a rule that says all courses must be in the same subject
    area or all courses must be in the same concentration/focus area, but doesn't matter which specific 
    one in particular.

    For example, concentration.* means all courses must be within the same concentration.
    If course1 has attribute concentration.1 and course2 has attribute concentration.1 and concentration.2,
    this function will return a list of fulfillment sets as follows:

    Template1.1 [concentration.1] : fulfillment courses: [course1, course2]
    Template1.2 [concentration.2] : fulfillment courses: [course2]

    If the template doesn't contain a wildcard operator, the returned list would be a single entry
    '''

    fulfillment_sets = list() # all possible fulfillments based on different combinations resulting from wildcard sauge
    all_conditions = dict() # all possible wildcard replacement conditions that can influence the result (wildcard branching)

    # current fulfillment set, will be added only if current template does not contain wildcards
    # (recursive calls remove one wildcard at a time), so essentially "leaf" branches
    # get to add their fulfillment to fulfillment_sets
    curr_fulfillment = Fulfillment_Status(requirement, set())

    for element in elements:
        good_match, conditions = specification_parsing.attr_fulfills_specification(requirement.recommender_specifications, element.attributes)

        # updates all_conditions with possible values for wildcard replacement
        for condition, condition_sat_set in conditions.items():
            current_condition_set = all_conditions.get(condition, set())
            current_condition_set.update(condition_sat_set)
            all_conditions.update({condition:current_condition_set})

        # if this is a leaf call (no wildcard branching), add to current fulfillment set
        if good_match and not len(conditions):
            curr_fulfillment.add_element(element)

    # if this is a leaf call (no wildcard branching), add to main fulfillment set
    if not len(all_conditions):
        fulfillment_sets.append(curr_fulfillment)

    print(f'all conditions: {all_conditions}')

    # if there are wildcard branching needed (we only need to pop the first one, the rest is handled by the following recursive calls
    # as each recursive call only needs to handle one)
    if not len(all_conditions):
        return fulfillment_sets
    wildcard_attr, wildcard_choices = all_conditions.popitem()

    for choice in wildcard_choices:
        # for each branching choice, make a copy of the template with the wildcard replaced with a possible value
        requirement_copy = copy.deepcopy(requirement)
        
        specifications = requirement_copy.recommender_specifications
        if wildcard_attr not in specifications:
            continue

        # we make a note of the replacements needed by storing it in replace_attributes
        requirement_copy.specifications = specifications.replace(wildcard_attr, choice)
        requirement_copy.recommender_specifications = requirement_copy.specifications

        # recursively call this function, we're guaranteed that the final return values all are wildcard-free
        fulfillment_sets.extend(get_branched_element_match(requirement_copy, elements))

    return fulfillment_sets

##############################################################################################
# fulfillment computation
##############################################################################################

def generate_resolution_combos(wildcard_resolutions:Dict_Array):

    wildcard_resolutions.convert_list_type('list')
    wildcard_resolutions.sort()
    wildcard_resolutions = wildcard_resolutions.to_tuples()

    #print(f'generate combo method: WILDCARD RESOLUTIONS: {wildcard_resolutions}')

    # if template contains wildcards, this is how many templates can result from the wildcard
    # ex: [1, 2, 2, 1, 1], meaning indexes 1 and 2 have wildcard and each evaluates to 2 possibilities
    # bound_array = [len(e) for e in max_fulfillment_possibilities]

    bound_array = [len(e[1]) for e in wildcard_resolutions]
    #print(f'generate combo method bound array: {bound_array}')

    # all possible combinations using all generated templates
    # ex: [[1, 1, 1, 1, 1], [1, 1, 2, 1, 1], [1, 2, 1, 1, 1], [1, 2, 2, 1, 1]] continuing from the example above
    combos = af.generate_combinatorics(bound_array, 0)
    #print(f'generate combo method combos array: {combos}')
    
    # list of combinations, each combination is a dictionary
    wildcard_combos = list()
    for combo in combos:
        wildcard_combo = dict()
        for i in range(len(combo)):
            wildcard_combo.update({wildcard_resolutions[i][0]:wildcard_resolutions[i][1][combo[i]]})
        wildcard_combos.append(wildcard_combo)

    #print(f'generate combo method wildcard_combos: {wildcard_combos}')

    return wildcard_combos


def group_requirements(requirements) -> list:
    '''
    the first array within the returned list will always be the group of templates without wildcards
    '''
    graph = Graph()
    wildcardless_requirements = list()
    for requirement in requirements:
        wildcards = requirement.wildcards()
        if not len(wildcards) and '*' not in requirement.name:
            wildcardless_requirements.append(requirement)
            continue
        graph.add_node(requirement, False)
        for wildcard in wildcards:
            graph.add_node(wildcard, False)
            graph.update_connection(requirement, wildcard)
            graph.update_connection(wildcard, requirement)

    connected_components = graph.connected_components()

    garbage = list()
    for component in connected_components:
        for node in component:
            if not isinstance(node, Requirement):
                garbage.append(node)
        for g in garbage:
            component.remove(g)
        garbage = list()
    
    while [] in connected_components:
        connected_components.remove([])

    connected_components.insert(0, wildcardless_requirements)
    return connected_components


##############################################################################################
# MAIN FULFILLMENT FUNCTION
##############################################################################################

def get_group_fulfillment(fulfillments:dict, groups:list, forced_groupings:dict=None) -> dict:
    tallies = dict()
    new_groups = []
    for group in groups:
        group = copy.copy(group)
        group:Requirement_Group
        tally = dict()
        # remake group requirements:
        group.requirements = []
        for requirement in fulfillments.keys():
            if (requirement.name.split('-')[0].strip().casefold() == group.name.casefold()):
                group.requirements.append(requirement)

        group.requirements = sorted(group.requirements, key=lambda obj: obj.importance, reverse=True)
        
        for requirement in group.requirements:
            requirement:Requirement
            if fulfillments.get(requirement) is None:
                continue
            fulfillment_set = fulfillments.get(requirement).fulfillment_set
            
            for element in fulfillment_set:
                element:Element
                for minimum in group.minimum_requirements.keys():
                    tally.update({minimum:int(element.attr('credits')) + tally.get(minimum, 0)})

        tallies.update({group.name:tally})
        new_groups.append(group)

    return {"groups":new_groups, "tally": tallies}


def get_fulfillment_details(all_courses, taken_courses, requirements) -> dict:
    details_all_taken = {} # requirement: [[requirement, fulfillments]]
    details_all_possible = {}
    
    for requirement in requirements:
        if requirement.display:
            print(f'BEGINNING EVAL OF DISPLAY')
            requirement_fulfillment = get_fulfillment(taken_courses, [requirement], None, None, True)
            requirement_max_fulfillment = get_fulfillment(all_courses, [requirement], None, None, True)
            #print(f'calculating display based on requirement {requirement.specifications} {requirement.display} courses {taken_courses}')
            #print(f'requirement_fulfillment_list: {requirement_fulfillment}')

            # list of fulfillment possiblities
            # calculating from all taken courses
            fulfillment_as_list = []
            for fulfillment_dict in requirement_fulfillment:
                for resolved_requirement, fulfillment_set in fulfillment_dict.items():
                    if '*' not in resolved_requirement.specifications:
                        fulfillment_as_list.append([resolved_requirement.specifications, [e.name for e in fulfillment_set.fulfillment_set]])
            details_all_taken.update({requirement.name:fulfillment_as_list})

            # calculating from all possible courses
            fulfillment_as_list_max = []
            for fulfillment_dict in requirement_max_fulfillment:
                for resolved_requirement, fulfillment_set in fulfillment_dict.items():
                    if '*' not in resolved_requirement.specifications:
                        fulfillment_as_list_max.append([resolved_requirement.specifications, [e.name for e in fulfillment_set.fulfillment_set]])
            details_all_possible.update({requirement.name:fulfillment_as_list_max})

    return {'details_all_possible': details_all_possible, 'details_all_taken': details_all_taken}


def get_optimized_fulfillment(elements_selected:set, requirements:set, forced_wildcard_resolutions:Dict_Array=None, groups=None, return_all=False, relevant_templates=None) -> dict:

    start = timeit.default_timer()
    
    if return_all:
        return get_fulfillment(elements_selected, requirements, forced_wildcard_resolutions=forced_wildcard_resolutions, groups=groups, return_all=return_all, relevant_templates=relevant_templates)
    
    ''' 
    segments templates into groups where:
        - all templates that share the same wildcard will be in the same group
        - first group will be all templates without wildcards
    '''
    grouped_requirements = group_requirements(requirements)
    wildcardless_requirements = grouped_requirements[0]
    logging.debug(f'requirement groups: {[[r.name for r in e] for e in grouped_requirements]}')

    resolved_requirements = copy.copy(wildcardless_requirements)
    for i in range(1, len(grouped_requirements)):
        requirement_group = grouped_requirements[i]
        # add wildcardless requirements to each group such that they can engage in trading/stealing optimizations
        # linearly increases runtime, which is fine since this process is to avoid the exponential growth of multiple wilcards
        requirement_group.update(wildcardless_requirements)
        fulfillments = get_fulfillment(elements_selected, requirement_group, forced_wildcard_resolutions=forced_wildcard_resolutions, relevant_templates=relevant_templates)

        # use these wildcard resolutions that led to a local best
        for requirement in fulfillments.keys():
            if requirement in wildcardless_requirements:
                continue
            resolved_requirements.append(requirement)
    
    # at this point, we obtained resolved_requirements, which represents all the requirements with resolved wildcards to use
    fulfillments = get_fulfillment(elements_selected, resolved_requirements, forced_wildcard_resolutions=forced_wildcard_resolutions, groups=groups, return_all=return_all, relevant_templates=relevant_templates)

    end = timeit.default_timer()
    logging.warn(f'\n------------------------------fulfillment runtime: {end - start}\n')

    return fulfillments


def get_fulfillment(elements_selected:set, requirements:set, forced_wildcard_resolutions:Dict_Array=None, groups=None, return_all=False, relevant_templates=None) -> dict:
    '''
    Returns:
        fulfillment: { Requirement: Fulfillment_Status }
    '''
    requirements = set(requirements)

    # unpack requirements
    if groups is not None:
        fulfillments = {}
        for group in groups:
            # print(f'group {group} :{group.separate_fulfillment}')
            if group.separate_fulfillment:
                fulfillment = get_fulfillment(elements_selected, group.requirements, forced_wildcard_resolutions, None, return_all, relevant_templates)
                fulfillments.update(fulfillment)
                requirements = requirements.difference(group.requirements)
        fulfillments.update(get_fulfillment(elements_selected, requirements, forced_wildcard_resolutions, None, return_all, relevant_templates))
        return fulfillments
    
    '''
    # generate attribute search for requirements
    requirement_names = Attributes()
    for requirement in requirements:
        requirement:Requirement
        if '*' not in requirement.name:
            requirement_names.add_attribute(requirement.name)
    
    # resolve wildcards
    for requirement in requirements:
        requirement:Requirement

        # we found a requirement that needs substitution
        if '*' in requirement.name:
            resolvable, resolution_options = specification_parsing.attr_fulfills_specification(requirement.name, requirement_names)
            if not resolvable:
                continue
            print(f'resolution options: {resolution_options}')
            resolution_tracks = Dict_Array()
            for option in resolution_options:
                resolution_tracks.add(option.split('.')[0], requirement.name[:requirement.name.index('*')] + option)
            print(f'resolution tracks: {resolution_tracks}')
            for track, track_items in resolution_tracks.dictionary.items():
                new_requirements = []
                for track_item in track_items:
                    new_requirements
    '''


    wildcard_resolutions = Dict_Array(list_type='set')

    for requirement in requirements:
        requirement:Requirement
        wildcard_resolutions.extend(requirement.wildcard_resolutions(elements_selected))


    if relevant_templates is not None:
        # find resolutions for requirement names
        template_names = Attributes()
        for template in relevant_templates:
            template_names.add_attribute(template.name)

        for requirement in requirements:
            requirement:Requirement

            # we found a requirement that needs substitution
            if '*' in requirement.name:
                resolvable, resolution_options = specification_parsing.attr_fulfills_specification(requirement.name.casefold(), template_names)
                if not resolvable:
                    continue
                #print(f'options: {resolution_options}')
                wildcard_resolutions.extend(resolution_options)
                requirement.track_resolutions = resolution_options

    if forced_wildcard_resolutions is not None and len(forced_wildcard_resolutions):
        # forced wildcard resolutions should not contain wildcards in resolution, will remove them
        forced_wildcard_resolutions.prune(lambda x : '*' in x)
        wildcard_resolutions.extend(forced_wildcard_resolutions, overwrite=True)

    print(f'wildcard resolutions: {wildcard_resolutions}')

    wildcard_combos = generate_resolution_combos(wildcard_resolutions)

    potential_fulfillments = list()

    for wildcard_combo in wildcard_combos:
        requirement_set = copy.deepcopy(requirements)
        new_requirement_set = []

        # replace template set attributes with this resolution combination
        for requirement in requirement_set:
            for old_attr, new_attr in wildcard_combo.items():
                requirement.replace_specifications(old_attr, new_attr)

        print(f'requirements before substitution: {requirement_set}')
        
        # replace requirement with requirements from specified template
        for requirement in requirement_set:
            resolved = False
            for old_attr, new_attr in wildcard_combo.items():
                if requirement.name.casefold() == old_attr:
                    template = [t for t in relevant_templates if t.name.casefold() == new_attr]
                    if len(template) == 1:
                        extended_requirements = template[0].requirements
                        for extend_requirement in extended_requirements:
                            extend_requirement.track_resolutions = requirement.track_resolutions
                            break
                        new_requirement_set.extend(extended_requirements)
                        resolved = True
                    break
            if not resolved:
                new_requirement_set.append(requirement)
        requirement_set = new_requirement_set

        print(f'requirements after substitution: {requirement_set}')


        # all courses that fulfills each template
        max_fulfillments = dict()
        for requirement in requirement_set:
            max_fulfillments.update({requirement:get_element_match(requirement, elements_selected)})

        # Output.visualize('degree', max_fulfillments, 'max fulfillment')
        all_fulfillment = dict()

        '''
        NR TEMPLATE FIRST COME FIRST SERVE FILL
        '''
        for requirement in requirement_set:
            if requirement.replacement:
                continue
            all_fulfillment.update({requirement:requirement_fill(requirement, all_fulfillment, max_fulfillments)})

        logging.debug(f'after NR fulfillment: {Output.print_fulfillment(all_fulfillment)}')

        '''
        NR TEMPLATE STEAL
        '''
        graph = generate_graph(all_fulfillment, max_fulfillments)
        for requirement in requirement_set:
            requirement_steal(requirement, all_fulfillment, max_fulfillments, graph)
        
        logging.debug(f'after NR steal: {Output.print_fulfillment(all_fulfillment)}')

        '''
        R TEMPLATE FIRST COME FIRST SERVE FILL
        '''
        for requirement in requirement_set:
            if not requirement.replacement:
                continue
            all_fulfillment.update({requirement:requirement_fill(requirement, all_fulfillment, max_fulfillments)})

        logging.debug(f'after R fulfillment: {Output.print_fulfillment(all_fulfillment)}')

        '''
        R TEMPLATE STEAL/TRADE
        '''
        for requirement in requirement_set:
            #continue
            replacement_template_steal(requirement, all_fulfillment, max_fulfillments)

        logging.debug(f'after R steal: {Output.print_fulfillment(all_fulfillment)}')
        '''
        R TEMPLATE FORCE STEAL/TRADE
        '''
        for requirement in requirement_set:
            replacement_template_steal(requirement, all_fulfillment, max_fulfillments, requirement.importance)

        potential_fulfillments.append(all_fulfillment)

        Output.visualize('degree', all_fulfillment, 'completed fulfillment calculations')

    if return_all:
        return potential_fulfillments

    # checks all fulfillment sets and return the best one
    best_fulfillment = None
    for fulfillment in potential_fulfillments:
        if best_fulfillment is None or total_unfulfilled_slots(fulfillment) < total_unfulfilled_slots(best_fulfillment):
            best_fulfillment = fulfillment
        elif total_unfulfilled_slots(fulfillment) == total_unfulfilled_slots(best_fulfillment) and total_credits(fulfillment) > total_credits(best_fulfillment):
            best_fulfillment = fulfillment

    return best_fulfillment


def generate_graph(all_fulfillment:dict, max_fulfillments:dict):
    bfs_roots = set()
    overlap_calculator = Backwards_Overlap(all_fulfillment, max_fulfillments)
    graph = Graph(set(all_fulfillment.keys()), overlap_calculator)
    
    # generate links between fulfillment statuses
    for fulfillment_status1 in all_fulfillment.values():
        fulfillment_status1:Fulfillment_Status
        if fulfillment_status1.requirement.replacement:
            continue
        if fulfillment_status1.excess_count() > 0:
            bfs_roots.add(fulfillment_status1.requirement)

        for fulfillment_status2 in all_fulfillment.values():
            fulfillment_status2:Fulfillment_Status
            if fulfillment_status2.requirement.replacement:
                continue
            graph.update_connection(fulfillment_status1.requirement, fulfillment_status2.requirement)

    graph.roots = bfs_roots
    logging.debug(str(graph))
    return graph


def element_move(giver_fulfillment:Fulfillment_Status, receiver_fulfillment:Fulfillment_Status, element:Element, graph:Graph) -> None:
    '''
    manages the graph such that it remains consistent with course moves. This method must be used
    if you want to be able to modify fulfillment sets without rebuilding the entire graph
    '''
    giver_fulfillment.remove_element(element)
    receiver_fulfillment.add_element(element)

    for out_connection in graph.outbound_connections(giver_fulfillment.requirement):
        graph.update_connection(giver_fulfillment.requirement, out_connection)

    for in_connection in graph.inbound_connections(receiver_fulfillment.requirement):
        graph.update_connection(receiver_fulfillment.requirement, in_connection)

    graph.update_connection(giver_fulfillment.requirement, receiver_fulfillment.requirement)
    graph.update_connection(receiver_fulfillment.requirement, giver_fulfillment.requirement)


def requirement_fill(requirement:Requirement, all_fulfillment:dict, max_fulfillments:dict, importance_level:int=-1) -> Fulfillment_Status:
    '''
    fills in each template with available courses in order in which the templates appear.
    
    Note that the goal is not to produce an optimal solution just yet, but rather to guarantee that ALL courses that
    can be assigned to a template is assigned to some template. (any template for now, doesn't matter which one in particular.)
    Optimizing the assignments occurs in the next steps.

    Parameters:
        template (Template): template being fulfilled, must not contain wildcards
        all_fulfillment ({Template:Fulfillment_Status}): all previously fulfilled statuses
        max_fulfillments ({Template:Fulfillment_Status}): all taken courses that can possibilty fulfill this template
        importance level (int): a course will treat all courses under this specified importance level as stealable

    Returns:
        fulfillment (Fulfillment_Status): fulfillment status of the current template
    '''

    requested_elements = max_fulfillments.get(requirement).fulfillment_set

    logging.debug(f"template {requirement} requests: {[str(e) for e in requested_elements]}")

    if requirement.replacement:
        requested_elements = sorting.dictionary_sort(num_wanted_bindings(all_fulfillment, max_fulfillments, requested_elements, Bind_Type.R))
        requested_elements.reverse()
    this_fulfillment = Fulfillment_Status(requirement, set())

    """
    we grab all courses from potential_courses that won't disturb
    the fulfillment of previous templates
    """
    for element in requested_elements:

        Output.visualize('degree', all_fulfillment, 'template fill')

        # course hasn't been added to any fulfillment sets yet, or if this template is replacement enabled
        # and the course is not in any no replacement templates
        if (not num_bindings(all_fulfillment, element)
                or (requirement.replacement and not num_bindings(all_fulfillment, element, bind_type=Bind_Type.NR))):
            this_fulfillment.add_element(element)
            all_fulfillment.update({requirement:this_fulfillment})
            continue

        # we are free to remove the course from its original places and add it here
        if not this_fulfillment.fulfilled() and element_weakly_bound(all_fulfillment, element, importance_level) and not requirement.replacement:
            element_bindings_clear(all_fulfillment, element)
            this_fulfillment.add_element(element)
            all_fulfillment.update({requirement:this_fulfillment})
            continue

    Output.visualize('degree', all_fulfillment, 'template fill')

    return this_fulfillment


def element_steal(requirement:Requirement, element:Element, all_fulfillment:dict, max_fulfillments:dict, graph:Graph, importance_level:int=-1, less_important_templates:set=None) -> bool:
    '''
    The optimization step for course assignment to templates.

    There can be scenarios where a course may take a course from another template's fulfillment set without negatively
    impacting them. This occurs when the template being stolen from has excess (fulfillment courses > required courses).

    This method uses a BFS search tree to locate all the different paths we can shuffle courses around (say template1
    needs a course template2 has. Template2 may not have excess, but Template3 does and can offer Template2 a course, so
    we transfer a course from Template3 to Template2, then the wanted course from Template2 to Template1.)

    The BFS tree has the excessively filled templates as roots and the template we want to receive a course as the target
    for search. If less_important_templates is not None, then we also add them as the roots, essentially saying that
    we can take courses from this template without compensation. This step is used as a final optimization step when
    interacting between replacement and non replacement templates due to the fact that all non replacement templates
    get computed first, even the ones that are of lower importance than existing replacement templates, so we need a way
    for the replacement templates to recapture their deserved courses.

    try to have template steal the course from aother templates in all_fulfillment, using the graph given and update
    graph appropriately after a successful transfer of courses

    returns whether steal is successful
    '''
    if less_important_templates is None:
        less_important_templates = get_less_important_requirements(all_fulfillment, importance_level)
    bfs = graph.bfs(add_roots=less_important_templates)

    # Optimization: we can leave immediately if BFS doesn't even contain the target at all
    if not bfs.contains_child(requirement):
        return False

    # the templates containing the requested course, we will BFS search for this template
    target_template = requirements_containing_element(all_fulfillment, element, True)
    if target_template is None:
        return False
    
    # the path to move courses, recorded as a list of templates traversed
    path = bfs.get_path(target_template)
    logging.debug('path: ' + ' -> '.join([str(e) for e in path]) + ' --> ' + str(requirement))

    # shifts courses along the path such that we obtain a new course
    for i in range(0, len(path) - 1):
        giver = path[i]
        receiver = path[i + 1]
        transferred_courses = graph.edge_data(giver, receiver, False)

        # avoid being greedy and taking courses that fulfill replaceable templates for yourself!
        transferred_course = sorting.bucket_sort(num_bindings(max_fulfillments, transferred_courses, Bind_Type.R))[0]

        logging.debug(f'transferring course {transferred_course} from {giver} to {receiver}')
        element_move(all_fulfillment.get(giver), all_fulfillment.get(receiver), transferred_course, graph)

        Output.visualize('degree', all_fulfillment, 'course steal')

    logging.debug(f'transferring course {element} from {path[-1]} to {all_fulfillment.get(requirement)}')
    element_move(all_fulfillment.get(path[-1]), all_fulfillment.get(requirement), element, graph)

    Output.visualize('degree', all_fulfillment, 'course steal')


def requirement_steal(requirement:Requirement, all_fulfillment:dict, max_fulfillments:dict, graph:Graph, importance_level:int=-1) -> None:
    '''
    try to steal any courses it can from other templates
    '''
    if requirement.replacement:
        return

    this_fulfillment = all_fulfillment.get(requirement)
    bfs = graph.bfs()
    if not bfs.contains_child(requirement):
        return

    for course in max_fulfillments.get(requirement).fulfillment_set:
        if this_fulfillment.fulfilled():
            return
        if course in all_fulfillment.get(requirement).fulfillment_set:
            continue
        element_steal(requirement, course, all_fulfillment, max_fulfillments, graph, importance_level)


def replacement_template_steal(requirement:Requirement, all_fulfillment:dict, max_fulfillments:dict, importance_level=-1) -> None:
    '''
    We now introduce templates with replacement. (note this computation should occur after non-replacement
    templates are fully optimized.) This is essentially a version of the course stealing method but used for
    replacement templates, since replacement templates have the unique property of allowing multiple templates
    to simulatenously posess the same course.

    Note that this method employs the stealing method as a sub-routine, so it is not a replacement for the course
    steal method but rather an extension of it.

    
    There are senarios where if the replacement templates give up a course, they will be able to in turn receive
    an otherwise 'locked' course that can more optimally fulfill them.

    For example, suppose the following scenario:
        Template 1 (no-replacement): wants course1 or course2
        Template 2 (replacement): wants course1
        Template 3 (replacement): wants course1 or course2

    If we gave course1 to template 1 and the course2 to template 2/3, only two of them (template 1 and template 3) are
    fulfilled. To remedy this, this method functions as follows:

        1) identify the courses we want that can fulfill a maximum number of replacement templates. In this case, there
        exists one such course: course1.

        2) identify the courses that, should we obtain the wanted course, we will be able to free up and give away.
        In this case, if we obtain course1, we will be able to release course2. This method does this by temporarily
        giving the templates the wanted course and generating the list of courses that can be subsequently removed
        without affecting any fulfillment sets that doesn't have excess. (NOTE a proof is still needed to demonstrate that,
        because we originally filled the templates with there are no scenarios exist in which we can give up a course that
        breaks a fulfillment set but results in more fulfillment sets being fulfilled)

        3) see if giving those courses out to the replacement templates will allow the course we want to take to be taken.
        We do this by creating two 'dummy templates', one receiver and one giver, with the receiver essentially telling
        the course stealing algorithm that we want that course in particular, and the giver containing all the donor courses
        we can offer.

        4) we will know whether this worked or not by seeing if the donor fulfillment set has had courses taken from it. If it
        did, then this trade was a success. If not, we revert everything back to how it was originally
        
        5) repeat until we go through all wanted courses or this template becomes fulfilled.
    '''
    this_fulfillment = all_fulfillment.get(requirement)

    if not requirement.replacement or this_fulfillment.fulfilled():
        return

    requested_courses = max_fulfillments.get(requirement).fulfillment_set.difference(all_fulfillment.get(requirement).fulfillment_set)
    requested_courses_sorted = sorted(num_bindings(all_fulfillment, requested_courses, Bind_Type.R).items(), key=lambda x: x[1])
    requested_courses_sorted = [x[0] for x in requested_courses_sorted]
    requested_courses_sorted.reverse()
    for course in requested_courses_sorted:
        if this_fulfillment.fulfilled():
            return

        # we bind the wanted course (which at this point, we know is unbound since the requested courses filtered out already bound courses)
        course_bind_to_R_templates(all_fulfillment, max_fulfillments, course)

        # calculate the donateable courses, which is the weakly bound courses
        donateable_courses = get_weakly_bound_elements(all_fulfillment, Bind_Type.R)

        # run BFS to see if there are a donateable course that allows for the requested course to be taken
        #
        # it's important to make sure dummy is in the name so course steal knows to remove the course
        # it stole from the actual replacement templates in addition to the dummy templates
        less_important_templates = get_less_important_requirements(all_fulfillment, importance_level, Bind_Type.NR)
        
        dummy_donor_template = Requirement('dummy donor', elements_required=0)
        dummy_donor_fulfillment = Fulfillment_Status(dummy_donor_template, fulfillment_set=donateable_courses)
        all_fulfillment.update({dummy_donor_template:dummy_donor_fulfillment})
        max_fulfillments.update({dummy_donor_template:copy.deepcopy(dummy_donor_fulfillment)})

        dummy_receiver_template = Requirement('dummy receiver', elements_required=9999)
        dummy_receiver_fulfillment = Fulfillment_Status(dummy_receiver_template, fulfillment_set=set())
        dummy_receiver_max_fulfillment = Fulfillment_Status(dummy_receiver_template, fulfillment_set={course})
        all_fulfillment.update({dummy_receiver_template:dummy_receiver_fulfillment})
        max_fulfillments.update({dummy_receiver_template:dummy_receiver_max_fulfillment})

        graph = generate_graph(all_fulfillment, max_fulfillments)

        bfs = graph.bfs(add_roots=less_important_templates)
        template_with_course = requirements_containing_element(all_fulfillment, course, True)

        if not bfs.contains_node(template_with_course):
            logging.debug(f'R template attempting to steal course {course} failed, not found in bfs tree {bfs}')
            element_bindings_clear(all_fulfillment, course, Bind_Type.R)
            all_fulfillment.pop(dummy_donor_template)
            max_fulfillments.pop(dummy_donor_template)
            all_fulfillment.pop(dummy_receiver_template)
            max_fulfillments.pop(dummy_receiver_template)
            continue
        logging.debug(f'R template stealing course {course}')
        element_steal(dummy_receiver_template, course, all_fulfillment, max_fulfillments, graph, less_important_templates=less_important_templates)

        traded_course = max_fulfillments.get(dummy_donor_template).fulfillment_set - dummy_donor_fulfillment.fulfillment_set
        if len(traded_course) == 1:
            traded_course = list(traded_course)[0]

        element_bindings_clear(all_fulfillment, traded_course, Bind_Type.R)

        this_fulfillment.add_element(course)
        all_fulfillment.pop(dummy_donor_template)
        max_fulfillments.pop(dummy_donor_template)
        all_fulfillment.pop(dummy_receiver_template)
        max_fulfillments.pop(dummy_receiver_template)


def num_bindings(all_fulfillment:dict, element:Element, bind_type:Bind_Type=Bind_Type.ALL):
    '''
    Total number of appearances of course in fulfillment sets that allow replacement

    returns integer if input is a course, returns dictionary of course:int if input is a list of courses
    '''
    if isinstance(element, list) or isinstance(element, set):
        dictionary_return = dict()
        for c in element:
            dictionary_return.update({c:num_bindings(all_fulfillment, c, bind_type)})
        return dictionary_return
    
    count = 0
    for requirement, fulfillment_status in all_fulfillment.items():
        if (bind_type == Bind_Type.ALL or requirement.replacement == bind_type.value) and element in fulfillment_status.fulfillment_set:
            count += 1
    return count


def num_wanted_bindings(all_fulfillment:dict, max_fulfillments:dict, requested_courses:list, bind_type:Bind_Type=Bind_Type.ALL) -> list:
    '''
    sorts courses inside requested_courses by the number of bindings they have
    with courses within all_fulfillment, from least to most
    '''
    num_wanted = dict()

    for course in requested_courses:
        # determine the appropriate bucket to put each course in
        num_appearances = 0
        for requirement, fulfillment_status in all_fulfillment.items():
            fulfillment_status:Fulfillment_Status
            # if the course appears inside a max fulfillment set and the fulfillment set is not fulfilled
            if ((bind_type == Bind_Type.ALL or requirement.replacement == bind_type.value)
                and (not fulfillment_status.fulfilled() and course in max_fulfillments.get(requirement).fulfillment_set)):
                num_appearances += 1
        num_wanted.update({course:num_appearances})

    return num_wanted


def get_less_important_requirements(all_fulfillment:dict, importance_level, bind_type:Bind_Type=Bind_Type.ALL) -> set:
    requirements = set()
    if importance_level == -1:
        return requirements
    for requirement in all_fulfillment.keys():
        if bind_type != Bind_Type.ALL and requirement.replacement != bind_type.value:
            continue
        if requirement.importance < importance_level:
            requirements.add(requirement)
    return requirements


def get_weakly_bound_elements(all_fulfillment:dict, bind_type:Bind_Type=Bind_Type.ALL) -> set:
    loosely_bound = set()
    strongly_bound = set()
    for requirement, fulfillment in all_fulfillment.items():
        fulfillment:Fulfillment_Status
        if bind_type != Bind_Type.ALL and requirement.replacement != bind_type.value:
            continue
        if requirement.elements_required < fulfillment.get_actual_count():
            loosely_bound.update(fulfillment.fulfillment_set)
        else:
            strongly_bound.update(fulfillment.fulfillment_set)
    return loosely_bound - strongly_bound


def element_weakly_bound(all_fulfillment:dict, element, importance_level:int=-1) -> bool:
    '''
    true if removing this course from all existing fulfillment sets will not cause a fulfilled
    template to become unfulfilled
    '''
    for fulfillment_status in all_fulfillment.values():
        fulfillment_status:Fulfillment_Status
        if element in fulfillment_status.fulfillment_set and fulfillment_status.excess_count() == 0 and fulfillment_status.requirement.importance >= importance_level:
            return False
    return True


def element_bindings_clear(all_fulfillment:dict, element, bind_type:Bind_Type=Bind_Type.ALL) -> None:
    '''
    Removes course from all existing fulfillment sets
    '''
    for requirement, fulfillment_status in all_fulfillment.items():
        fulfillment_status:Fulfillment_Status
        if bind_type != Bind_Type.ALL and requirement.replacement != bind_type.value:
            continue
        if element in fulfillment_status.fulfillment_set:
            fulfillment_status.remove_element(element)


def course_bind_to_R_templates(all_fulfillment:dict, max_fulfillments:dict, element:Element) -> None:
    '''
    add the course to all fulfillment sets that are replacement enabled
    '''
    for fulfillment_status in all_fulfillment.values():
        fulfillment_status:Fulfillment_Status
        if (fulfillment_status.requirement.replacement 
                and element in max_fulfillments.get(fulfillment_status.requirement).fulfillment_set):
            fulfillment_status.add_element(element)


def total_unfulfilled_slots(all_fulfillment:dict) -> int:
    '''
    Total number of unfulfilled courses across all fulfillment sets
    '''
    count = 0
    for fulfillment_status in all_fulfillment.values():
        fulfillment_status:Fulfillment_Status
        count += max(0, fulfillment_status.get_required_count() - fulfillment_status.get_actual_count())
    return count


def total_filled_slots(all_fulfillment:dict) -> int:
    count = 0
    for fulfillment_status in all_fulfillment.values():
        fulfillment_status:Fulfillment_Status
        count += fulfillment_status.get_actual_count()
    return count


def total_credits(all_fulfillment:dict) -> int:
    count = 0
    for fulfillment_status in all_fulfillment.values():
        fulfillment_status:Fulfillment_Status
        count += fulfillment_status.get_total_credits()
    return count


def requirements_containing_element(all_fulfillment:dict, element:Element, first_occurance_only:bool=False) -> set:
    '''
    returns a set of all templates that contain the specified course
    '''
    requirements = set()
    for requirement, fulfillment_status in all_fulfillment.items():
        fulfillment_status:Fulfillment_Status
        if element in fulfillment_status.fulfillment_set:
            if first_occurance_only:
                return requirement
            requirements.add(requirement)

    if first_occurance_only and not len(requirements):
        return None
    return requirements
