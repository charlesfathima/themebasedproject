# themebasedproject
final year project

DESCRIPTION:
        
        This project is about recommending tourist places to the people based upon their preferences.
        User while registering he enters the preferences (eg:beach,hillstations,etc..,),when he logs in to the site he gets the                     recommendations.
        We also managed to not recommend places which has bad description using textblob library eventhough user prefers that                   typeofplace 
        
        He can also search and upload places along with location and type of place.
        He might also change the preferences after he logs in. 
        He can get the accommodation details once he clicks on the place that is recommended for him, accommodation details are provided         in map,i.e.., hotels near by place are spotted on the map and when we move mouse over to that hotel, we get the details like             price and rating about that hotel(this can be done using google maps api, but due to api key issues we were unable to accomplish         spotting hotels on map, but we somehow managed to locate the place on map using mapbox api for directions purpose and inorder           to get coordinates for locating the place on map  we used opencage geocoder api)
        
 APPS IN PROJECT:
        
 travello:django app for recommendations
           Destinations is the class used to collect data about a place, uploaded files are stored in media file 
           views.py:
           It imports necessary libraries and api
           def changepreferences: for modifying preferences, redirects to homepage after changing preferences
           def index: home page to view popular destinations if user not logs in, if he logs in then recommendations are provided based                       upon the features -description,typeofplace,state and only if polarity(positive or negative) of description is >0.0                       we recommend that place although he is prefering that place
           def search:function to perform search operation, redirects to search.html
           def upload:function to perform upload operation, redirects to index.html(homepage)
           
           other functions are helper functions to get and set values
 accounts:django app for login/register
 
            django provides inbuilt login and registration classes, but to get preferences from user we created new class                           CustomPreferences which is linked to django's User class
            
 
 We are looking forward to make our website more userfriendly 
 
        
 
