
// Load the Visualization API and the corechart package.
        google.charts.load('current', {'packages': ['corechart']});

        // Set a callback to run when the Google Visualization API is loaded.
        google.charts.setOnLoadCallback(drawChart);

        // Callback that creates and populates a data table,
        // instantiates the pie chart, passes in the data and
        // draws it.
        function drawChart() {

            // Create the data table.
            var author_data = new google.visualization.DataTable();
            author_data.addColumn('string', 'Topping');
            author_data.addColumn('number', 'Slices');
            author_data.addRows({% autoescape off %}{{ author_data }}{% endautoescape %});

            // Set chart options
            var author_options = {
                'title': '',
                'legend': 'none',
                'width': 300,
                'height': 300
            };

            // Instantiate and draw our chart, passing in some options.
            var author_chart = new google.visualization.PieChart(document.getElementById('author_chart_div'));
            author_chart.draw(author_data, author_options);

            var subject_data = new google.visualization.DataTable();
            subject_data.addColumn('string', 'Topping');
            subject_data.addColumn('number', 'Slices');
            subject_data.addRows({% autoescape off %}{{ subject_data }}{% endautoescape %});

            // Set chart options
            var subject_options = {
                'title': '',
                'legend': 'none',
                'width': 300,
                'height': 300
            };

            // Instantiate and draw our chart, passing in some options.
            var subject_chart = new google.visualization.PieChart(document.getElementById('subject_chart_div'));
            subject_chart.draw(subject_data, subject_options);
        }