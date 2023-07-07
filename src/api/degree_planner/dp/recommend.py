import timeit
from .template import Template
from ..math.graph import Graph
from ..math.graph import Backwards_Overlap
from ..math.array_math import array_functions as af
from ..math.dictionary_array import Dict_Array
from ..io.output import Output
from ..math.sorting import sorting
from ..math.graph import Graph
from .course import Course
from .fulfillment_status import Fulfillment_Status
from .degree import Bind_Type

def recommend(taken_courses, best_fulfillments:dict, catalog, custom_tags=None) -> dict:
    '''
    gives possible courses to take

    returns: recommendation (dict): {best template : {alternative template : fulfillment list}}
    '''
    if custom_tags is not None and not len(custom_tags):
        custom_tags = None

    start = timeit.default_timer()


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
        print(f'1 {best_template}')
        # here we receive the list of fulfillment sets from get course match
        matches = best_template_original.get_course_match(catalog.courses())
        matches_dict = {}

        for matched_fulfillment in matches:

            """
            for each match, rank the matched courses
            """
            # remove the courses already taken
            recommended_courses = matched_fulfillment.get_fulfillment_set()
            
            fulfilled_courses = 0
            for course in best_fulfillment.get_fulfillment_set():
                recommended_courses.discard(course)
                fulfilled_courses += 1

            matched_fulfillment.get_template().courses_fulfilled = fulfilled_courses
            matched_fulfillment.get_template().importance = fulfilled_courses

            # course_R_bindings = num_bindings(max_fulfillments, recommended_courses, Bind_Type.R)
            course_relevances = catalog.recommender.embedded_relevance(taken_courses, recommended_courses, custom_tags)
            
            final_score = dict()
            for course in recommended_courses:
                score = course_relevances.get(course)
                # score += (course_R_bindings.get(course) / 50.0)
                final_score.update({course : score})

            recommended_courses = sorting.dictionary_sort(final_score)
            matches_dict.update({matched_fulfillment.get_template():recommended_courses})

        recommendation.update({best_template:matches_dict})

    end = timeit.default_timer()
    print(f'\r---------------------------------------recommendation runtime: {end - start}\n')
    
    return recommendation

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