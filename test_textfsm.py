import pytest
from textfsmlab import *   
@pytest.mark.neighbor
def test_createcommandfromneighbor():
    assert createcommandfromneighbor("172.31.8.1") == ['interface Gig0/0', 'description Connect to G0/0 of S0', 'exit']
    assert createcommandfromneighbor("172.31.8.2") == ['interface Gig0/2', 'description Connect to G0/0 of R2', 'exit', 'interface Gig0/1', 'description Connect to G0/0 of R1', 'exit', 'interface Gig0/3', 'description Connect to G0/0 of S1', 'exit', 'interface Gig0/0', 'description Connect to G0/0 of R0', 'exit']
    assert createcommandfromneighbor("172.31.8.3") == ['interface Gig0/1', 'description Connect to G0/1 of R2', 'exit', 'interface Gig0/0', 'description Connect to G0/3 of S0', 'exit']
    assert createcommandfromneighbor("172.31.8.4") == ['interface Gig0/1', 'description Connect to G0/2 of R2', 'exit', 'interface Gig0/0', 'description Connect to G0/1 of S0', 'exit']
    assert createcommandfromneighbor("172.31.8.5") == ['interface Gig0/0', 'description Connect to G0/2 of S0', 'exit', 'interface Gig0/2', 'description Connect to G0/1 of R1', 'exit', 'interface Gig0/1', 'description Connect to G0/1 of S1', 'exit']
@pytest.mark.blindport
def test_createcommandblindport():
    assert createcommandblindport("R0") == ['interface Gig0/1', 'description Connect to WAN', 'exit']
    assert createcommandblindport("R1") == ['interface Gig0/2', 'description Connect to Pc', 'exit']
    assert createcommandblindport("R2") == ['interface Gig0/3', 'description Connect to WAN', 'exit']
    assert createcommandblindport("S1") == ['interface Gig0/2', 'description Connect to Pc', 'exit']
    assert createcommandblindport("S0") == []
if __name__ == "__main__":
    test_createcommandfromneighbor()
    test_createcommandblindport()
