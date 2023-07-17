import timeit
from .catalog import Catalog
from .fulfillment_status import Fulfillment_Status
from ..math.sorting import sorting
from ..recommender.recommender import Recommender
from .fulfill import get_branched_element_match

def recommend(elements_selected, catalog:Catalog, requirements:set, custom_tags=None, enable_tensorflow=False) -> dict:
    '''
    gives possible courses to take

    returns: recommendation (dict): {best template : {alternative template : fulfillment list}}
    '''
    if custom_tags is not None and not len(custom_tags):
        custom_tags = None

    start = timeit.default_timer()
    if Recommender.cache is None:
        print(f' RECOMMENDER --- BUILDING RECOMMENDER')
        Recommender.initialize(catalog)
        Recommender.ENABLE_TENSORFLOW = enable_tensorflow
        print(f' RECOMMENDER --- FINISHED BUILDING RECOMMENDER')
    recommendation = dict() # {best template : {alternative template : fulfillment list}}
    # note that best template == alternative template if best template does not contain wildcards

    for requirement in requirements:
        print(f'  RECOMMENDER --- SOLVING {requirement}')
        # here we receive the list of fulfillment sets from get course match
        matches = get_branched_element_match(requirement, catalog.get_elements())
        matches_dict = {}

        for matched_fulfillment in matches:
            matched_fulfillment:Fulfillment_Status

            # remove the elements already selected
            elements_recommended = matched_fulfillment.fulfillment_set

            for element in elements_selected:
                elements_recommended.discard(element)

            # course_R_bindings = num_bindings(max_fulfillments, recommended_courses, Bind_Type.R)
            course_relevances = Recommender.embedded_relevance(elements_selected, elements_recommended, catalog.tags, custom_tags)

            final_score = dict()
            for element in elements_recommended:
                score = course_relevances.get(element)
                # score += (course_R_bindings.get(course) / 50.0)
                final_score.update({element : score})

            elements_recommended = sorting.dictionary_sort(final_score)
            matches_dict.update({matched_fulfillment.requirement:elements_recommended})

        recommendation.update({requirement:matches_dict})

    end = timeit.default_timer()
    print(f'\r---------------------------------------recommendation runtime: {end - start}\n')

    return recommendation
