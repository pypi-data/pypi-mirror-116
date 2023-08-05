from typing import Callable, Optional, Union
import json
from .struct import *
from ._tools import *
from ._decorator import *
from ._collections import *

class ChainManager:

    def __init__(self, xml_data: str, *args, **kwargs) -> None:

        self.attr_prefix = kwargs['attr_prefix'] if 'attr_prefix' in kwargs else ATTR_PREFIX
        self.cdata_key = kwargs['cdata_key'] if 'cdata_key' in kwargs else CDATA_KEY
        self.real_cdata_key = kwargs['real_cdata_key'] if 'real_cdata_key' in kwargs else REAL_CDATA_KEY
        ChainDict.cdata_key = self.real_cdata_key
        
        self.objects = ChainXML(
            xmltodict.parse(xml_data, attr_prefix=self.attr_prefix, cdata_key=self.cdata_key)
            , attr_prefix = self.attr_prefix
            , cdata_key = self.cdata_key
            , real_cdata_key = self.real_cdata_key
        )

        self.xml = self.objects.xml

        self._attr_searcher = self.objects._attr_searcher
        self._reverse_attr_name = self.objects._reverse_attr_name
        self._id_nodes = self.objects._id_nodes
        self._id_tags = self.objects._id_tags
        self._tag_ids = self.objects._tag_ids
        self._text_ids = self.objects._text_ids
        self._contrast_ids = self.objects._contrast_ids

        self.get_tag = self.objects.get_tag
        self.get_parent = self.objects.get_parent
        self.get_children = self.objects.get_children
        self.get_siblings = self.objects.get_siblings
        self.get_descendants = self.objects.get_descendants

        self.exists = self.objects.exists
        self.is_parent_exist = self.objects.is_parent_exist

    @limit_one
    def find_nodes_by_attrs(self, one_=False, **kwargs) -> Union[List[ChainDict], ChainDict]:

        if len(kwargs) < 1:
            raise KeywordAttrsError('Keyword parameters must be passed in.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in list(self._attr_searcher.keys()):
            if sk in conditions:
                match_cons.append(sk)

        if len(match_cons) != len(conditions):
            return []

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            return []
        elif 1 == len_match_cons:
            obj = self._attr_searcher[match_cons[0]]
            if obj['count'] > 1:
                return [self._id_nodes[_t] for _t in obj['nodes']]
            else:
                return [self._id_nodes[obj['nodes'][0]], ]
        else:
            objs = find_intersection([self._attr_searcher[t]['nodes'] for t in match_cons])
            if 0 == len(objs):
                return []
            elif 1 == len(objs):
                return [self._id_nodes[objs[0]], ]
            else:
                return [self._id_nodes[_t] for _t in objs]

    def find_node_by_attrs(self, **kwargs) -> ChainDict:
        return self.find_nodes_by_attrs(one_=True, **kwargs)

    @limit_one
    def find_nodes_by_indexs(self, indexs: List[int], one_=False, **kwargs) -> Union[List[ChainDict], ChainDict]:
        nodes = self.find_nodes_by_attrs(**kwargs)
        len_nodes = len(nodes)
        return_nodes = []
        for index in indexs:
            if 0 <= index < len_nodes:
                return_nodes.append(nodes[index])
        return return_nodes

    @limit_one
    def find_nodes_by_tag(self, tag: str, one_=False) -> Union[List[ChainDict], ChainDict]:
        nodes = []
        if tag in self._tag_ids:
            for _1 in [self._id_nodes[_id] for _id in self._tag_ids[tag]]:
                if isinstance(_1, ChainDict):
                    nodes.append(_1)
                elif isinstance(_1, list):
                    ...
        return nodes
    
    @limit_one
    def find_nodes_by_tag_and_attrs(self, tag_: str=None, one_=False, **kwargs) -> Union[List[ChainDict], ChainDict]:

        if tag_ is not None and tag_ not in self._tag_ids:
            return []

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in list(self._attr_searcher.keys()):
            if sk in conditions:
                match_cons.append(sk)

        if len(match_cons) != len(conditions):
            if 0 != len(conditions):
                return []
                
        len_match_cons = len(match_cons)
        if 0 == len_match_cons and 0 != len(conditions):
            return []
        else:
            if tag_ is not None:
                tag_ids = [id(_1) for _1 in self.find_nodes_by_tag(tag_)]
                objs = find_intersection([tag_ids] + [self._attr_searcher[t]['nodes'] for t in match_cons])
            else:
                objs = find_intersection([self._attr_searcher[t]['nodes'] for t in match_cons])

            if 0 == len(objs):
                return []
            elif 1 == len(objs):
                return [self._id_nodes[objs[0]], ]
            else:
                return [self._id_nodes[_t] for _t in objs]

    @limit_one
    def find_nodes_by_tag_text_attrs(self, tag_: str=None, text_: str=None, one_=False, **kwargs) -> Union[List[ChainDict], ChainDict]:
        tag_ids = None
        text_ids = None
        attr_ids = None

        if tag_ is not None:
            tag_ids = [id(_1) for _1 in self.find_nodes_by_tag(tag_)]
        if text_ is not None:
            text_ids = [id(_1) for _1 in self.find_nodes_by_text(text_)]
        if len(kwargs) > 0:
            attr_ids = [id(_1) for _1 in self.find_nodes_by_attrs(**kwargs)]

        node_ids = find_intersection([_1 for _1 in (tag_ids, text_ids, attr_ids) if _1 is not None])
        return [self._id_nodes[node_id] for node_id in node_ids]

    @limit_one
    def find_nodes_by_text(self, text: str, one_=True) -> Union[List[ChainDict], ChainDict]:
        if text in self._text_ids:
            return [self._id_nodes[_1] for _1 in self._text_ids[text]]
        return []

    def find_text(self, node: ChainDict, format_func: Callable=lambda x:x) -> Any:

        if not isinstance(node, ChainDict):
            raise TextNotFound('Text not found.')
        
        if self.real_cdata_key in node:
            return format_func(node[self.real_cdata_key])
        elif isinstance(node, str):
            return format_func(node)
        else:
            raise TextNotFound('Text not found.')

    def find_text_by_attrs(self, *args, text_type: int=TextType.STR, format_func: Callable=lambda x:x, **kwargs) -> str:
        node = self.find_nodes_by_attrs(*args, one_=True, **kwargs)
        text = self.find_text(node, format_func)
        if TextType.STR == text_type:
            return str(text)
        elif TextType.FLOAT == text_type:
            return float(text)
        elif TextType.INT == text_type:
            return int(text)
        else:
            return text

    def __find_constraint_node(self
            , unique_node: Optional[ChainDict] = None
            , find_func: Optional[Callable] = None
            , constraint: Optional[Dict[str, Any]] = None
        ) -> int:
        
        unique_node_id = None
        if unique_node is not None:
            if isinstance(unique_node, ChainDict):
                unique_node_id = id(unique_node)
            else:
                raise KeywordAttrsError('`unique_node` must be type of ChainDict.')

        if unique_node_id is None:
            if constraint is not None and isinstance(constraint, dict):
                if 'args' not in constraint or 'kwargs' not in constraint:
                    raise KeywordAttrsError('`args` and `kwargs` must in constraint.')
                find_func = find_func if find_func is not None else self.find_nodes_by_tag_text_attrs
                node = find_func(*constraint['args'], **constraint['kwargs'], one_=True)
                unique_node_id = id(node)
            else:
                raise KeywordAttrsError('`constraint` must be assign.')

        if unique_node_id is None:
            raise NotNodeFound('Constraint node not found.')

        return unique_node_id

    @limit_one
    def find_nodes_with_sibling_ancestor(self
            , unique_node: Optional[ChainDict] = None
            , *args
            , tag_: str = None
            , text_: str = None
            , one_=False
            , find_func: Optional[Callable] = None # default: find_nodes_by_tag_text_attrs
            , constraint: Optional[Dict[str, Any]] = None # {'args': [], 'kwargs': {}}
            , **kwargs
        ) -> Union[List[ChainDict], ChainDict]:

        unique_node_id = self.__find_constraint_node(unique_node, find_func, constraint)

        t_node_ids = [id(_1) for _1 in self.find_nodes_by_tag_text_attrs(tag_=tag_, text_=text_, *args, **kwargs)]
        if len(t_node_ids) <= 0:
            return []

        nodes = []
        for t_node_id in t_node_ids:
            for _1 in self.objects.sibling_ancestor(t_node_id):
                if unique_node_id in _1:
                    nodes.append(self._id_nodes[t_node_id])
                    break
        return nodes

    @limit_one
    def find_nodes_with_ancestor(self
            , unique_node: Optional[ChainDict] = None
            , *args
            , tag_: str = None
            , text_: str = None
            , one_=False
            , find_func: Optional[Callable] = None # default: find_nodes_by_tag_text_attrs
            , constraint: Optional[Dict[str, Any]] = None # {'args': [], 'kwargs': {}}
            , **kwargs
        ) -> Union[List[ChainDict], ChainDict]:

        unique_node_id = self.__find_constraint_node(unique_node, find_func, constraint)

        t_node_ids = [id(_1) for _1 in self.find_nodes_by_tag_text_attrs(tag_=tag_, text_=text_, *args, **kwargs)]
        if len(t_node_ids) <= 0:
            return []

        nodes = []
        for t_node_id in t_node_ids:
            for _1 in self.objects.ancestor(t_node_id):
                if unique_node_id in _1:
                    nodes.append(self._id_nodes[t_node_id])
                    break
        return nodes

    @limit_one
    def find_nodes_with_descendants(self
            , unique_node: Optional[ChainDict] = None
            , *args
            , tag_: str = None
            , text_: str = None
            , one_=False
            , find_func: Optional[Callable] = None # default: find_nodes_by_tag_text_attrs
            , constraint: Optional[Dict[str, Any]] = None # {'args': [], 'kwargs': {}}
            , **kwargs
        ) -> Union[List[ChainDict], ChainDict]:
        
        unique_node_id = self.__find_constraint_node(unique_node, find_func, constraint)

        t_node_ids = [id(_1) for _1 in self.find_nodes_by_tag_text_attrs(tag_=tag_, text_=text_, *args, **kwargs)]
        if len(t_node_ids) <= 0:
            return []

        nodes = []
        for t_node_id in t_node_ids:
            if unique_node_id in self.objects.descendants(t_node_id):
                nodes.append(self._id_nodes[t_node_id])
        return nodes

    def find_nodes_by_magic_path(self, magic_path: str):
        # 用类似于 XPATH 的路径语法搜索节点
        # a[id='okk']
        ...

    def popitem(self, obj: ChainDict) -> ChainDict:
        self.objects.signal_del_node_base(obj)

    def pop_node_by_attrs(self, **kwargs):
        obj = self.find_nodes_by_attrs(one_=True, **kwargs)
        return self.popitem(obj)

    def pop_nodes_by_attrs(self, **kwargs) -> List[ChainDict]:
        objs = self.find_nodes_by_attrs(**kwargs)
        del_nodes = []
        for obj in objs:
            del_nodes.append(self.popitem(obj))
        return del_nodes

    def add_attrs(self, node, *args, **kwargs) -> None:
        for attr_name, value in args+tuple(kwargs.items()):
            value = str(value)
            if attr_name not in node:
                node[attr_name] = value
                self.objects.signal_add_attr_base(node, attr_name, value)

    def update_attr(self, node: ChainDict, attr_name: str, new_value: Any) -> Tuple[str, str]:
        if attr_name in node:
            old_search_key = f'{attr_name}={node[attr_name]}'
            return_v = (attr_name, node[attr_name])
            node[attr_name] = new_value
            new_search_key = f'{attr_name}={new_value}'
            self.objects.signal_modify_attr(old_search_key, new_search_key, node)
            return return_v
        else:
            raise UpdateError('Unable to update this node, check whether the attribute exists.')

    def del_attr(self, node: ChainDict, attr_name: str) -> Tuple[str, str]:
        attr_value = node[attr_name]
        return_v = (attr_name, attr_value)
        node.pop(attr_name)
        self.objects.signal_del_attr_base(node, attr_name, attr_value)
        return return_v

    def batch_del_attr(self, node: ChainDict, *args) -> List[Tuple[str, str]]:
        return_vs = []
        for attr_name in args:
            return_vs.append(self.del_attr(node, attr_name))
        return return_vs

    def batch_update_attrs(self, node, *args, **kwargs) -> List[Tuple[str, str]]:
        if len(args) < 1 and len(kwargs) < 1:
            raise KeywordAttrsError('Parameters or keyword parameters must be passed in.')
        return_vs = []
        for attr_name, value in args+tuple(kwargs.items()):
            return_vs.append(self.update_attr(node, attr_name, value))
        return return_vs
        
    def update_text(self, node: ChainDict, new_text: Any) -> str:
        if self.real_cdata_key in node:
            old_text = node[self.real_cdata_key]
            node[self.real_cdata_key] = new_text
            self.objects.signal_modify_text(old_text, new_text, node)
            return old_text
        else:
            raise UpdateError('Unable to update this node, `text_` is not found.')

    def clear_text(self, node: ChainDict) -> str:
        return self.update_text(node, '')

    def batch_clear_text(self, nodes: List[ChainDict]) -> List[str]:
        old_values = []
        for node in nodes:
            old_values.append(self.update_text(node, ''))
        return old_values
        
    def insert(self, node: Union[ChainDict, List[Any]], tag: str='', attrs={}, text: str='') -> None:
        if isinstance(node, ChainDict):
            insert_node = ChainDict()
            insert_node[self.real_cdata_key] = ''
            inner_node = ChainDict()
            self.add_attrs(inner_node, **attrs)
            inner_node[self.real_cdata_key] = text
            insert_node[tag] = inner_node
            node.update(insert_node)
            self.objects.signal_add_node(inner_node, insert_node, tag=tag, text=text)
            self.objects.signal_add_node(insert_node, node, tag=tag, text='')
            return inner_node
        elif isinstance(node, list):
            inner_node = ChainDict()
            self.add_attrs(inner_node, **attrs)
            inner_node[self.real_cdata_key] = text
            node.append(inner_node)
            self.objects.signal_add_node(inner_node, node, tag=tag, text='')
            return inner_node
        else:
            raise AddNodeError('Add node error, obj must be `ChainDict` type or `List` type.')

    def move(self) -> None:
        ...

    def save(self, path: str = 'output.xml', encoding='utf-8') -> None:
        self.objects._revert_data(forward=False)
        with open(path, 'w', encoding=encoding) as fp:
            xmltodict.unparse(self.xml, fp)
        self.objects._revert_data()

    def save_json(self, path: str = 'output.json', encoding='utf-8', ori=False) -> None:
        if ori:
            self.objects._revert_data(forward=False)
        with open(path, 'w', encoding=encoding) as fp:
            json.dump(self.xml, fp)
        if ori:
            self.objects._revert_data()

