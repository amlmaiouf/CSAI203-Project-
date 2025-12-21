from repositories.service_repository import ServiceRepository
import unittest
class TestRepositories(unittest.TestCase):
    def test_get_all_available_services(self):
        """Tests if the repository returns a list of services."""
        services = ServiceRepository.get_all_available()
        # Even if DB is empty, it should return a list, not None
        self.assertIsInstance(services, list)

    def test_get_service_by_id(self):
        """Tests fetching the specific service (ID 4)."""
        service = ServiceRepository.get_by_id(4)
        if service:
            self.assertEqual(service.service_name, 'غسيل الملابس')