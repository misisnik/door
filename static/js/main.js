// variables
_ACTUAL_SELECTION = 0
// init vue
app = new Vue({
  delimiters: ['${', '}'],
  el: '#web-box',
  data: {
    door_state: 'unknown',
    data: [],
    loading: false,
  },
  methods: {
    request: function(path, type='get', data = null, others = null) {
      url = path_to_url('/_api/' + path);
      if(type == 'get')
      {
        this.$http.get(url).then((result) => {
            if(path == 'door-state'){
              app.door_state = result.body['status'];
              app.data = result.body['data'];
            }else if(path == 'neco_dalsiho'){
              pass
            }
          }, err => {
              // handle error
          })
      }else{
        // post
        this.$http.post(url, data).then((result) => {
            app.loading = false;
            if(path == 'door-state'){
              // return na door action je jeslti se to povedlo nebo nepovedlo
              console.log(result.body['status']);
              app.door_state = result.body['status'];
              app.data = result.body['data'];
            }
          }, err => {
              // handle error
          })
      }
    }
  }
})

path_to_url = function(path) {
  return window.location.protocol + '//' + window.location.host + path;
};

function initDoor(){
  //load zeros
  app.request('door-state');
}

function doorAction(){
  app.loading = true;
  app.request('door-state', 'post', {'status':!app.door_state});
}

// workflow
initDoor()
// websocket
connectWebSocket = function() {
  recInterval = null;
  window.sock = null;
  new_conn = function() {
    sock = window.sock = new SockJS('/sockjs', null, {
      protocols_transports: ['websocket', 'xdr-streaming', 'xhr-streaming', 'iframe-eventsource', 'iframe-htmlfile', 'xdr-polling', 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling']
    });
    clearInterval(recInterval);
    sock.onopen = function() {

    };
    sock.onclose = function() {

      sock = window.sock = null;
    };
    return sock.onmessage = function(msg) {
      data = JSON.parse(msg.data);
      console.log(data);
      if(data.action=='door-action'){
        // change door state
        console.log(data.status);
        app.loading = false;
        app.door_state = data.status;
        return;
      }else if (data.action='loading'){
        console.log('menime status na neco co nikdo nickdy nepoznal');
        console.log(data.status);
        app.loading = data.status;
        // app.data = data.data;
      }

    };
  };
  // load websocket
  return new_conn();
};

connectWebSocket();
