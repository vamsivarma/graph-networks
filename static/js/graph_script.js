$(document).ready(function($) {

  var holderElem = $('#graph-search-holder');
  
  if(holderElem.length) {

    //document.getElementById("defaultOpen").click();
    graphModule.initGraphModule(holderElem);
  
  }
 
 });  
  

  var graphModule = (function() {
  
    //DOM for Search page...
    var moduleHolderElem = '';
    var overlayElem = '';

    var _this = '';
    var baseURL = "http://localhost:8080/";

    var authorsAPIFlag = false;
    var conferencesAPIFlag = false;

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
          'callBackFunc': searchByConference.bind(this),
          'columnsAry': [{'title':'Author ID'},
                        {'title':'Author Name'},
                        {'title':'Degree Centrality'},
                        {'title':'Closeness Centrality'},
                        {'title':'Betweeness Centrality'}]
    }, {
          'tabHolder': 'searchByAuthor',
          'buttonElem': 'graph_sba',
          'selectElemAry': [{
                              'selectHolder': 'authors-proximity-select',
                              'type': 'author',
                              'placeholder': 'Select an author to generate proximity graph',
                              'multiple': false
                            }],
          'callBackFunc': searchByAuthor.bind(this),
          'columnsAry': [{'title':'Author ID'},
                        {'title':'Author Name'},
                        {'title':'Distance From Selected Author'}]
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
          'callBackFunc': findGroupNumber.bind(this),
          'columnsAry': [{'title':'Author ID'},
                        {'title':'Author Name'},
                        {'title':'Group Number'}]
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

          //curSelectElem.prop("selectedIndex", -1);

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

    function sort_array_of_objs(aoob) {

      aoob.sort(function(a, b) {
        if(a.text < b.text) return -1;
        if(a.text > b.text) return 1;
        return 0;
      });

      return aoob;
    }

    function store_authors_data(response) {
        authorsAPIFlag = false;
        authors_list = response['authors_list'];
        authors_list = sort_array_of_objs(authors_list);

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

      conferences_list = sort_array_of_objs(conferences_list);

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

          document.getElementById("defaultOpen").click();
        }
    }

    function returnCurrentSelectDOM(index) {
      return graphTabDOMObj[curTabId]['selectElemAry'][index]['selectHolder']
    }

    //Start - Functions related to Centrality
    function searchByConference() {
      var curConfSelElem = returnCurrentSelectDOM(0);
      var selectedConfId = curConfSelElem.val();

      if(selectedConfId !== null) {

        //Show loader
        overlayElem.show();

        var conf_name = curConfSelElem.select2('data')[0]['text'];

        $.ajax({
          type: 'GET',
          url: baseURL + "find_centralities?conf_id=" + selectedConfId + '&conf_name=' + conf_name,
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: find_centralities_success.bind(this),
          error: find_centralities_failure.bind(this)
        });
      } else {
        alert('Please select at least one conference...');
      } 
    }

    function find_centralities_success(response) {

      //Hide loader
      overlayElem.hide();

      var conf_id = response['conf_id'];
      var conf_name = response['conf_name'];

      //Need to do the DOM Manipulation more efficiently
      moduleHolderElem.find('#centrality-title').html("<h3>Centrality results for " + conf_name + "</h3>");
      moduleHolderElem.find('#centrality-graph').html("<h3>Centrality Graph:</h3><img width='800px' height='500px' src='static/images/centrality/centrality_" + conf_id + ".png' />");

      var centralityTableElem = moduleHolderElem.find('#centrality_table');

      moduleHolderElem.find('#centrality-table-title').html("<h3>Centrality Table:</h3>");

      centralityTableElem.DataTable({
          destroy: true,
          data: response.cDataset,
          columns: graphTabDOMObj[curTabId]['columnsAry']
      });
    } 

    function find_centralities_failure(xhr, textStatus, errorThrown) {
      //Hide loader
      overlayElem.hide();
    
    }

    //End - Functions related to Centrality


    //Start - Functions related to Proximity
    function searchByAuthor() {
      
      var curAuthorSelElem = returnCurrentSelectDOM(0);
      var selectedAuthorId = curAuthorSelElem.val();

      var hop_count = moduleHolderElem.find('#graph_hc').val();

      if(selectedAuthorId !== null) {

        //Show loader
        overlayElem.show();

        var author_name = curAuthorSelElem.select2('data')[0]['text']

        $.ajax({
          type: 'GET',
          url: baseURL + "find_proximity?proximity_id=" + selectedAuthorId + "&hop_count=" + hop_count + "&proximity_name=" + author_name,
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: find_proximities_success.bind(this),
          error: find_proximities_failure.bind(this)
        });
      } else {
        alert('Please select at least one author...');
      } 
    }

    function find_proximities_success(response) {

      //Hide loader
      overlayElem.hide();

      var proximity_id = response['proximity_id'];
      var proximity_name = response['proximity_name'];

      moduleHolderElem.find('#proximity-title').html("<h3>Proximity results for " + proximity_name + "</h3>");
      //Need to do the DOM Manipulation more efficiently
      moduleHolderElem.find('#proximity-graph').html("<h3>Proximity Graph:</h3><img width='800px' height='500px' src='static/images/proximity/proximity_" + proximity_id + ".png' />");
      moduleHolderElem.find('#proximity-table-title').html("<h3>Proximity Table:</h3>");

      var proximityTableElem = moduleHolderElem.find('#proximity_table');

      var columnsAry = graphTabDOMObj[curTabId]['columnsAry'];
      columnsAry[columnsAry.length - 1]['title'] = 'Distance From ' + proximity_name;
      columnsAry[columnsAry.length - 1]['sTitle'] = 'Distance From ' + proximity_name;

      proximityTableElem.DataTable({
          destroy: true,
          data: response.pDataset,
          columns: columnsAry
      });

    } 

    function find_proximities_failure(xhr, textStatus, errorThrown) {

      //Hide loader
      overlayElem.hide();
    }
    //End - Functions related to Proximity


    //Start - Functions related to Shortest Path
    function findShortestPath() {

      var author1SelElem = returnCurrentSelectDOM(0);
      var author1Id = author1SelElem.val();

      var author2SelElem = returnCurrentSelectDOM(1);
      var author2Id = author2SelElem.val();

      if(author1Id !== null && author2Id !== null) {

        //Show loader
        overlayElem.show();

        var author1_name = author1SelElem.select2('data')[0]['text'];
        var author2_name = author2SelElem.select2('data')[0]['text'];

        $.ajax({
          type: 'GET',
          url: baseURL + "find_shortest_path?author1_id=" + author1Id + "&author2_id=" + author2Id + "&author1_name=" + author1_name + "&author2_name=" + author2_name,
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: find_shortestpath_success.bind(this),
          error: find_shortestpath_failure.bind(this)
        });
      } else {
        alert('Please select author from each drop down to calculate shortest path');
      } 
    }

    function find_shortestpath_success(response) {

      //Hide loader
      overlayElem.hide();

      var author1_name = response['author1_name'];
      var author2_name = response['author2_name'];
      var cur_sd = response['shortest_distance'];

      var curTabHolderElem = graphTabDOMObj[curTabId]['tabHolder'];

      curTabHolderElem.find('.graph-results-holder').html('<h3>Distance between ' + author1_name + ' and ' + author2_name + ' is ' + cur_sd + '</h3>');

    } 

    function find_shortestpath_failure(xhr, textStatus, errorThrown) {
      
      //Hide loader
      overlayElem.hide();

    }
    //End - Functions related to Shortest Path

    //Start - Functions related to Group Number
    function findGroupNumber() {

      var authorsSelElem = returnCurrentSelectDOM(0);
      var selectedAuthors = authorsSelElem.val();

      if( selectedAuthors.length ) {

        selectedAuthors = selectedAuthors.join(',');

        $.ajax({
          type: 'GET',
          url: baseURL + "find_author_group_numbers?authors_subset=" + selectedAuthors,
          timeout: 1000000, //@TODO: Need to revisit this
          dataType: 'json',
          success: find_groupnumber_success.bind(this),
          error: find_groupnumber_failure.bind(this)
        });
      } else {
        alert('Please select at least one author...');
      }
    }

    function find_groupnumber_success(response) {

    } 

    function find_groupnumber_failure(xhr, textStatus, errorThrown) {

    }
    //End - Functions related to Group Number

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


  