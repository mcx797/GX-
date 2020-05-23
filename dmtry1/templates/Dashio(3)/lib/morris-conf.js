var Script = function () {

    //morris chart

    $(function () {
      // data stolen from http://howmanyleft.co.uk/vehicle/jaguar_'e'_type
      var tax_data = [
           {"period": "2011 Q3", "licensed": 3407, "sorned": 660},
           {"period": "2011 Q2", "licensed": 3351, "sorned": 629},
           {"period": "2011 Q1", "licensed": 3269, "sorned": 618},
           {"period": "2010 Q4", "licensed": 3246, "sorned": 661},
           {"period": "2009 Q4", "licensed": 3171, "sorned": 676},
           {"period": "2008 Q4", "licensed": 3155, "sorned": 681},
           {"period": "2007 Q4", "licensed": 3226, "sorned": 620},
           {"period": "2006 Q4", "licensed": 3245, "sorned": null},
           {"period": "2005 Q4", "licensed": 3289, "sorned": null}
      ];
      Morris.Line({
        element: 'hero-graph',
        data: tax_data,
        xkey: 'period',
        ykeys: ['licensed', 'sorned'],
        labels: ['Licensed', 'Off the road'],
        lineColors:['#4ECDC4','#ed5565']
      });

      Morris.Donut({
        element: 'hero-donut',
        data: [
          {label: 'JamJ', value: 25 },
          {label: 'Frosted', value: 40 },
          {label: 'Custard', value: 25 },
          {label: 'Sugar', value: 10 }
        ],
          colors: ['#3498db', '#2980b9', '#34495e'],
        formatter: function (y) { return y + "%" }
      });

      Morris.Area({
        element: 'hero-area',
        data: [
          {period: '2020-01', all: 2655, scholar: null, student: 2647},
          {period: '2020-02', all: 2778, scholar: 2294, student: 2441},
          {period: '2020-03', all: 4912, scholar: 1969, student: 2501},
          {period: '2020-04', all: 3767, scholar: 3597, student: 5689},
          {period: '2020-05', all: 6810, scholar: 1914, student: 2293},
          {period: '2020-06', all: 5670, scholar: 4293, student: 1881},
          {period: '2020-07', all: 4820, scholar: 3795, student: 1588},
          {period: '2020-08', all: 15073, scholar: 5967, student: 5175},
          {period: '2020-09', all: 10687, scholar: 4460, student: 2028},
          {period: '2020-10', all: 8432, scholar: 5713, student: 1791},
          {period: '2020-11', all: 8432, scholar: 5713, student: 1791},
          {period: '2020-12', all: 8432, scholar: 5713, student: 1791}
        ],

          xkey: 'period',
          ykeys: ['all', 'scholar', 'student'],
          labels: ['all', 'scholar', 'student'],
          hideHover: 'auto',
          lineWidth: 1,
          pointSize: 5,
          lineColors: ['#4a8bc2', '#ff6c60', '#a9d86e'],
          fillOpacity: 0.5,
          smooth: true
      });

      Morris.Bar({
        element: 'hero-bar',
        data: [
          {device: 'iPhone', geekbench: 136},
          {device: 'iPhone 3G', geekbench: 137},
          {device: 'iPhone 3GS', geekbench: 275},
          {device: 'iPhone 4', geekbench: 380},
          {device: 'iPhone 4S', geekbench: 655},
          {device: 'iPhone 5', geekbench: 1571}
        ],
        xkey: 'device',
        ykeys: ['geekbench'],
        labels: ['Geekbench'],
        barRatio: 0.4,
        xLabelAngle: 35,
        hideHover: 'auto',
        barColors: ['#ac92ec']
      });

      new Morris.Line({
        element: 'examplefirst',
        xkey: 'year',
        ykeys: ['value'],
        labels: ['Value'],
        data: [
          {year: '2008', value: 20},
          {year: '2009', value: 10},
          {year: '2010', value: 5},
          {year: '2011', value: 5},
          {year: '2012', value: 20}
        ]
      });

      $('.code-example').each(function (index, el) {
        eval($(el).text());
      });
    });

}();




