from typing import Union, List, Dict


class Storage:
    """A class for storing the Step Details and stats.

    This class provides methods for managing data in a list or dictionary format and 
    handles appending values, retrieving data, and clearing the storage.
    """

    _vehicles = []
    _stats = {}

    def __init__(self, **kwargs):
        """Initializes the storage with the specified data type.

        Args:
            kwargs: A dictionary containing optional parameters:
                - "data_type": Type of storage ('list', or 'dict'). Defaults to 'list'.
        """
        self.stats: Dict = {}

        data_type = kwargs.get("data_type", "list")
        if data_type == "list":
            self.data: list = []
        elif data_type == "dict":
            self.data: dict = {}
        else:
            raise ValueError("Unsupported data_type. Use 'list', or 'dict'.")

    def add(self, data):
        """
        Add data to the storage (list, or dict) based on the current storage type.

        Args:
            data (Any | tuple): The data to add to the storage.
                - **For list**: Can be any data type (e.g., int, string, object).
                - **For dict**: Must be a tuple containing exactly two elements,
                where the first element is the key (hashable), and the second
                element is the value (any type).

        Raises:
            ValueError: If `data` is provided as a tuple but does not contain exactly
                        two elements when the storage is a dictionary.
            TypeError: If the storage type is unsupported or if `data` does not match
                    the expected format for the current storage type.
        """
        if isinstance(self.data, list):
            self.data.append(data)
        elif isinstance(self.data, dict):
            if isinstance(data, tuple) and len(data) == 2:
                key, value = data
                if key not in self.data:
                    self.data[key] = set()
                self.data[key].update(value)
            else:
                raise ValueError("Storage: For dict type, data must be a tuple (key, value).")
        else:
            raise TypeError("Storage: Unsupported storage type.")

    def add_stat(self, stats):
        """
        Add stats to the storage.

        Args:
            stats (Dict): The stats to add to the storage.
        """
        self.stats = stats

    def get_data(self) -> Union[List, Dict]:
        """Returns the stored data. set data is converted to list.

        Returns:
            Union[List, Dict]: The stored data, either a list or dictionary.
        """
        data = self.data

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, set):
                    data[key] = list(set(value))
        elif isinstance(data, set):
            data = list(data)

        return data

    def get_stats(self) -> Dict:
        """Returns the stored stats.

        Returns:
            Dict: The stored stats as a dictionary.
        """
        return self.stats

    def clear(self):
        """Clears the stored data and stats.

        This method empties the list or dictionary stored in `self.data` and resets
        the stats to an empty dictionary.
        """
        self.data.clear()
        if self.stats is not None:
            self.stats.clear()
