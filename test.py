from EntityNode import EntityNode

import pytest

class Test:
    def test_get_parent():
        parent = EntityNode("aminities", ["aminity", "aminitiies", "amminites"], parent=None, entype="normal", metaData=None)
        node1 = EntityNode("wifi", ["wifi", "internet"],parent=parent, entype="Normal", metaData=None)
        assert node1.get_parent() == (parent, "aminities")

        node2 = EntityNode("orange", ["fruit"])
        assert node2.get_parent() == (None, None)
    def test_get_children():
        parent = EntityNode("aminities", ["aminity", "aminitiies", "amminites"], parent=None, entype="normal", metaData=None)
        children1 = EntityNode("wifi", ["wifi", "internet"],parent=parent, entype="Normal", metaData=None)
        children2 = EntityNode("AC", ["Air-conditioner","A-C","AC"], parent=parent, entype="Normal", metaData=None)
        assert parent.get_children() == ([children1, children2], ["wifi", "AC"])

        node4 = EntityNode("apple", ["fruit"])
        assert node4.get_children() == (None, None)
    def test_get_siblings():
          parent = EntityNode("aminities", ["aminity", "aminitiies", "amminites"], parent=None, entype="normal", metaData=None)
          children1 = EntityNode("wifi", ["wifi", "internet"],parent=parent, entype="Normal", metaData=None)
          children2 = EntityNode("AC", ["Air-conditioner","A-C","AC"], parent=parent, entype="Normal", metaData=None)
          assert children1.get_siblings() == (children2,"AC")

          node4 = EntityNode("apple", ["fruit"])
          assert node4.get_siblings() == (None, None)
    def test_str_method(capsys):
        parent = EntityNode("aminities", ["aminity", "aminitiies", "amminites"], parent=None, entype="normal", metaData=None)
        children1 = EntityNode("wifi", ["wifi", "internet"],parent=parent, entype="Normal", metaData=None)
        children2 = EntityNode("AC", ["Air-conditioner","A-C","AC"], parent=parent, entype="Normal", metaData=None)
        grandchild = EntityNode("speed", ["speed", "fast"], parent=children1)

        parent.__str__()
        captured = capsys.readouterr()
        expected_output = ("parent    ['aminity', 'aminitiies', 'amminites'] ['aminities'] None normal None\n"
                           "├── children1 ['wifi', 'internet'] ['wifi'] parent normal None\n"
                           "│   └── grandchild ['speed', 'fast-child'] ['speed'] children1 normal None\n"
                           "└── children2 ['A-C', 'Air-conditioner','AC] ['AC'] parent normal None\n")
        assert captured.out == expected_output
    
    