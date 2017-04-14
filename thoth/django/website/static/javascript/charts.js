

      /*******************************************************
                            PIE CHART
      *******************************************************/
      // Load the Visualization API and the corechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawPieChart);

      // Callback that creates and populates a data table,
      // instantiates the pie chart, passes in the data and
      // draws it.

      function drawPieChart() {

        // Create the data table.
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Vote');
        data.addColumn('number', 'Number');
        data.addRows([
          ['Speed up', upVotes],
          ['Slow down', downVotes],
          ['Not voting', nonVotes],
        ]);

        // Set chart options
        var options = {'title':'Student feedback',
                       'width':300,
                       'height':200};

        // Instantiate and draw our chart, passing in some options.
        var pie_chart = new google.visualization.PieChart(document.getElementById('pie_chart_div'));
        pie_chart.draw(data, options);
      }

      /*******************************************************
                            AREA CHART
      *******************************************************/
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawAreaChart);

      function drawAreaChart() {
        var areaStyle = 'fill-color: #ffeb3b; stroke-color: #b71c1c; stroke-width: 8;';
        var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses'],
          ['2013',  1000,      400],
          ['2014',  1170,      460],
          ['2015',  660,       1120],
          ['2016',  1030,      540]
        ]);

        var options = {
          title: 'Student feedback',
          hAxis: {title: 'Year',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0}

        };

        var area_chart = new google.visualization.AreaChart(document.getElementById('area_chart_div'));
        area_chart.draw(data, options);
      }