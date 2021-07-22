var pos;

var $demo;


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
  const postRequest = axios.create({
    baseURL: '/api',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
    }
    })

  function initMap() {
    const myLatlng = { lat: 40.363, lng: -75.044 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 2,
        center: myLatlng,
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map to get Lat/Lng!",
        position: myLatlng,
    });
    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
        position: mapsMouseEvent.latLng,
        });
        infoWindow.setContent(
        JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        );
        infoWindow.open(map);
   

    });
            
    function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
        }
      }
    });

    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        function (position) {
          console.log('Position has been set successfully');

          dataToSend = {
            "fbpost": $("input[name=fb-post]").is(':checked'),
            "latitude": position.coords.latitude,
            "longitude": position.coords.longitude
          };

          $.ajax({
            type: "GET",
            dataType: 'json',
            url: '/find_coords/',
            data: {'d': 'JSON.stringify(dataToSend)'},
            success: function (msg) {
              console.log('Succeeded!');            
            },
            error: function (err) {
              console.log('Error!');
            }
          });
        }, function (error) {
            console.log('Position could not be obtained.')
        }
      );
    }





      $('#username_exists_form').on('submit',function(e){
          e.preventDefault();
          var username = $(this).find('input').val();
          $.get('/exists/',
              {'username': username,  
              function(response){ $('#response_msg').text(response.msg); }
              });
      }); 


      $('#get_this').on('submit',function(e){
          e.preventDefault();
          //var username = $(this).find('input').val();
          var get_this = 'YOU GOT IT'
          $.get('/exists/',
              {'get_this': get_this,  
              'user_lat' :  user_lat},
              function(response){ $('#response_msg').text(response.msg); }
          );
      }); 

  


  }


function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    $demo.text("Geolocation is not supported by this browser.");
  }
}

function showPosition(position) {
  pos = position;
  var { latitude, longitude } = pos.coords;
  $demo.html(`Latitude: ${latitude}<br>Longitude: ${longitude}`);
  $('#btn_submit').attr("disabled", null);
}

$(document).ready(function() {
  $demo = $("#demo");
  $('#btn_submit').on('click', function() {
    var data = pos.coords;
    data.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
    $.post("/ajax/", data, function() {
      alert("Saved Data!");
    });
  });
  $(document).on('submit', '#demo', function(e){
    e.preventDefault();
    $.ajax(

     type='POST',
     url = '/ajax/',
     data = {

         lat:position.coords.latitude,
         long: position.coords.longitude,
         csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
       });
      });
});