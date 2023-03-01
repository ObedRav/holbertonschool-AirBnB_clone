#!/usr/bin/python3
"""
Module Name:
base_model

Module Description:
This module contains only one Class

Module Classes:
- BaseModel

Module Attributes:
- None
"""
import uuid
from datetime import datetime


class BaseModel:
    """
    The BaseModel class is a Python class that can be used as a base class
    for other classes that require common functionality such as creating a
    unique ID, saving to a database, and converting to a dictionary.
    """

    def __init__(self, *args, **kwargs) -> None:
        from models import storage
        """
        This method is called when an instance of the class is created.
        It initializes the instance's attributes id, created_at, and updated_at

        Attributes:
        ----------------
        id: is a unique identifier generated using the uuid.uuid4() method.
        created_at and updated_at: are set to the current date and time
                                   using the datetime.now() method.
        """

        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != '__class__':
                    # Everything will be added as an attribute except the class
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self) -> str:
        """
        This method returns a string representation of the instance.
        The string includes the instance's class name, id, and attributes.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        from models import storage
        """
        This method updates the updated_at attribute to the current date
        and time using the datetime.now() method. It can be used to indicate
        that an instance has been modified and needs to be saved.
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self) -> dict:
        """
        This method returns a dictionary representation of the instance.
        The dictionary includes all of the instance's attributes,
        as well as the class name, created_at, and updated_at attributes.
        The created_at and updated_at attributes are formatted as ISO 8601
        strings using the datetime.isoformat() method.
        """
        data = {}
        for key, value in self.__dict__.items():
            if key in ['created_at', 'updated_at']:
                data[key] = value.isoformat()
            else:
                data[key] = value
        data['__class__'] = self.__class__.__name__
        return data
