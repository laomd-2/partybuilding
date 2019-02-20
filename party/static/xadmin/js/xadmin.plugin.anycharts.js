$(document).ready(function(){
    $.fn.chart = function() {
        $(this).each(function () {
            var $chart = $(this);
            var dom = document.getElementById($chart.context.id);
            var myChart = echarts.init(dom);
            $.getJSON($chart.data('chart-url'), function (data) {
                if (data.option && typeof data.option === "object") {
                myChart.setOption(data.option, true);
                }
            });
        });
    };

    $('.chart-tab a').click(function(e){
      e.preventDefault();
      $(this).tab('show');

      $($(this).attr('href')).chart();
    });
    $('.chart-tab a:first').click();
    $('.chart.init').chart();
});
