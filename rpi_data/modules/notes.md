get courses: http://rpi.apis.acalog.com/v2/search/courses?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=listing&catalog=26&options[limit]=0

get catalog id: http://rpi.apis.acalog.com/v2/content?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=getCatalogs


Get course ids? http://rpi.apis.acalog.com/v2/content?options[full]=1&method=getItems&type=courses&key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&catalog=26

http://rpi.apis.acalog.com/v2/search/courses?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=listing&catalog=26&options[limit]=0 

API Key: 3eef8a28f26fb2bcc514e6f1938929a1f9317628

Default link? http://rpi.apis.acalog.com/v2/content?

Get courses - http://rpi.apis.acalog.com/v1/content?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&method=getItems&options[full]=1&catalog=26&type=courses 


http://rpi.apis.acalog.com/v1/content?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml&method=getItems&options[full]=1&catalog=26&type=courses&ids[]=59451&ids[]=59452&ids[]=60917&ids[]=60918&ids[]=59454&ids[]=59455&ids[]=59456&ids[]=60955&ids[]=61524&ids[]=61525&ids[]=61526&ids[]=59457&ids[]=60933&ids[]=60934&ids[]=60935&ids[]=60936&ids[]=60939&ids[]=60940&ids[]=60941&ids[]=60942&ids[]=60948&ids[]=60949&ids[]=59458&ids[]=59459&ids[]=60956&ids[]=60913&ids[]=60938&ids[]=61007&ids[]=60919&ids[]=60920&ids[]=60921&ids[]=59453&ids[]=60916&ids[]=60915&ids[]=67677&ids[]=59460&ids[]=61527&ids[]=61528&ids[]=60951&ids[]=60952&ids[]=60950&ids[]=59461&ids[]=60953&ids[]=59462&ids[]=60914&ids[]=60954&ids[]=59463&ids[]=60945&ids[]=61245&ids[]=60946&ids[]=61246&ids[]=61253&ids[]=61196&ids[]=60943&ids[]=60944&ids[]=59464&ids[]=59465&ids[]=59466&ids[]=61186&ids[]=61136&ids[]=61137&ids[]=60937&ids[]=60947&ids[]=59467&ids[]=59468&ids[]=61016&ids[]=61021&ids[]=61018&ids[]=61027&ids[]=61020&ids[]=61024&ids[]=61017&ids[]=61023&ids[]=61019&ids[]=61022&ids[]=61025&ids[]=61033&ids[]=61030&ids[]=61034&ids[]=61036&ids[]=59469&ids[]=59470&ids[]=59471&ids[]=59472&ids[]=59473&ids[]=59474&ids[]=60924&ids[]=60925&ids[]=61070&ids[]=61067&ids[]=59475&ids[]=59476&ids[]=61026&ids[]=61029&ids[]=61032&ids[]=61028&ids[]=61031&ids[]=59477&ids[]=59478&ids[]=59479

url = "http://rpi.apis.acalog.com/v1/content?"
API Key: 3eef8a28f26fb2bcc514e6f1938929a1f9317628
Above link is url + key + format ="xml&method=getItems&options[full]=1*catalog="{catalog id} + "&type=courses& + ids
where each element in ids = "ids[]=crn" of course.

How the old parser works - create the acalog. Then get all of the course ids - crns for each course, converting them into 'ids[]=crn'. Then then join the ids with the base url above to get url + "&{id_chunk}" where the id chunk is a massive list of crns each up to 200 in size. After that the rest of the program crashes because the course_details xml output is null. But it seems that from that 