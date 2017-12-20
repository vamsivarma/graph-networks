var dataSet = [
    [ "Tiger Nixon", "System Architect", "Edinburgh", "5421", "2011/04/25", "$320,800" ],
    [ "Garrett Winters", "Accountant", "Tokyo", "8422", "2011/07/25", "$170,750" ],
    [ "Ashton Cox", "Junior Technical Author", "San Francisco", "1562", "2009/01/12", "$86,000" ],
    [ "Cedric Kelly", "Senior Javascript Developer", "Edinburgh", "6224", "2012/03/29", "$433,060" ],
    [ "Airi Satou", "Accountant", "Tokyo", "5407", "2008/11/28", "$162,700" ],
    [ "Brielle Williamson", "Integration Specialist", "New York", "4804", "2012/12/02", "$372,000" ],
    [ "Herrod Chandler", "Sales Assistant", "San Francisco", "9608", "2012/08/06", "$137,500" ],
    [ "Rhona Davidson", "Integration Specialist", "Tokyo", "6200", "2010/10/14", "$327,900" ],
    [ "Colleen Hurst", "Javascript Developer", "San Francisco", "2360", "2009/09/15", "$205,500" ],
    [ "Sonya Frost", "Software Engineer", "Edinburgh", "1667", "2008/12/13", "$103,600" ],
    [ "Jena Gaines", "Office Manager", "London", "3814", "2008/12/19", "$90,560" ],
    [ "Quinn Flynn", "Support Lead", "Edinburgh", "9497", "2013/03/03", "$342,000" ],
    [ "Charde Marshall", "Regional Director", "San Francisco", "6741", "2008/10/16", "$470,600" ],
    [ "Haley Kennedy", "Senior Marketing Designer", "London", "3597", "2012/12/18", "$313,500" ],
    [ "Tatyana Fitzpatrick", "Regional Director", "London", "1965", "2010/03/17", "$385,750" ],
    [ "Michael Silva", "Marketing Designer", "London", "1581", "2012/11/27", "$198,500" ],
    [ "Paul Byrd", "Chief Financial Officer (CFO)", "New York", "3059", "2010/06/09", "$725,000" ],
    [ "Gloria Little", "Systems Administrator", "New York", "1721", "2009/04/10", "$237,500" ],
    [ "Bradley Greer", "Software Engineer", "London", "2558", "2012/10/13", "$132,000" ],
    [ "Dai Rios", "Personnel Lead", "Edinburgh", "2290", "2012/09/26", "$217,500" ],
    [ "Jenette Caldwell", "Development Lead", "New York", "1937", "2011/09/03", "$345,000" ],
    [ "Yuri Berry", "Chief Marketing Officer (CMO)", "New York", "6154", "2009/06/25", "$675,000" ],
    [ "Caesar Vance", "Pre-Sales Support", "New York", "8330", "2011/12/12", "$106,450" ],
    [ "Doris Wilder", "Sales Assistant", "Sidney", "3023", "2010/09/20", "$85,600" ],
    [ "Angelica Ramos", "Chief Executive Officer (CEO)", "London", "5797", "2009/10/09", "$1,200,000" ],
    [ "Gavin Joyce", "Developer", "Edinburgh", "8822", "2010/12/22", "$92,575" ],
    [ "Jennifer Chang", "Regional Director", "Singapore", "9239", "2010/11/14", "$357,650" ],
    [ "Brenden Wagner", "Software Engineer", "San Francisco", "1314", "2011/06/07", "$206,850" ],
    [ "Fiona Green", "Chief Operating Officer (COO)", "San Francisco", "2947", "2010/03/11", "$850,000" ],
    [ "Shou Itou", "Regional Marketing", "Tokyo", "8899", "2011/08/14", "$163,000" ],
    [ "Michelle House", "Integration Specialist", "Sidney", "2769", "2011/06/02", "$95,400" ],
    [ "Suki Burks", "Developer", "London", "6832", "2009/10/22", "$114,500" ],
    [ "Prescott Bartlett", "Technical Author", "London", "3606", "2011/05/07", "$145,000" ],
    [ "Gavin Cortez", "Team Leader", "San Francisco", "2860", "2008/10/26", "$235,500" ],
    [ "Martena Mccray", "Post-Sales support", "Edinburgh", "8240", "2011/03/09", "$324,050" ],
    [ "Unity Butler", "Marketing Designer", "San Francisco", "5384", "2009/12/09", "$85,675" ]
];


$(document).ready(function($) {

  var holderElem = $('#graph-search-holder');
  
  if(holderElem.length) {

    //document.getElementById("defaultOpen").click();
    graphModule.initGraphModule(holderElem);

    columnsAry = [
            { title: "Name" },
            { title: "Position" },
            { title: "Office" },
            { title: "Extn." },
            { title: "Start date" },
            { title: "Salary" }
        ]

    $('#example').DataTable({
        data: dataSet,
        columns: columnsAry
    });

    $('#example_group').DataTable({
        data: dataSet,
        columns: columnsAry
    });
  
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

        $.ajax({
          type: 'GET',
          url: baseURL + "find_centralities?conf_id=" + selectedConfId,
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

    } 

    function find_centralities_failure(xhr, textStatus, errorThrown) {

    }
    //End - Functions related to Centrality


    //Start - Functions related to Proximity
    function searchByAuthor() {
      
      var curAuthorSelElem = returnCurrentSelectDOM(0);
      var selectedAuthorId = curAuthorSelElem.val();

      if(selectedAuthorId !== null) {

        $.ajax({
          type: 'GET',
          url: baseURL + "find_proximity?author_id=" + selectedAuthorId,
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

    } 

    function find_proximities_failure(xhr, textStatus, errorThrown) {

    }
    //End - Functions related to Proximity


    //Start - Functions related to Shortest Path
    function findShortestPath() {

      var author1SelElem = returnCurrentSelectDOM(0);
      var author1Id = author1SelElem.val();

      var author2SelElem = returnCurrentSelectDOM(1);
      var author2Id = author2SelElem.val();

      if(author1Id !== null && author2Id !== null) {

        $.ajax({
          type: 'GET',
          url: baseURL + "find_shortest_path?author1_id=" + author1Id + "&author2_id=" + author2Id,
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

    } 

    function find_shortestpath_failure(xhr, textStatus, errorThrown) {

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


  