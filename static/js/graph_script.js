
$(document).ready(function($) {

  var holderElem = $('#graph-search-holder');
  
  if(holderElem.length) {

    document.getElementById("defaultOpen").click();
    graphModule.initGraphModule(holderElem);
  
  }
 
 });  
  

  var graphModule = (function() {
  
    //DOM for Search page...
    var moduleHolderElem = '';
    var overlayElem = '';

    var _this = '';
    var baseURL = "http://localhost:8080/";

    var authorsAPIFlag = true;
    var conferencesAPIFlag = true;

    var authors_list = [];
    var conferences_list = [];

    var graphTabDOMObj = [{
          'tabHolder': 'searchByConference',
          'buttonElem': 'graph_sbc',
          'selectElemAry': [{
                              'selectHolder': 'conferences-select',
                              'type': 'conference',
                              'placeholder': 'Select a conference',
                              'multiple': false
                            }],
          'callBackFunc': searchByConference.bind(this)
    }, {
          'tabHolder': 'searchByAuthor',
          'buttonElem': 'graph_sba',
          'selectElemAry': [{
                              'selectHolder': 'authors-proximity-select',
                              'type': 'author',
                              'placeholder': 'Select an author to generate proximity graph',
                              'multiple': false
                            }],
          'callBackFunc': searchByAuthor.bind(this)

    }, {
          'tabHolder': 'findShortestPath',
          'buttonElem': 'graph_sp',
          'selectElemAry': [{
                              'selectHolder': 'authors-sp-select1',
                              'type': 'author',
                              'placeholder': 'Select 1st author to calculate shortest path',
                              'multiple': false
                            }, {
                              'selectHolder': 'authors-sp-select2',
                              'type': 'author',
                              'placeholder': 'Select 2nd author to calculate shortest path',
                              'multiple': false
                            }],
          'callBackFunc': findShortestPath.bind(this)
    }, {
          'tabHolder': 'findGroupNumber',
          'buttonElem': 'graph_gn',
          'selectElemAry': [{
                              'selectHolder': 'authors-group-select',
                              'type': 'author',
                              'placeholder': 'Select authors to calculate group number',
                              'multiple': true
                            }],
          'callBackFunc': findGroupNumber.bind(this)
    }];

    var curTabId = '';
    var curTabDOM = {};

    function initGraphModule(holderElem) {
      
      //Initializing DOM of Advanced Search module
      moduleHolderElem = holderElem;
      overlayElem = moduleHolderElem.find('#ss-overlay');
      
      _this = this;  
      
      //Show loader
      overlayElem.show();

      getAuthors();
      getConferences();
 
    }

    function initializeGraphModuleDOMAndEvents() {

      //Initialize DOM of the Graph Module elements
      graphTabDOMObj.forEach(function(tabDOMObj) {

        var tabId =  tabDOMObj['tabHolder'];
        var buttonId = tabDOMObj['buttonElem'];

        tabDOMObj['tabHolder'] = moduleHolderElem.find('#' + tabId);
        tabDOMObj['buttonElem'] = moduleHolderElem.find('#' + buttonId);

        var selectElemAry = tabDOMObj['selectElemAry'];

        selectElemAry.forEach(function(selectMeta, index) {
          var selectHolderId = selectMeta['selectHolder'];
          selectMeta['selectHolder'] = moduleHolderElem.find('#' + selectHolderId);

          var curSelectElem = selectMeta['selectHolder'];

          var curSelectData = [];

          if(selectMeta['type'] == 'author') {
            curSelectData = authors_list;
          } else {
            curSelectData = conferences_list;
          }

          //Initialize select 2
          //curSelectElem.select2('destroy').empty();
          curSelectElem.select2({ 
                                    placeholder: selectMeta['placeholder'],
                                    disabled: false, 
                                    data: curSelectData,
                                    allowClear: false,
                                    closeOnSelect: !selectMeta['multiple'],
                                    multiple: selectMeta['multiple']
                                }); 

        });

        //Register click events
        tabDOMObj['buttonElem'].off('click').on('click', tabDOMObj['callBackFunc']);

      });
    }


    function clear_previous_results() {   
      //Clear previous search results...
      moduleHolderElem.find('#results-container').html('');

      //Disable the text input until all the search results are fetched...
      //document.getElementById('graph_search').disabled = true;
      //document.getElementById('graph_search_btn').disabled = true;
      //document.getElementById('graph_wc_btn').disabled = true;

    }
    
    function getAuthors() {

      authorsAPIFlag = true;

      $.ajax({
          type: 'GET',
          url: baseURL + "get_authors",
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: store_authors_data.bind(this),
          error: handle_authors_failure.bind(this)
      });
    }

    function store_authors_data(response) {
        authorsAPIFlag = false;
        authors_list = response['authors_list'];
        hideLoader();
    }

    function handle_authors_failure(xhr, textStatus, errorThrown) {
        authorsAPIFlag = false;
        hideLoader();
    }
    
    function getConferences() {

      conferencesAPIFlag = true;
      
      $.ajax({
          type: 'GET',
          url: baseURL + "get_conferences",
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: store_conferences_data.bind(this),
          error: handle_conferences_failure.bind(this)
      });    
    
    }

    function store_conferences_data(response) {
      conferencesAPIFlag = false;

      conferences_list = response['conferences_list'];

      hideLoader();
    }

    function handle_conferences_failure(xhr, textStatus, errorThrown) {
      conferencesAPIFlag = false;
      hideLoader();
    }

    function hideLoader() {
        if( !conferencesAPIFlag && !authorsAPIFlag ) {
          overlayElem.hide();

          initializeGraphModuleDOMAndEvents();
        }
    }

    function searchByConference() {
      alert('Search by conference call back function got called');
    }


    function searchByAuthor() {
      alert('Search by author call back function got called');
    }

    function findShortestPath() {
      alert('Find shortest path call back function got called');
    }

    function findGroupNumber() {
      alert('Find group number call back function got called');
    }

    function openGraphTab(evt, tabName, tabId) {

      if(tabId !== curTabId) {

        curTabId = tabId;

        // Declare all variables
        var i, tabcontent, tablinks;

        // Get all elements with class="tabcontent" and hide them
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        // Get all elements with class="tablinks" and remove the class "active"
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        // Show the current tab, and add an "active" class to the button that opened the tab
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";

      }
      
      
    
    } 

    return {
      'initGraphModule': initGraphModule,
      'openGraphTab': openGraphTab
    }

  })();


  