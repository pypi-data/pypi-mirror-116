from CKClient import get_client
from graph_op import CHGraph as ch
import Longger_design

class ModelService(object):
    # 切换图空间
    def use_graph(self, graph_name, db):
        res = db.use_tables(graph_name)
        print(res)
        if res is None:
            return
        else:
            self.graph_name = graph_name
            self.graph_cfg = res

    # 根据条件过滤查询子图
    def search_subgraph_by_condition(self, data,
                                     config_param):
        if "subGraph" in data.keys():
            graph_name = data["subGraph"]
        else:
            return None
        # if "fieldList" in data.keys():
        #     fieldList = data["fieldList"]
        #     fields = ",".join(fieldList)
        #
        edge_types = None
        if "edgeTypes" in data.keys():
            edge_types = data["edgeTypes"]

        node_types = None
        if "nodeTypes" in data.keys():
            node_types = data["nodeTypes"]

        db = config_param["db"]
        # graph_client = config_param["graphClient"]
        clickhouse_connect = config_param["clickhouse_connect"]
        graph_client = get_client(clickhouse_connect)
        graph = CHGraph(graph_client)
        self.use_graph(graph_name, db)
        ######
        edges = self.graph_cfg["edges"]
        vertexes = self.graph_cfg["vertexes"]

        if "edgeConditions" in data.keys():
            edge_conditions = data["edgeConditions"]
            edge_condition_dict, edge_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                edge_conditions, edges)
        else:
            edge_condition_dict, edge_order_dict = {}, {}
        if "nodeConditions" in data.keys():
            node_conditions = data["nodeConditions"]
            node_condition_dict, node_order_dict, special_sql_dict = ConditionOperation().conditionalOperation(
                node_conditions, vertexes)
        else:
            node_condition_dict, node_order_dict = {}, {}

        if "fieldList" in data.keys():
            ext_field_list = data["fieldList"]
        else:
            ext_field_list = None
        if "resultType" in data.keys():
            result_type = data["resultType"]
        else:
            result_type = None
        data = {}
        path_data = {}
        edge_data_list = []
        vertexes_data_list = []

        if edge_types:
            edge_data_list = executeController(edge_types, edges, edge_condition_dict, edge_order_dict, graph, "edge",
                                               ext_field_list, result_type)
        else:
            # edge_data_list = executeController(edges, edges, edge_condition_dict, edge_order_dict, graph, "edge")
            pass
        if node_types:
            vertexes_data_list = executeController(node_types, vertexes, node_condition_dict, node_order_dict, graph,
                                                   "vertexes", ext_field_list, result_type)
        else:
            # vertexes_data_list = executeController(vertexes, vertexes, node_condition_dict, node_order_dict, graph,
            #                                      "vertexes")
            pass

        path_data["graphEdges"] = edge_data_list
        path_data["graphNodes"] = vertexes_data_list
        data["pathList"] = path_data
        # 释放链接
        disconnect_client(graph_client)
        return data