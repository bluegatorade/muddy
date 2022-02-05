from datetime import datetime
from dataclasses import dataclass
import res_config

class ResConfig:
    date: str
    size: str
    firstname: str
    lastname: str
    phone: str
    email: str

    def __repr__(self):
        return f"{self.date},{self.size},{self.firstname},{self.lastname},{self.phone},{self.email}"

    def FromString(s: str):
        x = s.replace("\n", "").split(',')
        return ResConfig(x[0],x[1],x[2],x[3],x[4],x[5])

    def __init__(self, date, size, firstname, lastname, phone, email):
        if not date:
            raise ValueError("date missing")
        if not size:
            raise ValueError("size missing")
        if not firstname:
            raise ValueError("firstname missing")
        if not lastname:
            raise ValueError("lastname missing")
        if not phone:
            raise ValueError("phone missing")
        if not email:
            raise ValueError("email missing")
        try: 
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("invalid date")

        if len(date) != len('2022-02-08'):
            raise ValueError("invalid date (must be YYYY-MM-DD)") 

        try:
            s = int(size)
            if s < 1 or s > 4:
                raise ValueError("size must be in [1-4]")
        except TypeError as e:
            raise ValueError("size must be in [1-4]")
        
        if firstname == "" or lastname == "" or phone == "" or email == "":
            raise ValueError("empty fields")
        
        self.date = date
        self.size = size
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        self.email = email
