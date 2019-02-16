import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView


class HelloWorldPlugin(BaseAdminPlugin):
    datas = [[], []]

    # 初始化方法根据 ``say_hello`` 属性值返回
    def init_request(self, *args, **kwargs):
        return bool(self.datas[0])

    # context 即为 TemplateContext， nodes 参数包含了其他插件的返回内容。
    # 您可以直接返回 HTML 片段，或是将内容加入到 nodes 参数中
    def block_results_top(self, context, nodes):
        return '''<div id="container2" style="height: 100%"></div>
        <script type="text/javascript">
    var dom = document.getElementById("container2");
    if (dom != null) {
        var myChart = echarts.init(dom);
        var app = {};
        option = null;
        app.title = '极坐标系下的堆叠柱状图';

        option = {
            angleAxis: {},
            radiusAxis: {
                type: 'category',
                data: ['周一', '周二', '周三', '周四'],
                z: 10
            },
            polar: {},
            series: [{
                type: 'bar',
                data: [1, 2, 3, 4],
                coordinateSystem: 'polar',
                name: 'A',
                stack: 'a'
            }, {
                type: 'bar',
                data: [2, 4, 6, 8],
                coordinateSystem: 'polar',
                name: 'B',
                stack: 'a'
            }, {
                type: 'bar',
                data: [1, 2, 3, 4],
                coordinateSystem: 'polar',
                name: 'C',
                stack: 'a'
            }],
            legend: {
                show: true,
                data: ['A', 'B', 'C']
            }
        };
        ;
        if (option && typeof option === "object") {
            myChart.setOption(option, true);
        }
    }
   </script>
'''


xadmin.site.register_plugin(HelloWorldPlugin, ListAdminView)
