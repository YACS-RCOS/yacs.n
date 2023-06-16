'''
contains degree class and a set of helper functions
'''

import json
import timeit
import copy
from enum import Enum
from .template import Template
from ..math.graph import Graph
from ..math.graph import Backwards_Overlap
from ..math.array_math import array_functions as af
from ..io.output import Output
from ..math.sorting import sorting
from .course import Course
from .fulfillment_status import Fulfillment_Status

class Bind_Type(Enum):
    NR = False
    R = True
    ALL = 2 # must be distinct in value since False gets converted to 1 in some instances

class Degree():
    '''
    Stores a list of rules, inserted in order of importance

    Rules will be computed sequentially for fulfillment. A rule computed first will
    be guaranteed the fact that subsequential rules cannot remove courses from its
    fulfillment set if it does not have any excess.

    rules can additionally be marked as high priority to compute its fulfillment first
    '''

    def __init__(self, name, catalog=None):
        self.name = name
        self.templates = list()
        self.catalog = catalog
        self.io = Output(Output.OUT.CONSOLE, auto_clear=True)

        self.MAX_IMPORTANCE = 1000 # essentially the maximum number of templates possible


    def add_template(self, template:Template):
        '''
        templates should be inserted in order of importance
        '''
        if not len(self.templates):
            template.importance = self.MAX_IMPORTANCE
        else:
            template.importance = self.templates[-1].importance - 1
        self.templates.append(template)

    def remove_template(self, template:Template):
        ''' removes template object '''
        self.templates.remove(template)

    def get_template(self, template_name) -> Template:
        ''' gets template by name, O(n) time '''
        for template in self.templates:
            if template.name == template_name:
                return template
        return None


    ##############################################################################################
    # fulfillment computation
    ##############################################################################################

    def generate_template_combinations(self, taken_courses, template_set:list=None) -> list:
        '''
        generates a list of all possible template combinations resulted from wildcard usage
        '''
        # max fulfillment set for every template, including wildcards

        if template_set is None:
            template_set = self.templates

        max_fulfillment_possibilities = list()
        for template in template_set:
            max_fulfillment_possibilities.append(template.get_course_match(taken_courses))

        # if template contains wildcards, this is how many templates can result from the wildcard
        bound_array = [len(e) for e in max_fulfillment_possibilities]

        # all possible combinations using all generated templates
        combos = af.generate_combinatorics(bound_array, 1)
        all_template_combinations = list()

        for combo in combos:
            templates_to_use = []

            # generates the combination of templates to use
            for i in range(0, len(combo)):
                # gets the fulfillment status to use based on the number in combo
                fulfillment_status = max_fulfillment_possibilities[i][combo[i] - 1]
                templates_to_use.append(fulfillment_status.get_template())
            all_template_combinations.append(templates_to_use)

        return all_template_combinations


    ##############################################################################################
    # MAIN FULFILLMENT FUNCTION
    ##############################################################################################

    def fulfillment(self, taken_courses:set, template_sets:list=None, attributes_to_replace:list=None) -> dict:
        '''
        Generates the best fulfillment set by assigning courses to the templates stored along with
        each degree.

        If a wildcard is encountered, all possible values of that wildcard will be attempted and the
        best one in the end applied and stored in the return dictionary. (For example, suppose
        Template1 has attribute [concentration.*]. This means all courses must be within the same
        concentration, not mattering which one in particular. The return we receive would describe
        the concentration that provided the best fulfillment, and would have an attribute such as
        [concentration.ai].)

        parameters:
            taken_courses (set): all courses that is to be used to generate the fulfillment sets
            templates_set (list): specify list of templates to use, leave empty to use default set of this degree

        returns:
            all_fulfillment (dict): {template : Fulfillment_set}
                template is the template evaluated, with all wildcard tokens replaced by the best token
                fulfillment_set objects contain the courses that fulfill that template
        '''
        start = timeit.default_timer()
        # all fulfillment sets based on each possible combination of templates resulted from wildcard templates
        potential_fulfillments = list()

        if template_sets is None:
            template_sets = self.templates
        if attributes_to_replace is not None:
            template_sets = copy.deepcopy(template_sets)


            # just for now, we treat attributes to replace as a list where [template, attribute to replace, template, attribute to replace ...]
            for i in range(0, len(attributes_to_replace) - 1, 2):
                for template in template_sets:
                    print(f'comparing {template.name} and {attributes_to_replace[i]}')
                    if template.name.casefold() == attributes_to_replace[i].casefold():
                        attribute = attributes_to_replace[i + 1]
                        attribute_head = attribute[:attribute.find('.')]
                        template.replace_specifications(attribute_head, attribute)

        for template_set in self.generate_template_combinations(taken_courses, template_sets):

            # all courses that fulfills each template
            max_fulfillments = dict()
            for template in template_set:
                max_fulfillments.update({template:template.get_course_match(taken_courses)[0]})

            Output.visualize('degree', max_fulfillments, 'max fulfillment')

            all_fulfillment = dict()

            '''
            NR TEMPLATE FIRST COME FIRST SERVE FILL
            '''
            for template in template_set:
                if template.replacement:
                    continue
                all_fulfillment.update({template:self.template_fill(template, all_fulfillment, max_fulfillments)})

            self.io.debug(f'after NR fulfillment: {Output.print_fulfillment(all_fulfillment)}')

            '''
            NR TEMPLATE STEAL
            '''
            graph = self.generate_graph(all_fulfillment, max_fulfillments)
            for template in template_set:
                self.template_steal(template, all_fulfillment, max_fulfillments, graph)
            
            self.io.debug(f'after NR steal: {Output.print_fulfillment(all_fulfillment)}')

            '''
            R TEMPLATE FIRST COME FIRST SERVE FILL
            '''
            for template in template_set:
                if not template.replacement:
                    continue
                all_fulfillment.update({template:self.template_fill(template, all_fulfillment, max_fulfillments)})

            self.io.debug(f'after R fulfillment: {Output.print_fulfillment(all_fulfillment)}')

            '''
            R TEMPLATE STEAL/TRADE
            '''
            for template in template_set:
                #continue
                self.replacement_template_steal(template, all_fulfillment, max_fulfillments)

            self.io.debug(f'after R steal: {Output.print_fulfillment(all_fulfillment)}')

            '''
            R TEMPLATE FORCE STEAL/TRADE
            '''
            for template in template_set:
                self.replacement_template_steal(template, all_fulfillment, max_fulfillments, template.importance)

            potential_fulfillments.append(all_fulfillment)

            Output.visualize('degree', all_fulfillment, 'completed fulfillment calculations')

        # checks all fulfillment sets and return the best one
        best_fulfillment = None
        for fulfillment in potential_fulfillments:
            if best_fulfillment is None or total_unfulfilled_slots(fulfillment) < total_unfulfilled_slots(best_fulfillment):
                best_fulfillment = fulfillment
            elif total_unfulfilled_slots(fulfillment) == total_unfulfilled_slots(best_fulfillment) and total_filled_slots(fulfillment) > total_filled_slots(best_fulfillment):
                best_fulfillment = fulfillment

        end = timeit.default_timer()
        self.io.info(f'\nfulfillment runtime: {end - start}\n')
        return best_fulfillment


    def generate_graph(self, all_fulfillment:dict, max_fulfillments:dict):
        bfs_roots = set()
        overlap_calculator = Backwards_Overlap(all_fulfillment, max_fulfillments)
        graph = Graph(set(all_fulfillment.keys()), overlap_calculator)
        
        # generate links between fulfillment statuses
        for fulfillment_status1 in all_fulfillment.values():
            if fulfillment_status1.get_template().replacement:
                continue
            if fulfillment_status1.excess_count() > 0:
                bfs_roots.add(fulfillment_status1.get_template())
            for fulfillment_status2 in all_fulfillment.values():
                if fulfillment_status2.get_template().replacement:
                    continue
                graph.update_connection(fulfillment_status1.get_template(), fulfillment_status2.get_template())
        graph.roots = bfs_roots
        self.io.debug(str(graph))
        return graph


    def course_move(self, giver_fulfillment:Fulfillment_Status, receiver_fulfillment:Fulfillment_Status, course:Course, graph:Graph) -> None:
        '''
        manages the graph such that it remains consistent with course moves. This method must be used
        if you want to be able to modify fulfillment sets without rebuilding the entire graph
        '''
        giver_fulfillment.remove_fulfillment_course(course)
        receiver_fulfillment.add_fulfillment_course(course)

        for out_connection in graph.outbound_connections(giver_fulfillment.get_template()):
            graph.update_connection(giver_fulfillment.get_template(), out_connection)

        for in_connection in graph.inbound_connections(receiver_fulfillment.get_template()):
            graph.update_connection(receiver_fulfillment.get_template(), in_connection)

        graph.update_connection(giver_fulfillment.get_template(), receiver_fulfillment.get_template())
        graph.update_connection(receiver_fulfillment.get_template(), giver_fulfillment.get_template())


    def template_fill(self, template:Template, all_fulfillment:dict, max_fulfillments:dict, importance_level:int=-1) -> Fulfillment_Status:
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

        requested_courses = max_fulfillments.get(template).get_fulfillment_set()

        self.io.debug(f"template {template} requests: {[str(e) for e in requested_courses]}")

        if template.replacement:
            requested_courses = sorting.dictionary_sort(num_wanted_bindings(all_fulfillment, max_fulfillments, requested_courses, Bind_Type.R))
            requested_courses.reverse()
        this_fulfillment = Fulfillment_Status(template, template.courses_required, set())

        """
        we grab all courses from potential_courses that won't disturb
        the fulfillment of previous templates
        """
        for course in requested_courses:

            Output.visualize('degree', all_fulfillment, 'template fill')

            # course hasn't been added to any fulfillment sets yet, or if this template is replacement enabled
            # and the course is not in any no replacement templates
            if (not num_bindings(all_fulfillment, course)
                    or (template.replacement and not num_bindings(all_fulfillment, course, bind_type=Bind_Type.NR))):
                this_fulfillment.add_fulfillment_course(course)
                all_fulfillment.update({template:this_fulfillment})
                continue

            # we are free to remove the course from its original places and add it here
            if not this_fulfillment.fulfilled() and course_weakly_bound(all_fulfillment, course, importance_level) and not template.replacement:
                course_bindings_clear(all_fulfillment, course)
                this_fulfillment.add_fulfillment_course(course)
                all_fulfillment.update({template:this_fulfillment})
                continue

        Output.visualize('degree', all_fulfillment, 'template fill')

        return this_fulfillment


    def course_steal(self, template:Template, course:Course, all_fulfillment:dict, max_fulfillments:dict, graph:Graph, importance_level:int=-1, less_important_templates:set=None) -> bool:
        '''
        The optimization step for course assignment to templates.

        There can be scenarios where a course may take a course from another template's fulfillment set without negatively
        impacting them. This occurs when the template being stolen from has excess (fulfillment courses > required courses).

        This method uses a BFS search tree to locate all the different paths we can shuffle courses around (say template1
        needs a course template2 has. Template2 may not have excess, but Template3 does and can offer Template2 a course, so
        we transfer a course from Template3 to Template2, then the wanted course from Template2 to Template1.)

        The BFS tree has the excessly filled templates as roots and the template we want to receive a course as the target
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
            less_important_templates = get_less_important_templates(all_fulfillment, importance_level)
        bfs = graph.bfs(less_important_templates)

        # Optimization: we can leave immediately if BFS doesn't even contain the target at all
        if not bfs.contains_child(template):
            return False

        # the templates containing the requested course, we will BFS search for this template
        target_template = templates_containing_course(all_fulfillment, course, True)
        if target_template is None:
            return False
        
        # the path to move courses, recorded as a list of templates traversed
        path = bfs.get_path(target_template)
        self.io.debug('path: ' + ' -> '.join([str(e) for e in path]) + ' --> ' + str(template))

        # shifts courses along the path such that we obtain a new course
        for i in range(0, len(path) - 1):
            giver = path[i]
            receiver = path[i + 1]
            transferred_courses = graph.edge_data(giver, receiver, False)

            # avoid being greedy and taking courses that fulfill replaceable templates for yourself!
            transferred_course = sorting.bucket_sort(num_bindings(max_fulfillments, transferred_courses, Bind_Type.R))[0]

            self.io.debug(f'transferring course {transferred_course} from {giver} to {receiver}')
            self.course_move(all_fulfillment.get(giver), all_fulfillment.get(receiver), transferred_course, graph)

            Output.visualize('degree', all_fulfillment, 'course steal')

        self.io.debug(f'transferring course {course} from {path[-1]} to {all_fulfillment.get(template)}')
        self.course_move(all_fulfillment.get(path[-1]), all_fulfillment.get(template), course, graph)

        Output.visualize('degree', all_fulfillment, 'course steal')


    def template_steal(self, template:Template, all_fulfillment:dict, max_fulfillments:dict, graph:Graph, importance_level:int=-1) -> None:
        '''
        try to steal any courses it can from other templates
        '''
        if template.replacement:
            return

        this_fulfillment = all_fulfillment.get(template)
        bfs = graph.bfs()
        if not bfs.contains_child(template):
            return

        for course in max_fulfillments.get(template).get_fulfillment_set():
            if this_fulfillment.fulfilled():
                return
            if course in all_fulfillment.get(template).get_fulfillment_set():
                continue
            self.course_steal(template, course, all_fulfillment, max_fulfillments, graph, importance_level)


    def replacement_template_steal(self, template:Template, all_fulfillment:dict, max_fulfillments:dict, importance_level=-1) -> None:
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
        this_fulfillment = all_fulfillment.get(template)

        if not template.replacement or this_fulfillment.fulfilled():
            return

        requested_courses = max_fulfillments.get(template).get_fulfillment_set().difference(all_fulfillment.get(template).get_fulfillment_set())
        requested_courses_sorted = sorting.bucket_sort(num_bindings(all_fulfillment, requested_courses, Bind_Type.R))

        for course in requested_courses_sorted:
            if this_fulfillment.fulfilled():
                return

            # we bind the wanted course (which at this point, we know is unbound since the requested courses filtered out already bound courses)
            course_bind_to_R_templates(all_fulfillment, max_fulfillments, course)

            # calculate the donateable courses, which is the weakly bound courses
            donateable_courses = get_weakly_bound_courses(all_fulfillment, Bind_Type.R)

            # run BFS to see if there are a donateable course that allows for the requested course to be taken
            #
            # it's important to make sure dummy is in the name so course steal knows to remove the course
            # it stole from the actual replacement templates in addition to the dummy templates
            less_important_templates = get_less_important_templates(all_fulfillment, importance_level, Bind_Type.NR)
            
            dummy_donor_template = Template('dummy donor', courses_required = 0)
            dummy_donor_fulfillment = Fulfillment_Status(dummy_donor_template, fulfillment_set=donateable_courses)
            all_fulfillment.update({dummy_donor_template:dummy_donor_fulfillment})
            max_fulfillments.update({dummy_donor_template:copy.deepcopy(dummy_donor_fulfillment)})

            dummy_receiver_template = Template('dummy receiver', courses_required = 999)
            dummy_receiver_fulfillment = Fulfillment_Status(dummy_receiver_template, fulfillment_set=set())
            dummy_receiver_max_fulfillment = Fulfillment_Status(dummy_receiver_template, fulfillment_set={course})
            all_fulfillment.update({dummy_receiver_template:dummy_receiver_fulfillment})
            max_fulfillments.update({dummy_receiver_template:dummy_receiver_max_fulfillment})

            graph = self.generate_graph(all_fulfillment, max_fulfillments)

            bfs = graph.bfs(less_important_templates)
            template_with_course = templates_containing_course(all_fulfillment, course, True)

            if not bfs.contains_node(template_with_course):
                self.io.debug(f'R template attempting to steal course {course} failed, not found in bfs tree {bfs}')
                course_bindings_clear(all_fulfillment, course, Bind_Type.R)
                all_fulfillment.pop(dummy_donor_template)
                max_fulfillments.pop(dummy_donor_template)
                all_fulfillment.pop(dummy_receiver_template)
                max_fulfillments.pop(dummy_receiver_template)
                continue
            self.io.debug(f'R template stealing course {course}')
            self.course_steal(dummy_receiver_template, course, all_fulfillment, max_fulfillments, graph, less_important_templates=less_important_templates)

            traded_course = max_fulfillments.get(dummy_donor_template).get_fulfillment_set() - dummy_donor_fulfillment.get_fulfillment_set()
            if len(traded_course) == 1:
                traded_course = list(traded_course)[0]

            course_bindings_clear(all_fulfillment, traded_course, Bind_Type.R)

            this_fulfillment.add_fulfillment_course(course)
            all_fulfillment.pop(dummy_donor_template)
            max_fulfillments.pop(dummy_donor_template)
            all_fulfillment.pop(dummy_receiver_template)
            max_fulfillments.pop(dummy_receiver_template)


    ##############################################################################################
    # fulfillment recommendation
    ##############################################################################################

    def recommend(self, taken_courses, best_fulfillments:dict=None, custom_tags=None) -> dict:
        '''
        gives possible courses to take

        returns: recommendation (dict): {best template : {alternative template : fulfillment list}}
        '''
        if best_fulfillments is None:
            best_fulfillments = self.fulfillment(taken_courses)
        if custom_tags is not None and not len(custom_tags):
            custom_tags = None

        start = timeit.default_timer()

        """
        compute max_fulfillments for the sake of potential bindings calculation
        """
        max_fulfillments = dict()
        

        for best_template, best_fulfillment in best_fulfillments.items():
            original_specification = best_template.original_specifications
            best_template_original = Template(best_template.name, specifications=original_specification, replacement=best_template.replacement, courses_required=1)
            matches = best_template_original.get_course_match(self.catalog.courses())

            status = matches[0]
            for matched_fulfillment in matches:
                status.add_fulfillment_course(matched_fulfillment.get_fulfillment_set())
                max_fulfillments.update({best_template_original:status})

        recommendation = dict() # {best template : {alternative template : fulfillment list}}
        # note that best template == alternative template if best template does not contain wildcards

        for best_template, best_fulfillment in best_fulfillments.items():

            """
            compute matches by calling get_course_match and receiving matches based on wildcard combinations

            each combination is stored as an 'alternative template' under their respective best template inside recommender
            """

            original_specification = best_template.original_specifications
            # remaking the original template
            best_template_original = Template(f'{best_template.name}', specifications=original_specification, replacement=best_template.replacement, courses_required=1)

            # here we receive the list of fulfillment sets from get course match
            matches = best_template_original.get_course_match(self.catalog.courses())
            matches_dict = {}

            for matched_fulfillment in matches:

                """
                for each match, rank the matched courses
                """

                self.io.debug(f'max match for template {best_template_original}: \n{matches}\n')
                # remove the courses already taken
                recommended_courses = matched_fulfillment.get_fulfillment_set()
                
                fulfilled_courses = 0
                for course in best_fulfillment.get_fulfillment_set():
                    recommended_courses.discard(course)
                    fulfilled_courses += 1

                matched_fulfillment.get_template().courses_fulfilled = fulfilled_courses
                matched_fulfillment.get_template().importance = fulfilled_courses

                course_R_bindings = num_bindings(max_fulfillments, recommended_courses, Bind_Type.R)
                course_relevances = self.catalog.recommender.embedded_relevance(taken_courses, recommended_courses, custom_tags)
                
                final_score = dict()
                for course in recommended_courses:
                    score = course_relevances.get(course)
                    score += (course_R_bindings.get(course) / 50.0)
                    final_score.update({course : score})

                recommended_courses = sorting.dictionary_sort(final_score)
                matches_dict.update({matched_fulfillment.get_template():recommended_courses})

                for course in recommended_courses:
                    self.io.print(f'score {final_score.get(course)} for course {str(course)}, keywords: {course.keywords}')

            recommendation.update({best_template:matches_dict})

        end = timeit.default_timer()
        self.io.info(f'\rrecommendation runtime: {end - start}\n')
       
        return recommendation
    

    def json(self) -> json:
        degree = dict()
        degree.update({self.name:self.templates})
        return json.dumps(degree)

    def __str__(self):
        return self.name

    def __repr__(self):
        rep = f"degree: {self.name} \n"
        for template in self.templates:
            rep += repr(template) + '\n'
        return rep

    def __eq__(self, other):
        if not isinstance(other, Degree):
            return False
        if self.name == other.name and self.rules == other.rules:
            return True
        return False

    def __hash__(self):
        i = 0
        for template in self.templates:
            i += hash(template)
        i += hash(self.name)
        return i


######################################
# FULFILLMENT SET CALC HELPER FUNCTIONS
######################################


def num_bindings(all_fulfillment:dict, course:Course, bind_type:Bind_Type=Bind_Type.ALL):
    '''
    Total number of appearances of course in fulfillment sets that allow replacement

    returns integer if input is a course, returns dictionary of course:int if input is a list of courses
    '''
    if isinstance(course, list) or isinstance(course, set):
        dictionary_return = dict()
        for c in course:
            dictionary_return.update({c:num_bindings(all_fulfillment, c, bind_type)})
        return dictionary_return
    
    count = 0
    for template, fulfillment_status in all_fulfillment.items():
        if (bind_type == Bind_Type.ALL or template.replacement == bind_type.value) and course in fulfillment_status.get_fulfillment_set():
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
        for template, fulfillment_status in all_fulfillment.items():
            # if the course appears inside a max fulfillment set and the fulfillment set is not fulfilled
            if ((bind_type == Bind_Type.ALL or template.replacement == bind_type.value)
                and (not fulfillment_status.fulfilled() and course in max_fulfillments.get(template).get_fulfillment_set())):
                num_appearances += 1
        num_wanted.update({course:num_appearances})

    return num_wanted


def get_less_important_templates(all_fulfillment:dict, importance_level, bind_type:Bind_Type=Bind_Type.ALL) -> set:
    templates = set()
    if importance_level == -1:
        return templates
    for template in all_fulfillment.keys():
        if bind_type != Bind_Type.ALL and template.replacement != bind_type.value:
            continue
        if template.importance < importance_level:
            templates.add(template)
    return templates


def get_weakly_bound_courses(all_fulfillment:dict, bind_type:Bind_Type=Bind_Type.ALL) -> set:
    loosely_bound = set()
    strongly_bound = set()
    for template, fulfillment in all_fulfillment.items():
        if bind_type != Bind_Type.ALL and template.replacement != bind_type.value:
            continue
        if template.courses_required < fulfillment.get_actual_count():
            loosely_bound.update(fulfillment.get_fulfillment_set())
        else:
            strongly_bound.update(fulfillment.get_fulfillment_set())
    return loosely_bound - strongly_bound


def course_weakly_bound(all_fulfillment:dict, course, importance_level:int=-1) -> bool:
    '''
    true if removing this course from all existing fulfillment sets will not cause a fulfilled
    template to become unfulfilled
    '''
    for fulfillment_status in all_fulfillment.values():
        if course in fulfillment_status.get_fulfillment_set() and fulfillment_status.excess_count() == 0 and fulfillment_status.get_template().importance >= importance_level:
            return False
    return True


def course_bindings_clear(all_fulfillment:dict, course, bind_type:Bind_Type=Bind_Type.ALL) -> None:
    '''
    Removes course from all existing fulfillment sets
    '''
    for template, fulfillment_status in all_fulfillment.items():
        if bind_type != Bind_Type.ALL and template.replacement != bind_type.value:
            continue
        if course in fulfillment_status.get_fulfillment_set():
            fulfillment_status.remove_fulfillment_course(course)


def course_bind_to_R_templates(all_fulfillment:dict, max_fulfillments:dict, course:Course) -> None:
    '''
    add the course to all fulfillment sets that are replacement enabled
    '''
    for fulfillment_status in all_fulfillment.values():
        if (fulfillment_status.get_template().replacement 
                and course in max_fulfillments.get(fulfillment_status.get_template()).get_fulfillment_set()):
            fulfillment_status.add_fulfillment_course(course)


def total_unfulfilled_slots(all_fulfillment:dict) -> int:
    '''
    Total number of unfulfilled courses across all fulfillment sets
    '''
    count = 0
    for fulfillment_status in all_fulfillment.values():
        count += max(0, fulfillment_status.get_required_count() - fulfillment_status.get_actual_count())
    return count


def total_filled_slots(all_fulfillment:dict) -> int:
    count = 0
    for fulfillment_status in all_fulfillment.values():
        count += fulfillment_status.get_actual_count()
    return count


def templates_containing_course(all_fulfillment:dict, course:Course, first_occurance_only:bool=False) -> set:
    '''
    returns a set of all templates that contain the specified course
    '''
    templates = set()
    for template, fulfillment_status in all_fulfillment.items():
        if course in fulfillment_status.get_fulfillment_set():
            if first_occurance_only:
                return template
            templates.add(template)

    if first_occurance_only and not len(templates):
        return None
    return templates
