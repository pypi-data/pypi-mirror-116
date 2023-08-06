from .Base import Base
from .Script import Script
from .RC import CLASSES
from .MacroNodeTypes import build_macro_classes


class MacroScript(Script):
    """Besides all the properties of a Script, a MacroScript automatically adds input and output nodes to the flow,
    and locally defines a new Node class and registers it in the session."""

    id_ctr = Base.IDCtr()  # using custom ID to count MacroScripts

    """
    the custom ID ensures that I don't need to change the macro node class's identifier when the script's title changes.
    the ID gets stored when serializing and is reloaded in a way that the ctr will afterwards still be larger than
    any ID used, even if there were macro scripts deleted which created holes in the ID assignments, so we don't get
    dangerous overlapping.
    notice that id_ctr is defined statically for MacroScript, and not for Base, so this won't affect other
    Base subclasses, only MacroScripts.
    """

    # custom node classes
    MacroInputNode, MacroOutputNode, MacroNode = None, None, None

    @classmethod
    def build_node_classes(cls):
        """
        Triggered by the session during initialization.
        Internally defined nodes must get built dynamically, during session initialization
        because the user can provide a custom node base class for all nodes, which affects the inheritance
        of all internal nodes too.
        """
        cls.MacroInputNode, \
        cls.MacroOutputNode, \
        cls.MacroNode = \
            build_macro_classes(BaseClass=CLASSES['node base'])

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, session, title: str = None, config_data: dict = None, create_default_logs=True):

        self.input_node, self.output_node = None, None
        self.parameters: [dict] = []
        self.returns: [dict] = []
        self.caller = None

        # notice there is only one caller reference, not a stack of callers. it is not allowed to call a macro
        # recursively, as this would bring at the very least immense performance issues for retaining all data,
        # and it wouldn't make sense at all with sequential nodes.

        self.ID = self.id_ctr.count()
        if config_data and 'ID' in config_data:
            self.ID = max(config_data['ID'], self.ID)
        self.id_ctr.set_count(self.ID)

        super().__init__(session, title, config_data, create_default_logs)

        _self = self

        class CustomMacrotionScriptNode(_self.MacroNode):

            identifier = _self.macro_node_identifier()

            title = _self.title

            # it is important that these two static attributes are defined here ant NOT in MacroScriptNode
            # otherwise they would result in the same for ALL MacroScriptNodes
            macro_script = _self
            instances = []

        self.macro_node_class = CustomMacrotionScriptNode
        self.session.register_node(self.macro_node_class)

        if self.init_config:
            self.parameters = self.init_config['parameters']
            self.returns = self.init_config['returns']


    def macro_node_identifier(self):
        # not using the script title here anymore, because although it's unique, it can change
        return f'MACRO_NODE_{self.ID}'


    def load_flow(self):
        super().load_flow()

        if self.init_config:
            # find input and output node that have already been created by the flow
            for node in self.flow.nodes:
                if node.identifier == self.MacroInputNode.identifier:
                    self.input_node = node
                elif node.identifier == self.MacroOutputNode.identifier:
                    self.output_node = node
        else:
            self.input_node = self.flow.create_node(self.MacroInputNode)
            self.output_node = self.flow.create_node(self.MacroOutputNode)


    def add_parameter(self, type_, label):
        self.parameters.append({'type': type_, 'label': label})

        for mn in self.macro_node_class.instances:
            mn.create_input(label=label, type_=type_)

    def remove_parameter(self, index):
        self.parameters.remove(self.parameters[index])

        for mn in self.macro_node_class.instances:
            mn.delete_input(index)

    def add_return(self, type_, label):
        self.returns.append({'type': type_, 'label': label})

        for mn in self.macro_node_class.instances:
            mn.create_output(label, type_)

    def remove_return(self, index):
        self.returns.remove(self.returns[index])

        for mn in self.macro_node_class.instances:
            mn.delete_output(index)

    def serialize(self) -> dict:
        script_dict = super().serialize()

        script_dict['parameters'] = self.parameters
        script_dict['returns'] = self.returns
        script_dict['ID'] = self.ID

        return script_dict
