// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';


function set_dashboard_data(result)
{
 var result_obj = JSON.parse(result);
 var labels = []
 var values = []
 console.log()
 param = window.location.pathname.split("/").pop()
 //salaire_paris_ville_titre
 var salaire_paris_ville_titre = document.getElementById("salaire_paris_ville_titre");
 if (param == "min")
 {
    salaire_paris_ville_titre.innerHTML = "Moyenne de la borne inférieure";
 }
 else if (param == "moyen")
 {
    salaire_paris_ville_titre.innerHTML = "Moyenne salariale";
 }
 else
 {
    salaire_paris_ville_titre.innerHTML = "Moyenne de la borne supérieure";
 }

 for (item in result_obj)
 {
   labels.push(item)
   values.push(result_obj[item][param])
 }
 // Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: "Salaire",
       backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc','#fd7e14'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#fdcea7'],
      borderColor: "#4e73df",
      data: values,
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'month'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: (Math.max.apply(Math,values) + 1000),
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return  number_format(value) + '€ ';
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
        }
      }
    },
  }
});

}
get_file('http://127.0.0.1:5000/dashboard/data', set_dashboard_data)
