# -*- codeing = utf-8 -*-
# @Time :2023/2/23 17:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :https://zhuanlan.zhihu.com/p/546002046
# @Link :https://blog.csdn.net/qq_39805362/article/details/122233420
# @Link :https://blog.csdn.net/weixin_41512727/article/details/80583157
# @Link :https://blog.csdn.net/qq_40206371/article/details/120407459
# @Link :https://zhuanlan.zhihu.com/p/488015442
# @Link :https://blog.csdn.net/weixin_41194129/article/details/111308381

# @File :  OSMnx使用教程.py

import osmnx as ox


# from pint.testsuite.test_matplotlib import plt
# ox.config(request_kwargs={})

# OSMnx，简称ox。其中主要分为两种地图模型，一种是区块数据（gdf_from_place）,另外一种是道路模型（graph_from_place）。

def shortest_path_length():
    # 获取最短路径距离
    G = ox.graph_from_address("广州大学", network_type='all')  # 第一步，获取道路数据
    ox.plot_graph(G)
    origin_point = (23.039506, 113.364664)  # 广州大学校门坐标
    destination_point = (23.074058, 113.386148)  # 中山大学校门坐标
    origin_node = ox.get_nearest_node(G, origin_point)  # 获取O最邻近的道路节点
    destination_node = ox.get_nearest_node(G, destination_point)  # 获取D最邻近的道路节点
    route = ox.shortest_path(G, origin_node, destination_node, weight='length')  # 请求获取最短路径
    distance = ox.shortest_path_length(G, origin_node, destination_node, weight='length')  # 并获取路径长度
    fig, ax = ox.plot_graph_route(G, route, origin_point=origin_point, destination_point=destination_point)  # 可视化结果
    print(str(distance))  # 输出最短路径距离


# 一行代码完成下载和建模可步行、可驾驶或可骑自行车的城市网络
def graph_from_place():
    G = ox.graph_from_place('Modena, Italy')
    # 以openstreetmap底图为背景绘图
    G_84 = ox.project_graph(G, to_crs='EPSG:4326')
    ox.plot_graph_folium(G_84, tiles='openstreetmap', kwargs={'width': 0.1})
    # ox.plot_graph(G)


# 自动下载行政地点边界和 shapefile
def geocode_to_gdf():
    city = ox.geocode_to_gdf('Chencang, Baoji, Shaanxi, China')
    ax = ox.project_gdf(city).plot()
    _ = ax.axis('off')


# 下载和建模街道网络(通过包围盒）
def graph_from_bbox():
    G = ox.graph_from_bbox(30.255904285611525, 30.141649815003344, 120.2972282472983, 120.2239798312058,
                           network_type='drive')
    # 形成路网图 https://blog.csdn.net/qq_39805362/article/details/122233420
    G = ox.project_graph(G, to_crs='EPSG:4326')
    ox.plot_graph_folium(G, tiles='openstreetmap', kwargs={'width': 0.1})

    # ox.plot_graph(G)

    # plt.rcParams['figure.dpi'] = 400
    # fig = plt.figure(figsize=(10, 6))  # 设置画布大小
    # ax = plt.gca()
    # ox.plot_graph(G, ax=ax, figsize=(8 * 4), bgcolor='white', node_color='blue', edge_color='grey', show=True,
    #               edge_linewidth=0.3, node_size=5, node_alpha=0.5)


# 获得距离经纬度点 0.75 公里（沿网络）内的街道网络（通过原点）
def graph_from_point():
    """
    center_point (tuple) – 构建 graph 的中心点
    dist (int) – 仅保留距离图中心 dist 米的节点（ 当 dist_type 的值为 'bbox' 时 ）
    """
    G = ox.graph_from_point(
        ox.geocoder.geocode('天下汇（高新店）, 宝鸡'),
        dist=750,
        network_type='all'
    )
    ox.plot_graph(G)

    # 将同一个交叉口的所有nodes合并 原文链接：https://blog.csdn.net/qq_39805362/article/details/122233420
    # G = ox.consolidate_intersections(G, tolerance=25, rebuild_graph=True, dead_ends=False,
    #                                  reconnect_edges=True)


# 爬取萧山的路网拓扑结果并形成networkx的数据结构

# osmnx.graph_from_***很费时间，下载下来的graph如果需要重复试图用应该存在本地，存成一个.osm file。下次直接graph_from_xml。例子：
def save_graph_xml():
    G = ox.graph_from_bbox(30.531952, 30.140702, -81.475139, -81.817727, network_type='drive')
    ox.save_graph_xml(G, 'test.osm')

    ox.save_graph_shapefile(G, filepath='test.shp')

    G = ox.graph_from_xml('test.osm')


xml = ox.graph_from_xml(r"E:\WorkSpace\pyWorkSpace\osmnx-examples\notebooks\input_data\West-Oakland.osm")
ox.plot_graph(xml)
# toDo 下面有问题未解决
# 将同一个交叉口的所有nodes合并
G = ox.consolidate_intersections(xml, tolerance=25, rebuild_graph=False, dead_ends=False)
# 原文链接：https://blog.csdn.net/qq_39805362/article/details/122233420
ox.plot_graph(G)

# shortest_path_length()
