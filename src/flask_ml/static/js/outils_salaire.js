//import {get_file, number_format} from 'utilities.js';
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function set_outils_data_generic(result, title_id, chart_id,tools_count_id)
{
 var result_obj = JSON.parse(result);
 var labels = []
 var values = []
 param = window.location.pathname.split("/").pop()

 var langage_de_prog_titre = document.getElementById(title_id);
 if (param == "toutes")
 {
    langage_de_prog_titre.innerHTML = "Salaire - Toute la France";
 }
 else
 {
    langage_de_prog_titre.innerHTML = "Salaire - " + param;
 }

 count = 0
 for (item in result_obj)
 {
    var key =  "_" + param
    if  (item.indexOf(key) != -1)
    {
        labels.push(item.replace(key,""))
        values.push(result_obj[item])
        count = count + 1
    }
 }

 var tools_count = document.getElementById(tools_count_id);
 tools_count.innerHTML = count

 // Bar Chart Example
var ctx = document.getElementById(chart_id);
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: "Salaire",
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc','#fd7e14','#6610f2','#1cc88a','#e74a3b','#5a5c69','#0f6848','#4e73df', '#1cc88a', '#36b9cc','#fd7e14','#6610f2','#1cc88a','#e74a3b','#5a5c69','#0f6848'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#fdcea7','#9967ea','#7ec5ac','#e0928a','#88898e','#1eb57f','#2e59d9', '#17a673', '#2c9faf','#fdcea7','#9967ea','#7ec5ac','#e0928a','#88898e','#1eb57f'],
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
          maxTicksLimit: 20
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

function set_outils_popularite_generic(result, title_id, chart_id)
{
  var result_obj = JSON.parse(result);
 var labels = []
 var values = []
 param = window.location.pathname.split("/").pop()

var langage_de_prog_titre = document.getElementById(title_id);
 if (param == "toutes")
 {
    langage_de_prog_titre.innerHTML = "Popularité - Toute la France";
 }
 else
 {
    langage_de_prog_titre.innerHTML = "Popularité - " + param;
 }


 for (item in result_obj)
 {
    var key =  "_" + param
    if  (item.indexOf(key) != -1)
    {
        labels.push(item.replace(key,""))
        values.push(result_obj[item])
    }
 }

 var ctx = document.getElementById(chart_id);
var myPieChart = new Chart(ctx, {
  type: 'pie',
  data: {
    labels: labels,
    datasets: [{
      data: values,
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc','#fd7e14','#6610f2','#1cc88a','#e74a3b','#5a5c69','#0f6848','#4e73df', '#1cc88a', '#36b9cc','#fd7e14','#6610f2','#1cc88a','#e74a3b','#5a5c69','#0f6848'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf','#fdcea7','#9967ea','#7ec5ac','#e0928a','#88898e','#1eb57f','#2e59d9', '#17a673', '#2c9faf','#fdcea7','#9967ea','#7ec5ac','#e0928a','#88898e','#1eb57f'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 5,
      yPadding: 5,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 50,
  },
});


}

//db part
function set_outils_data_db(result){
  set_outils_data_generic(result, "outils_salaire_db_titre","outils_salaire_db_BarChart","tools_db_count")
}
function set_outils_popularite_db(result){
   set_outils_popularite_generic(result,"outils_popularite_titre", "outils_popularite_titre_PieChart")
}
get_file('http://127.0.0.1:5000/salaire_outils/db/data', set_outils_data_db)

get_file('http://127.0.0.1:5000/salaire_outils/db/popularity', set_outils_popularite_db)

//ci_cd
function set_outils_data_ci_cd(result){
  set_outils_data_generic(result, "outils_salaire_ci_cd_titre","outils_salaire_ci_cd_BarChart", "outils_ci_cd_id")
}
function set_outils_popularite_ci_cd(result){
   set_outils_popularite_generic(result,"outils_ci_cd_popularite_titre","outils_ci_cd_PieChart")
}
get_file('http://127.0.0.1:5000/salaire_outils/ci_cd/data', set_outils_data_ci_cd)

get_file('http://127.0.0.1:5000/salaire_outils/ci_cd/popularity', set_outils_popularite_ci_cd)


//collab
function set_outils_data_collab(result){
  set_outils_data_generic(result, "outils_salaire_collab_titre", "outils_salaire_collab_BarChart","outils_collab_id")
}
function set_outils_popularite_collab(result){
   set_outils_popularite_generic(result,"outils_collab_popularite_titre","outils_collab_PieChart")
}
get_file('http://127.0.0.1:5000/salaire_outils/collab/data', set_outils_data_collab)

get_file('http://127.0.0.1:5000/salaire_outils/collab/popularity', set_outils_popularite_collab)


//version_control
function set_outils_data_version_control(result){
  set_outils_data_generic(result, "outils_salaire_version_control_titre", "outils_salaire_BarChart", "outils_version_control_id")
}
function set_outils_popularite_version_control(result){
   set_outils_popularite_generic(result,"outils_version_control_popularite_titre", "outils_version_control_chartpie")
}
get_file('http://127.0.0.1:5000/salaire_outils/version_control/data', set_outils_data_version_control)

get_file('http://127.0.0.1:5000/salaire_outils/version_control/popularity', set_outils_popularite_version_control)


//test
function set_outils_data_test(result){
  set_outils_data_generic(result, "outils_salaire_test_titre", "outils_test_BarChart","outils_test_id")
}
function set_outils_popularite_test(result){
   set_outils_popularite_generic(result,"outils_test_popularite_titre", "outils_test_chartpie")
}
get_file('http://127.0.0.1:5000/salaire_outils/test/data', set_outils_data_test)

get_file('http://127.0.0.1:5000/salaire_outils/test/popularity', set_outils_popularite_test)

//bi_log
function set_outils_data_bi_log(result){
  set_outils_data_generic(result, "outils_salaire_bi_log_titre", "outils_bi_log_BarChart","outils_bi_log_id")
}
function set_outils_popularite_bi_log(result){
   set_outils_popularite_generic(result,"outils_bi_log_popularite", "outils_bi_log_chartpie")
}
get_file('http://127.0.0.1:5000/salaire_outils/bi_log/data', set_outils_data_bi_log)

get_file('http://127.0.0.1:5000/salaire_outils/bi_log/popularity', set_outils_popularite_bi_log)

//cloud
function set_outils_data_cloud(result){
  set_outils_data_generic(result, "outils_salaire_cloud_titre","outils_cloud_BarChart","outils_cloud_id")
}
function set_outils_popularite_cloud(result){
   set_outils_popularite_generic(result,"outils_cloud_popularite_titre", "outils_cloud_chartpie")
}
get_file('http://127.0.0.1:5000/salaire_outils/cloud/data', set_outils_data_cloud)

get_file('http://127.0.0.1:5000/salaire_outils/cloud/popularity', set_outils_popularite_cloud)