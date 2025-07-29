from typing import Generator
import pytest
from app.LoadBalancer import LoadBalancer, LoadBalancerException
from unittest.mock import patch

@pytest.fixture
def mock_load_balancer() -> LoadBalancer:
    return LoadBalancer()

@pytest.fixture
def mock_load_balancer_random() -> Generator[LoadBalancer, None, None]:
    with patch("random.choice", return_value="my_mock_instace"):
        yield LoadBalancer()

class TestLoadBalancer:
    def test_instance_registry(self, mock_load_balancer: LoadBalancer):
        mock_load_balancer.register_instance("my_instance")
        assert len(mock_load_balancer._instances) == 1
        assert "my_instance" in mock_load_balancer._instances
        
    
    def test_instance_registry_repeated(self, mock_load_balancer: LoadBalancer):
        mock_load_balancer.register_instance("instance")
        with pytest.raises(LoadBalancerException):
            mock_load_balancer.register_instance("instance")
        
    def test_instance_registry_limit_reached(self, mock_load_balancer: LoadBalancer):
        addresses = [f"address_{i}" for i in range(0, 10)]
        for address in addresses:
            mock_load_balancer.register_instance(address)
        with pytest.raises(LoadBalancerException):
            mock_load_balancer.register_instance("eleven instace")

    def test_get_instance_empty(self, mock_load_balancer: LoadBalancer):
        with pytest.raises(LoadBalancerException):
            mock_load_balancer.get_instance()
        
    def test_get_instance(self, mock_load_balancer: LoadBalancer):
        mock_load_balancer.register_instance("my_instance")
        assert mock_load_balancer.get_instance() == "my_instance"

    def test_get_instance_mock(self, mock_load_balancer_random: LoadBalancer):
        mock_load_balancer_random.register_instance("my_instace")
        assert "my_mock_instace" == mock_load_balancer_random.get_instance()
    
    def test_get_instance_round_robin_empty(self, mock_load_balancer: LoadBalancer):
        with pytest.raises(LoadBalancerException):
            mock_load_balancer.get_instance_round_robin()

    def test_get_instance_round_robin(self, mock_load_balancer: LoadBalancer):
        addresses = [f"address_{i}" for i in range(0, 10)]
        for address in addresses:
            mock_load_balancer.register_instance(address)
        for i, address in enumerate(addresses):
            assert addresses[i] == mock_load_balancer.get_instance_round_robin()
        assert addresses[0] == mock_load_balancer.get_instance_round_robin()
        